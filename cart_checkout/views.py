from django.shortcuts import (
    render, redirect, reverse, get_object_or_404, HttpResponse
)
from django.views.decorators.http import require_POST
from django.contrib import messages

from .forms import PurchaseForm

def cart_checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "There's nothing added to your cart")
        return redirect(reverse('products'))

    purchase_form = PurchaseForm()
    template = 'cart_checkout/cart_checkout.html'
    context = {
        'purchase_form': purchase_form,
    }

    return render(request, template, context)