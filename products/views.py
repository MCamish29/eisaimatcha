from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Tea, Equipment, Kit

def all_products(request):
    """A view to return all products page with category and search filters"""
    
    category_filter = request.GET.get('category', None)  # Get category filter from URL parameters
    # Fetch all products
    teas = Tea.objects.all()
    equipment = Equipment.objects.all()
    kits = Kit.objects.all()
    search = None
    
    
    # Search functionality
    if request.GET.get('q'):
        search = request.GET['q']
        if not search:
            messages.error(request, "No search criteria entered!")
            return redirect(reverse('products'))
        
        # Perform search in category names, product names, and descriptions
        queries = Q(category__category__icontains=search) | Q(product_name__icontains=search) | Q(description__icontains=search)
        teas = teas.filter(queries)
        equipment = equipment.filter(queries)
        kits = kits.filter(queries)
    
    # Apply category filter (if category is passed in the URL)
    if category_filter:
        if category_filter.lower() == 'tea':
            teas = teas.all()
            equipment = Equipment.objects.none()
            kits = Kit.objects.none()
        elif category_filter.lower() == 'equipment':
            equipment = equipment.all()
            teas = Tea.objects.none()
            kits = Kit.objects.none()
        elif category_filter.lower() == 'kits':
            kits = kits.all()
            teas = Tea.objects.none()
            equipment = Equipment.objects.none()

    # Combine all filtered products into one list
    all_products = list(teas) + list(equipment) + list(kits)
    
    context = {
        'all_products': all_products,
        'search_term': search,
    }
    
    return render(request, 'products/products.html', context)
