from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings

from .forms import PurchaseForm
from .models import Purchase, PurchaseLineItem
from merchandise.models import Merch
from cart.contexts import cart_items

import stripe


def cart_checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        cart = request.session.get('cart', {})

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
        }
        purchase_form = purchase_form(form_data)
        if purchase_form.is_valid():
            purchase = purchase_form.save()
            for merch_id, merch_data in cart.items():
                try:
                    merch = Merch.objects.get(id=merch_id)
                    if isinstance(merch_data, int):
                        purchase_line_item = PurchaseLineItem(
                            purchase=purchase,
                            merch=merch,
                            quantity=merch_data,
                        )
                        purchase_line_item.save()
                    else:
                        for clothing_size, quantity in merch_data['item_size'].items():
                            purchase_line_item = PurchaseLineItem(
                                purchase=purchase,
                                merch=merch,
                                quantity=quantity,
                                merch_size=clothing_size,
                            )
                            purchase_line_item.save()
                except Merch.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your cart wasn't found in our database. "
                        "Please call us for assistance!")
                    )
                    purchase.delete()
                    return redirect(reverse('view_cart'))

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success', args=[purchase.purchase_number]))
        else:
            messages.error(request, 'There was an error with your form. \
                Please double check your information.')
    else:
        cart = request.session.get('cart', {})
        if not cart:
            messages.error(request, "There's nothing in your cart at the moment")
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
            Did you forget to set it in your environment?')

    template = 'cart_checkout/cart_checkout.html'
    context = {
        'purchase_form': purchase_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)


def cart_checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    save_info = request.session.get('save_info')
    purchase = get_object_or_404(Purchase, purchase_number=purchase_number)
    messages.success(request, f'Order successfully processed! \
        Your order number is {purchase_number}. A confirmation \
        email will be sent to {purchase.email}.')

    if 'cart' in request.session:
        del request.session['cart']

    template = 'cart_checkout/cart_checkout_success.html'
    context = {
        'purchase': purchase,
    }

    return render(request, template, context)