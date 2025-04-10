from django.http import HttpResponse
import stripe
import json
import time
from .models import Order, OrderLineItem
from products.models import Tea, Equipment, Kit
from profiles.models import UserProfile
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

class StripeWH_Handler:
    """
    Handle Stripe Webhooks
    """

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        """Send the user a confirmation email"""
        cust_email = order.email
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order})
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})
        
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email]
        )        

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        print(f"Received event: {event['type']}")  # Debugging
        return HttpResponse(
            content=f'Unhandled Webhook received: {event["type"]}',
            status=200
        )

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe.
        """
        print(f"Handling payment intent succeeded for event: {event['type']}")  # Debugging

        intent = event.data.object
        pid = intent.id
        bag = intent.metadata.get("bag", "{}")  # Default to empty JSON if missing
        save_info = intent.metadata.get("save_info", False)

        # Get the Charge object if available
        stripe_charge = None
        if intent.latest_charge:
            try:
                stripe_charge = stripe.Charge.retrieve(intent.latest_charge)
            except stripe.error.StripeError as e:
                return HttpResponse(
                    content=f'Webhook error: Could not retrieve charge: {e}',
                    status=500
                )

        # Extract billing and shipping details
        billing_details = stripe_charge.billing_details if stripe_charge else intent.billing_details
        shipping_details = intent.shipping

        # Get grand total safely
        grand_total = round(stripe_charge.amount / 100, 2) if stripe_charge else round(intent.amount / 100, 2)

        # Clean shipping details
        if shipping_details and shipping_details.address:
            for field, value in shipping_details.address.items():
                if value == "":
                    shipping_details.address[field] = None

         # Update profile information if save_info was checked
        profile = None
        username = intent.metadata.username
        if username != 'AnonymousUser':
            profile = UserProfile.objects.get(user__username=username)
            if save_info:
                profile.default_phone_number = shipping_details.phone                
                profile.default_street_address1 = shipping_details.address.line1
                profile.default_street_address2 = shipping_details.address.line2
                profile.default_town_or_city = shipping_details.address.city
                profile.default_county = shipping_details.address.state
                profile.default_country = shipping_details.address.country
                profile.default_postcode = shipping_details.address.postal_code
                profile.save()

        # Check if order already exists
        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    street_address1__iexact=shipping_details.address.line1,
                    street_address2__iexact=shipping_details.address.line2,
                    town_or_city__iexact=shipping_details.address.city,
                    county__iexact=shipping_details.address.state,
                    country__iexact=shipping_details.address.country,
                    postcode__iexact=shipping_details.address.postal_code,
                    grand_total=grand_total,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)

        if order_exists:
            self._send_confirmation_email(order)
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in database',
                status=200
            )

        # Create the order if it doesn't exist
        order = None
        try:
            order = Order.objects.create(
                full_name=shipping_details.name,
                email=billing_details.email,
                phone_number=shipping_details.phone,
                street_address1=shipping_details.address.line1,
                street_address2=shipping_details.address.line2,
                town_or_city=shipping_details.address.city,
                county=shipping_details.address.state,
                country=shipping_details.address.country,
                postcode=shipping_details.address.postal_code,
                grand_total=grand_total,
                original_bag=bag,
                stripe_pid=pid,
            )

            # Add order line items
            for item_id, item_data in json.loads(bag).items():
                product = None
                for model in (Tea, Equipment, Kit):  # Try to find the product in any model
                    try:
                        product = model.objects.get(id=item_id)
                        break
                    except model.DoesNotExist:
                        continue

                if product:
                    order_line_item = OrderLineItem(
                        order=order,
                        tea=product if isinstance(product, Tea) else None,
                        equipment=product if isinstance(product, Equipment) else None,
                        kit=product if isinstance(product, Kit) else None,
                        quantity=item_data,
                    )
                    order_line_item.save()
                else:
                    raise ValueError(f"Product with ID {item_id} not found")

        except Exception as e:
            if order:
                order.delete()
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | ERROR: {e}',
                status=500)
        self._send_confirmation_email(order)
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Order created',
            status=200
        )

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        print(f"Handling payment intent failed for event: {event['type']}")  # Debugging
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )
