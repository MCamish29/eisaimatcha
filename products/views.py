from django.shortcuts import render,redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Tea, Equipment, Kit

def all_products(request):
    """A view to return all products page"""
    
    # Fetch all products
    teas = Tea.objects.all()
    equipment = Equipment.objects.all()
    kits = Kit.objects.all()
    search = None
    if request.GET:
        if 'q' in request.GET:
            search = request.GET['q']
            if not search:
                messages.error(request, "No search criteria entered!")
                return redirect(reverse('products'))
            
            # Perform search in category names, product names, and descriptions
            queries = Q(category__category__icontains=search) | Q(product_name__icontains=search) | Q(description__icontains=search)
            teas = teas.filter(queries)
            equipment = equipment.filter(queries)
            kits = kits.filter(queries)
    
    # Combine all products into one list (optional, if you want to display them all together)
    all_products = list(teas) + list(equipment) + list(kits)
    
    context = {
        'all_products': all_products,
        'search_term': search,
    }
    
    return render(request, 'products/products.html', context)
