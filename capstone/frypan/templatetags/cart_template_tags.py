from django import template
from frypan.models import Order
from django.shortcuts import get_object_or_404

register = template.Library()

@register.filter

def cart_item_count(user):
    if user.is_authenticated:
        order = Order.objects.get(user=user, ordered=False)
        sum = 0
        for item in order.items.all():
            sum += item.quantity
    return sum