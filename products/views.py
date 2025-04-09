from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Tea, Equipment, Kit, Category
from .forms import ProductForm


def all_products(request):
    """A view to return all products page with category and search filters"""
    
    category_filter = request.GET.get('category', None)
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
    
    # Apply category filter 
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
            category = form.cleaned_data['category']
            category_name = category.category.lower()

            # Shared fields
            base_fields = {
                'internal_name': form.cleaned_data['internal_name'],
                'product_name': form.cleaned_data['product_name'],
                'description': form.cleaned_data['description'],
                'category': category,
                'image': form.cleaned_data['image'],
                'price': form.cleaned_data['price'],
            }

            if category_name == 'tea':
                Tea.objects.create(
                    **base_fields,
                    blend=form.cleaned_data['blend'],
                    weight=form.cleaned_data['weight'],
                    country_of_origin=form.cleaned_data.get('country_of_origin')
                )
                messages.success(request, 'Successfully added tea product!')

            elif category_name == 'equipment':
                Equipment.objects.create(
                    **base_fields,
                    country_of_origin=form.cleaned_data.get('country_of_origin')
                )
                messages.success(request, 'Successfully added equipment product!')

            elif category_name == 'kit':
                base_fields.pop('country_of_origin', None)  
                Kit.objects.create(**base_fields)
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

def edit_product(request, product_id):
    """A view to edit a product."""
    
    # Check if the user is a superuser
    if not request.user.is_superuser:
        messages.error(request, "You are not authorized to edit this product.")
        return redirect('products')
    
    # Try to find the product in the different models
    product = None
    product_type = None
    if Tea.objects.filter(product_id=product_id).exists():
        product = get_object_or_404(Tea, product_id=product_id)
        product_type = 'Tea'
    elif Equipment.objects.filter(product_id=product_id).exists():
        product = get_object_or_404(Equipment, product_id=product_id)
        product_type = 'Equipment'
    elif Kit.objects.filter(product_id=product_id).exists():
        product = get_object_or_404(Kit, product_id=product_id)
        product_type = 'Kit'
    
    # If no product was found in any model, redirect with an error message
    if not product:
        messages.error(request, "Product not found.")
        return redirect('products')

    # Check if the form is submitted and valid
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            # Manually update the model with the form data based on product type
            product.internal_name = form.cleaned_data['internal_name']
            product.product_name = form.cleaned_data['product_name']
            product.description = form.cleaned_data['description']

            
            if product_type == 'Tea':
                product.blend = form.cleaned_data['blend']
                product.weight = form.cleaned_data['weight'] 
            elif product_type == 'Equipment':                
                pass
            elif product_type == 'Kit':
                pass

            product.category = form.cleaned_data['category']
                        
            if product_type != 'Kit':
                product.country_of_origin = form.cleaned_data['country_of_origin']
            
            product.price = form.cleaned_data['price']

            # If a new image is uploaded, update the image field
            if 'image' in request.FILES:
                product.image = form.cleaned_data['image']
            # If no new image is uploaded, keep the existing image
            else:
                product.image = product.image
            
            product.save()
            messages.success(request, 'Product successfully updated!')
            return redirect('products')
        else:
            print(form.errors)
            messages.error(request, 'Failed to update product. Please check the form for errors.')
    else:
        # Load the form with the current product data
        initial_data = {
            'internal_name': product.internal_name,
            'product_name': product.product_name,
            'description': product.description,
            'blend': product.blend if product_type == 'Tea' else '',
            'weight': product.weight if product_type == 'Tea' else '',
            'category': product.category,
            'image': product.image, 
            'price': product.price,
        }        
        
        if product_type != 'Kit':
            initial_data['country_of_origin'] = product.country_of_origin
        
        form = ProductForm(initial=initial_data)
    
    context = {
        'form': form,
        'product': product,
        'product_type': product_type
    }
    return render(request, 'products/edit_products.html', context)

def delete_product(request, product_id):
    """A view to delete a product."""
    
    # Check if the user is a superuser
    if not request.user.is_superuser:
        messages.error(request, "You are not authorized to delete this product.")
        return redirect('products')
    
    # Try to find the product in the different models
    product = None
    if Tea.objects.filter(product_id=product_id).exists():
        product = get_object_or_404(Tea, product_id=product_id)
    elif Equipment.objects.filter(product_id=product_id).exists():
        product = get_object_or_404(Equipment, product_id=product_id)
    elif Kit.objects.filter(product_id=product_id).exists():
        product = get_object_or_404(Kit, product_id=product_id)
    
    if product:
        product.delete()
        messages.success(request, 'Product successfully deleted!')
    else:
        messages.error(request, 'Product not found!')    
    
    return redirect('products')