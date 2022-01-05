from django.shortcuts import render, redirect


# Create your views here.


def view_cart(request):
    """ A view for the shopping cart page """

    return render(request, 'cart/cart.html')


def shopping_cart_quantity(request, merch_id):
    """ Number of items added to shopping cart """

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    clothing_size = None
    if 'item_size' in request.POST:
        clothing_size = request.POST['item_size']
    cart = request.session.get('cart', {})

    if clothing_size:
        if merch_id in list(cart.keys()):
            if clothing_size in cart['item_size'].keys():
                cart[merch_id]['item_size'][clothing_size] += quantity
            else:
                cart[merch_id]['item_size'][clothing_size] = quantity
        else:
            cart[merch_id] = {'item_size': {clothing_size: quantity}}
    else:
        if merch_id in list(cart.keys()):
            cart[merch_id] += quantity
        else: 
            cart[merch_id] = quantity

    request.session['cart'] = cart
    return redirect(redirect_url)

