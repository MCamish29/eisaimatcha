from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm

# Create your views here.
def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, 'There is nothing in your bag')
        return redirect(reverse('products'))
    
    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form' : order_form,
        'stripe_public_key' : 'pk_test_51Qt8S6LwFJk1QYFLbL5LlfnC9y30GoDERv0a9KVf4P572L7Ht3gNcKDRuKORUk9Rxj2bRAS0NLIBt8j9RoGDdlFQ00UqMRhNRg'
        
    }

    return render(request, template,context)