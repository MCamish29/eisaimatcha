from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib import messages

from products.models import Tea, Equipment, Kit

# Create your views here.
def view_bag(request):
    return render(request, 'bag/bag.html')

def add_to_bag(request, item_id):
  
    product = None
    
    try:
        product = Tea.objects.get(pk=item_id)
    except Tea.DoesNotExist:
        try:
            product = Equipment.objects.get(pk=item_id)
        except Equipment.DoesNotExist:
            try:
                product = Kit.objects.get(pk=item_id)
            except Kit.DoesNotExist:
                messages.error(request, "Product not found!")
                return redirect('view_bag')
            
            
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    bag  = request.session.get('bag', {})

    if item_id in list(bag.keys()):
        bag[item_id] += quantity
    else:
        bag[item_id] = quantity
        messages.success(request, f'Added {product.product_name} to your bag')

    request.session['bag'] = bag
    return redirect(redirect_url)

def adjust_bag(request, item_id):

    quantity = int(request.POST.get('quantity'))
    bag = request.session.get('bag', {})

    if quantity > 0:
        bag[item_id] = quantity
    else:
        bag.pop(item_id, None)

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))

def remove_from_bag(request, item_id):

    try:
        bag = request.session.get('bag', {})

        bag.pop(item_id, None)

        request.session['bag'] = bag
        return HttpResponse(status=200)
    except Exception as e:
        return HttpResponse(status=500)

