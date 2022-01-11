from django.shortcuts import (render, redirect, reverse, get_object_or_404, HttpResponse)
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
from .forms import PurchaseForm
from cart.contexts import cart_items
import stripe

def cart_checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "There's nothing added to your cart")
        return redirect(reverse('merchandise'))

    current_cart = cart_items(request)
    total = current_cart['grand_total']
    stripe_total = round(total * 100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    purchase_form = PurchaseForm()

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
            did you forget to set it up in your enviroment?')

    template = 'cart_checkout/cart_checkout.html'
    context = {
        'purchase_form': purchase_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)