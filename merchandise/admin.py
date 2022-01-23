from django.contrib import admin
from .models import Merch, Category, Comment

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


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'merch',
        'name',
        'email',
        'message',
        'added_on',
        'approved',
    )


admin.site.register(Comment, CommentAdmin)
admin.site.register(Merch, MerchAdmin)
admin.site.register(Category, CategoryAdmin)