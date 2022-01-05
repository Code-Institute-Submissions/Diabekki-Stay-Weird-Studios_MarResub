from django.shortcuts import render, redirect


# Create your views here.


def view_cart(request):
    """ A view for the shopping cart page """

    return render(request, 'cart/cart.html')


def shopping_cart_quantity(request, merch_id):
    """ Number of items added to shopping cart """

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})

    if merch_id in list(cart.keys()):
        cart[merch_id] += quantity
    else: 
        cart[merch_id] = quantity

        request.session['cart'] = cart
        return redirect(redirect_url)

