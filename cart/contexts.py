from decimal import Decimal
from django.conf import settings

def cart_items(request):

    cart_items = []
    total = 0
    merch_count = 0

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