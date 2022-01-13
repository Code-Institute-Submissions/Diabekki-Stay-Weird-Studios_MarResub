from django.http import HttpResponse

from django.template.loader import render_to_string
from django.conf import settings

from .models import Purchase, PurchaseLineItem
from merchandise.models import Merch

import json
import time


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        pid = intent.id
        cart = intent.metadata.cart
        save_info = intent.metadata.save_info

        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        grand_total = round(intent.charges.data[0].amount / 100, 2)

        # Clean data in the shipping details
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        # Update profile information if save_info was checked
        user = None
        username = intent.metadata.username
        if username != 'AnonymousUser':
            user = UserProfile.objects.get(user__username=username)
            if save_info:
                user.default_phone_number = shipping_details.phone
                user.default_country = shipping_details.address.country
                user.default_town_or_city = shipping_details.address.city
                user.default_street_address1 = shipping_details.address.line1
                user.default_street_address2 = shipping_details.address.line2
                user.save()

        purchase_exsits = False
        attempt = 1
        while attempt <= 5:
            try:
                purchase = Purchase.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    country__iexact=shipping_details.address.country,
                    town_or_city__iexact=shipping_details.address.city,
                    street_address1__iexact=shipping_details.address.line1,
                    street_address2__iexact=shipping_details.address.line2,
                    grand_total=grand_total,
                    original_cart=cart,
                    stripe_pid=pid,
                )
                purchase_exsits = True
                break
            except Purchase.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if purchase_exsits:
            self._send_confirmation_email(purchase)
            return HttpResponse(
                content=(f'Webhook received: {event["type"]} | SUCCESS: '
                         'Verified purchase already in database'),
                status=200)
        else:
            purchase = None
            try:
                purchase = Purchase.objects.create(
                    full_name=shipping_details.name,
                    user_profiles=user,
                    email=billing_details.email,
                    phone_number=shipping_details.phone,
                    country=shipping_details.address.country,
                    town_or_city=shipping_details.address.city,
                    street_address1=shipping_details.address.line1,
                    street_address2=shipping_details.address.line2,
                    original_cart=cart,
                    stripe_pid=pid,
                )
                for merch_id, merch_data in json.loads(cart).items():
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
            except Exception as e:
                if purchase:
                    purchase.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)
        self._send_confirmation_email(purchase)
        return HttpResponse(
            content=(f'Webhook received: {event["type"]} | SUCCESS: '
                     'Created purchase in webhook'),
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)