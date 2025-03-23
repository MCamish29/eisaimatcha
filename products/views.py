from django.shortcuts import render
from .models import Tea, Equipment, Kit

def all_products(request):
    """A view to return all products page"""
    
    # Fetch all products
    teas = Tea.objects.all()
    equipment = Equipment.objects.all()
    kits = Kit.objects.all()
    
    # Combine all products into one list (optional, if you want to display them all together)
    all_products = list(teas) + list(equipment) + list(kits)
    
    context = {
        'all_products': all_products,
    }
    
    return render(request, 'products/products.html', context)
