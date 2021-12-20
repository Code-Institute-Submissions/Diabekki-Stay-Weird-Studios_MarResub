from django.contrib import admin
from .models import Merch, Category

# Register your models here.


class MerchAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'rating',
        'image',
    )

    ordering = ('sku',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


admin.site.register(Merch, MerchAdmin)
admin.site.register(Category, CategoryAdmin)