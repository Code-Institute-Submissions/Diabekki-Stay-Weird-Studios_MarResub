from django.contrib import admin
from .models import Purchase, PurchaseLineItem


class PurchaseLineItemAdminInline(admin.TabularInline):
    model = PurchaseLineItem
    readonly_fields = ('lineitem_total',)


class PurchaseAdmin(admin.ModelAdmin):
    inlines = (PurchaseLineItemAdminInline,)

    readonly_fields = ('purchase_number', 'date',
                       'delivery_cost', 'purchase_total',
                       'grand_total', 'original_cart', 
                       'stripe_pid')

    fields = ('purchase_number', 'date', 'full_name', 
              'email', 'phone_number', 'country',
              'town_or_city', 'street_address1',
              'street_address2', 'delivery_cost',
              'purchase_total', 'grand_total', 'original_cart', 
              'stripe_pid')

    list_display = ('purchase_number', 'date', 'full_name',
                    'purchase_total', 'delivery_cost',
                    'grand_total',)

    ordering = ('-date',)


admin.site.register(Purchase, PurchaseAdmin)
