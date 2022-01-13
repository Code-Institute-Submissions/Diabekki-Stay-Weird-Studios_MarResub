from django.shortcuts import render, get_object_or_404
from django.contrib import messages

from .models import UserProfile
from .forms import UserProfileForm

from cart_checkout.models import Purchase


def user(request):

    user = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')

    form = UserProfileForm(instance=user)
    purchases = user.purchases.all()

    template = 'user_profiles/user.html'
    context = {
        'form': form,
        'purchases': purchases,
        'on_profile_page': True,
    }
        
    return render(request, template, context)

def purchase_history(request, purchase_number):
    purchase = get_object_or_404(Purchase, purchase_number=purchase_number)

    messages.info(request, (
        f'This is a past confirmation for purchase number {purchase_number}. '
        'A confirmation email was sent on the purchase date.'
    ))

    template = 'cart_checkout/cart_checkout_success.html'
    context = {
        'purchase': purchase,
        'from_user': True,
    }

    return render(request, template, context)