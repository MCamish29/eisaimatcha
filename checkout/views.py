from django.shortcuts import render, redirect, reverse
from django.shortcuts import get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings


from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Tea, Equipment, Kit
from profiles.forms import UserProfileForm
from profiles.models import UserProfile
from bag.contexts import bag_contents

import stripe
import json


@require_POST
def cache_checkout_data(request):

    """
    Cache checkout data in Stripe before final payment submission.
    """

    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


def checkout(request):

    """
    Process the checkout:
    validate order form, create order, and handle Stripe payment.
    """

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
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_bag = json.dumps(bag)
            order.save()
            # Loop through the items in the shopping bag
            for item_id, item_data in bag.items():
                try:
                    product = None
                    for model in (Tea, Equipment, Kit):
                        try:
                            product = model.objects.get(product_id=item_id)
                            break
                        except model.DoesNotExist:
                            continue

                    if product:
                        # Treat all items as simple quantities
                        order_line_item = OrderLineItem(
                            order=order,
                            tea=product if isinstance(product, Tea) else None,
                            equipment=(
                                product
                                if isinstance(product, Equipment)
                                else None
                                ),
                            kit=product if isinstance(product, Kit) else None,
                            quantity=item_data,
                        )
                        order_line_item.save()
                    else:
                        raise ValueError("Product not found")

                except (
                    Tea.DoesNotExist,
                    Equipment.DoesNotExist,
                    Kit.DoesNotExist,
                    ValueError
                ):
                    messages.error(request, (
                        "One of the products wasn't found in our database."
                        "Please call us for assistance!")
                    )
                    order.delete()  # Delete the order if product is not found
                    return redirect(reverse('view_bag'))

            # Save customer information preference
            request.session['save_info'] = 'save-info' in request.POST

            # Redirect to success page after successful checkout
            return redirect(
                reverse(
                    'checkout_success', args=[order.order_number]
                    )
                )

        else:
            messages.error(
                request,
                'Error on form. Please double check your information.'
            )

    else:
        bag = request.session.get('bag', {})
        if not bag:
            messages.error(
                request,
                "There's nothing in your bag at the moment"
            )
            return redirect(reverse('products'))

        current_bag = bag_contents(request)
        total = current_bag['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                order_form = OrderForm(initial={
                    'full_name': profile.user.get_full_name(),
                    'email': profile.user.email,
                    'phone_number': profile.default_phone_number,
                    'street_address1': profile.default_street_address1,
                    'street_address2': profile.default_street_address2,
                    'town_or_city': profile.default_town_or_city,
                    'county': profile.default_county,
                    'country': profile.default_country,
                    'postcode': profile.default_postcode,
                })
            except UserProfile.DoesNotExist:
                order_form = OrderForm()
        else:
            order_form = OrderForm()

        if not stripe_public_key:
            messages.warning(
                request,
                'Stripe public key is missing. Check environment')

        template = 'checkout/checkout.html'
        context = {
            'order_form': order_form,
            'stripe_public_key': stripe_public_key,
            'client_secret': intent.client_secret,
        }

        return render(request, template, context)


def checkout_success(request, order_number):

    """
    Handle post-checkout success logic,
    update user profile, and show confirmation.
    """

    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        order.user_profile = profile
        order.save()

        # Save the user's info
        if save_info:
            profile_data = {
                'default_phone_number': order.phone_number,
                'default_street_address1': order.street_address1,
                'default_street_address2': order.street_address2,
                'default_town_or_city': order.town_or_city,
                'default_county': order.county,
                'default_country': order.country,
                'default_postcode': order.postcode,
            }
            user_profile_form = UserProfileForm(profile_data, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()

    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
