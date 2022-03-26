from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings

from .forms import PurchaseForm
from .models import Purchase, PurchaseLineItem
from merchandise.models import Merch
from user_profiles.forms import UserProfileForm
from user_profiles.models import UserProfile
from cart.contexts import cart_contents

import stripe
import json


@require_POST
def cache_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'cart': json.dumps(request.session.get('cart', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, ('Sorry, your payment cannot be '
                                 'processed right now. Please try '
                                 'again.'))
        return HttpResponse(content=e, status=400)


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
        purchase_form = PurchaseForm(form_data)
        if purchase_form.is_valid():
            purchase = purchase_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            purchase.stripe_pid = pid
            purchase.original_cart = json.dumps(cart)
            purchase.save()
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
                        "One of the items in your cart wasn't found in our database. "
                        "Please call us for assistance!")
                    )
                    purchase.delete()
                    return redirect(reverse('view_cart'))

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('cart_checkout_success', args=[purchase.purchase_number]))
        else:
            messages.error(request, 'There was an error with your form. \
                Please double check your information.')
    else:
        cart = request.session.get('cart', {})
        if not cart:
            messages.error(request, "There's nothing in your cart at the moment")
            return redirect(reverse('merchandise'))

        current_cart = cart_contents(request)
        total = current_cart['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        # Attempt to prefill the form with any info
        # the user maintains in their profile
        if request.user.is_authenticated:
            try:
                user = UserProfile.objects.get(user=request.user)
                purchase_form = PurchaseForm(initial={
                    'full_name': user.user.get_full_name(),
                    'email': user.user.email,
                    'phone_number': user.default_phone_number,
                    'country': user.default_country,
                    'town_or_city': user.default_town_or_city,
                    'street_address1': user.default_street_address1,
                    'street_address2': user.default_street_address2,
                })
            except UserProfile.DoesNotExist:
                purchase_form = PurchaseForm()
        else:
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


def cart_checkout_success(request, purchase_number):
    """
    Handle successful checkouts
    """
    save_info = request.session.get('save_info')
    purchase = get_object_or_404(Purchase, purchase_number=purchase_number)

    if request.user.is_authenticated:
        user = UserProfile.objects.get(user=request.user)
        # Attach the user's profile to the order
        purchase.user_profile = user
        purchase.save()

        # Save the user's info
        if save_info:
            user_data = {
                'default_phone_number': purchase.phone_number,
                'default_country': purchase.country,
                'default_town_or_city': purchase.town_or_city,
                'default_street_address1': purchase.street_address1,
                'default_street_address2': purchase.street_address2,
            }
            user_profile_form = UserProfileForm(user_data, instance=user)
            if user_profile_form.is_valid():
                user_profile_form.save()

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