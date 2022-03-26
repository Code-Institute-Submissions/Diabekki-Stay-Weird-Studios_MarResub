from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import PurchaseLineItem


@receiver(post_save, sender=PurchaseLineItem)
def update_save(sender, instance, created, **kwargs):
    """
    Update order total on lineitem update/create
    """
    instance.purchase.update_total_cost()


@receiver(post_delete, sender=PurchaseLineItem)
def update_delete(sender, instance, **kwargs):
    """
    Update order total on lineitem delete
    """
    print('delete signal received')
    instance.purchase.update_total_cost()
