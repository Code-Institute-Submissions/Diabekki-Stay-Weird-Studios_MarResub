import uuid
from django.db import models
from django.db.models import Sum

from django_countries.fields import CountryField

from merchandise.models import Merch
from user_profiles.models import UserProfile


class Purchase(models.Model):

    purchase_number = models.CharField(
        max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                     null=True, blank=True,
                                     related_name='purchases')
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(blank_label='Country *', null=False, blank=False)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0)
    purchase_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)
    original_cart = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(
        max_length=254, null=False, blank=False, default='')

    def _generate_purchase_number(self):
        """
        makes random, unique purchase number using UUID
        """
        return uuid.uuid4().hex.upper()

    def update_total_cost(self):
        """
        Update grand total each time a line item is added,
        accounting for delivery costs.
        """
        self.purchase_total = self.lineitems.aggregate(
            Sum('lineitem_total'))['lineitem_total__sum'] or 0
        self.delivery_cost = self.purchase_total / 10
        self.grand_total = self.purchase_total + self.delivery_cost
        self.save()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.purchase_number:
            self.purchase_number = self._generate_purchase_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.purchase_number


class PurchaseLineItem(models.Model):
    purchase = models.ForeignKey(
        Purchase, null=False, blank=False,
        on_delete=models.CASCADE, related_name='lineitems')
    merch = models.ForeignKey(
        Merch, null=False, blank=False, on_delete=models.CASCADE)
    merch_size = models.CharField(
        max_length=2, null=True, blank=True)  # XS, S, M, L, XL
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(
        max_digits=6, decimal_places=2,
        null=False, blank=False, editable=False)

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total
        and update the purchase total cost.
        """
        self.lineitem_total = self.merch.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'SKU {self.merch.sku} on purchase\
            {self.purchase.purchase_number}'
