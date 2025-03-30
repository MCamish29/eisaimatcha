from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings
from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Tea, Equipment, Kit
from bag.contexts import bag_contents  # If you want to keep this helper function
import stripe

def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        bag = request.session.get('bag', {})

        # Form data received from the POST request
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }

        order_form = OrderForm(form_data)
        if order_form.is_valid():
            # Create the order
            order = order_form.save()

            # Loop through the items in the shopping bag
            for item_id, item_data in bag.items():
                try:
                    # Dynamically check each product model (Tea, Equipment, Kit)
                    product = None
                    for model in (Tea, Equipment, Kit):
                        try:
                            product = model.objects.get(product_id=item_id)
                            break  # Stop once we find the product
                        except model.DoesNotExist:
                            continue

                    if product:
                        if isinstance(item_data, int):
                            # If it's a simple quantity (no size differentiation)
                            order_line_item = OrderLineItem(
                                order=order,
                                tea=product if isinstance(product, Tea) else None,
                                equipment=product if isinstance(product, Equipment) else None,
                                kit=product if isinstance(product, Kit) else None,
                                quantity=item_data,
                            )
                            order_line_item.save()
                        else:
                            # If the item has sizes, handle accordingly
                            for size, quantity in item_data['items_by_size'].items():
                                order_line_item = OrderLineItem(
                                    order=order,
                                    tea=product if isinstance(product, Tea) else None,
                                    equipment=product if isinstance(product, Equipment) else None,
                                    kit=product if isinstance(product, Kit) else None,
                                    quantity=quantity,
                                    product_size=size,
                                )
                                order_line_item.save()
                    else:
                        raise ValueError("Product not found")

                except (Tea.DoesNotExist, Equipment.DoesNotExist, Kit.DoesNotExist, ValueError):
                    messages.error(request, (
                        "One of the products in your bag wasn't found in our database. "
                        "Please call us for assistance!")
                    )
                    order.delete()  # Delete the order if product is not found
                    return redirect(reverse('view_bag'))

            # Save customer information preference
            request.session['save_info'] = 'save-info' in request.POST

            # Redirect to success page after successful checkout
            return redirect(reverse('checkout_success', args=[order.order_number]))

        else:
            messages.error(request, 'There was an error with your form. Please double check your information.')

    else:
        # If the request is GET, show the checkout page
        bag = request.session.get('bag', {})
        if not bag:
            messages.error(request, "There's nothing in your bag at the moment")
            return redirect(reverse('products'))

        current_bag = bag_contents(request)  # You can use your existing bag_contents function if you want
        total = current_bag['grand_total']
        stripe_total = round(total * 100)  # Stripe amount must be in cents
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        order_form = OrderForm()

        if not stripe_public_key:
            messages.warning(request, 'Stripe public key is missing. Did you forget to set it in your environment?')

        template = 'checkout/checkout.html'
        context = {
            'order_form': order_form,
            'stripe_public_key': stripe_public_key,
            'client_secret': intent.client_secret,
        }

        return render(request, template, context)


def checkout_success(request, order_number):
    """
    Handle successful checkouts.
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(request, f'Order successfully processed! Your order number is {order_number}. A confirmation email will be sent to {order.email}.')
    
    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }
    return render(request, template, context)
