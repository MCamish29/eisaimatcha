from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Tea, Equipment, Kit, Category
from .forms import ProductForm


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



def add_product(request):
    """ Add a product to the store """
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            # Determine the product type by the category
            category = form.cleaned_data['category']
            
            # Create the corresponding product type based on the selected category
            if category.category.lower() == 'tea':  # Use 'category' field instead of 'name'
                Tea.objects.create(**form.cleaned_data)
                messages.success(request, 'Successfully added tea product!')
            elif category.category.lower() == 'equipment':  # Use 'category' field instead of 'name'
                Equipment.objects.create(**form.cleaned_data)
                messages.success(request, 'Successfully added equipment product!')
            elif category.category.lower() == 'kit':  # Use 'category' field instead of 'name'
                Kit.objects.create(**form.cleaned_data)
                messages.success(request, 'Successfully added kit product!')
            return redirect(reverse('add_product'))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()

    template = 'products/add_products.html'
    context = {
        'form': form,
    }

    return render(request, template, context)