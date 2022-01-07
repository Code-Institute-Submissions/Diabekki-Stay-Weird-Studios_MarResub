from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from merchandise.models import Merch

def cart_items(request):

    cart_items = []
    total = 0
    merch_count = 0
    cart = request.session.get('cart', {})

    for merch_id, merch_data in cart.items():
        if isinstance(merch_data, int):
            merch = get_object_or_404(Merch, pk=merch_id)
            total += merch_data * merch.price
            merch_count += merch_data
            cart_items.append({
                'merch_id': merch_id,
                'quantity': merch_data,
                'merch': merch,
            })
        else:
            merch = get_object_or_404(Merch, pk=merch_id)
            for clothing_size, quantity in merch_data['item_size'].items(): 
                total += quantity * merch.price
                merch_count += quantity
                cart_items.append({
                    'merch_id': merch_id,
                    'quantity': quantity,
                    'merch': merch,
                    'clothing_size': clothing_size,
                    })

    if total:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
    else:
        delivery = 0

    grand_total = delivery + total
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'merch_count': merch_count,
        'delivery': delivery,
        'grand_total': grand_total,
    }

    return context