from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Tea, Equipment, Kit

def bag_contents(request):

    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})
    
    for item_id, quantity in bag.items():
        product = None  # Ensure 'product' is always defined
        
        # Try getting the product from one of the three models
        try:
            product = Tea.objects.get(pk=item_id)
        except Tea.DoesNotExist:
            try:
                product = Equipment.objects.get(pk=item_id)
            except Equipment.DoesNotExist:
                try:
                    product = Kit.objects.get(pk=item_id)
                except Kit.DoesNotExist:
                    continue  # Skip if product ID does not exist in any model
        
        total += quantity * product.price
        product_count += quantity
        bag_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'product': product,
        })



    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = delivery + total

    context = {
        'bag_items' : bag_items,
        'total' : total,
        'product_count' : product_count,
        'delivery' : delivery,
        'free_delivery_delta' : free_delivery_delta,
        'free_delivery_threshold' : settings.STANDARD_DELIVERY_PERCENTAGE,
        'grand_total' : grand_total,
    }

    return context