from django.shortcuts import (render, redirect, reverse, HttpResponse, get_object_or_404)
from django.contrib import messages

from merchandise.models import Merch
# Create your views here.


def view_cart(request):
    """ A view for the shopping cart page """

    return render(request, 'cart/cart.html')


def shopping_cart_quantity(request, merch_id):
    """ Number of items added to shopping cart """

    merch = get_object_or_404(Merch, pk=merch_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    clothing_size = None
    if 'merch_size' in request.POST:
        clothing_size = request.POST['merch_size']
    cart = request.session.get('cart', {})

    if clothing_size:
        if merch_id in list(cart.keys()):
            if clothing_size in cart[merch_id]['item_size'].keys():
                cart[merch_id]['item_size'][clothing_size] += quantity
                messages.success(request, (f'Updated size {clothing_size.upper()} 'f'{merch.name} quantity to 'f'{cart[merch_id]["item_size"][clothing_size]}'))
            else:
                cart[merch_id]['item_size'][clothing_size] = quantity
                messages.success(request, (f'Added size {clothing_size.upper()} 'f'{merch.name} to your shopping cart'))
        else:
            cart[merch_id] = {'item_size': {clothing_size: quantity}}
            messages.success(request, (f'Added size {clothing_size.upper()} 'f'{merch.name} to your shopping'))
    else:
        if merch_id in list(cart.keys()):
            cart[merch_id] += quantity
            messages.success(request, f'Updated {merch.name} number to {cart[merch_id]}!')
        else: 
            cart[merch_id] = quantity
            messages.success(request, f'Added {merch.name} to shopping cart!')

    request.session['cart'] = cart
    return redirect(redirect_url)


def change_cart(request, merch_id):
    """ Changes number of items in shopping cart """

    merch = get_object_or_404(Merch, pk=merch_id)
    quantity = int(request.POST.get('quantity'))
    clothing_size = None
    if 'merch_size' in request.POST:
        clothing_size = request.POST['merch_size']
    cart = request.session.get('cart', {})

    if clothing_size:
        if quantity > 0:
            cart[merch_id]['item_size'][clothing_size] = quantity
            messages.success(request, f'Updated size {clothing_size()}{merch.name} number to {cart[merch_id]["item_size"][clothing_size]}!')
        else:
            del cart[merch_id]['item_size'][clothing_size]
            if not cart[merch_id]['item_size'][clothing_size]:
                cart.pop(merch_id)
            messages.success(request, f'Removed size {clothing_size()}{merch.name} from shopping cart!')
    else:
        if quantity > 0:
            cart[merch_id] = quantity
            messages.success(request, f'Updated {merch.name} number to {cart[merch_id]}!')
        else:
            cart.pop(merch_id)
            messages.success(request, f'Removed {merch.name} from shopping cart!')

    request.session['cart'] = cart
    return redirect(reverse('view_cart'))


def remove_merch(request, merch_id):
    """ Removes items from shopping cart """
    try:
        merch = get_object_or_404(Merch, pk=merch_id)
        clothing_size = None
        if 'merch_size' in request.POST:
            clothing_size = request.POST['merch_size']
            cart = request.session.get('cart', {})
            
        if clothing_size:
            del cart[merch_id]['item_size'][clothing_size]
            if not cart[merch_id]['item_size'][clothing_size]:
                cart.pop(merch_id)
            messages.success(request, f'Removed size {clothing_size()}{merch.name} from shopping cart!')
        else:
            cart.pop(merch_id)
            messages.success(request, f'Removed {merch.name} from shopping cart!')

        request.session['cart'] = cart
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, f'Issue removing item: {e}')
        return HttpResponse(status=200)