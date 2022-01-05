from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from merchandise.models import Merch

def cart_items(request):

    cart_items = []
    total = 0
    merch_count = 0
    cart = request.session.get('cart', {})


    for merch_id, quantity in cart.items():
        merch = get_object_or_404(Merch, pk=merch_id)
        total += quantity * merch.price
        merch_count += quantity
        cart_items.append({
            'merch_id': merch_id,
            'quantity': quantity,
            'merch': merch,
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