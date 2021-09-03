from django.contrib import messages
from django.db import models
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from  .models import Item, OrderItem, Order
from django.conf import settings
from django.urls import reverse
import stripe
stripe.api_key = settings.STRIPE_PRIVATE_KEY


def home(request):
    context = {
        'items':Item.objects.all()
    }
    return render(request,'home.html',context)



def thanks(request):
    order_items = OrderItem.objects.filter(user=request.user, ordered=False)
    for order_item in order_items:
        order_item.delete()
    return render(request, 'thanks.html')

def about_us(request):
    return render(request, 'aboutUs.html')

def contact_us(request):
    return render(request, 'contactUs.html')

@login_required
def order_summary(request):
    try:
        order = Order.objects.get(user=request.user, ordered=False)
        line_items = []
        for order_item in order.items.all():
            line_items.append({
            'price': order_item.items.stripe_price,
            'quantity': order_item.quantity,
            })
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url=request.build_absolute_uri(reverse("frypan:thanks")) + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=request.build_absolute_uri(reverse("frypan:home")),
            )
            context = {
                'order': order,
                'session_id' : session.id,
                'stripe_public_key' : settings.STRIPE_PUBLIC_KEY
            }
        except:
            context = {
                'order': order,
            }
        return render(request, 'orderSummary.html',context)
    except ObjectDoesNotExist:
        messages.error(request, "You do not have an active order")
        return redirect("/")

def product(request, product_id):
    prod = get_object_or_404(Item, id=product_id)
    context = {
        'prod':prod,
        'items':Item.objects.all()
    }
    return render(request,'product.html',context)

@login_required
def add_to_cart(request, product_id):
    item = get_object_or_404(Item, id=product_id)
    order_item, created= OrderItem.objects.get_or_create(
        items=item,
        user = request.user,
        ordered = False
        )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(items__id=item.id).exists():
            order_item.quantity+=1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("frypan:order_summary")
        elif order_item.quantity == 0:
            messages.info(request, "This item was added to your cart.")
            order.items.add(order_item)
            order_item.quantity+=1
            order_item.save()
            return redirect("frypan:order_summary")
        else:
            messages.info(request, "This item was added to your cart.")
            order.items.add(order_item)
            return redirect("frypan:order_summary")
    else:
        order_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=order_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("frypan:order_summary")

@login_required
def remove_single_from_cart(request, product_id):
    item = get_object_or_404(Item, id=product_id)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(items__id=item.id).exists():
            order_item = OrderItem.objects.filter(
                items=item,
                user = request.user,
                ordered = False
                )[0]
            if order_item.quantity > 0:
                order_item.quantity-=1
                order_item.save()
                messages.info(request, "This item quantity was updated.")
                return redirect("frypan:order_summary")
            else:
                order.items.remove(order_item)
                messages.info(request, "This item was removed from your cart.")
                return redirect("frypan:order_summary")
        else:
            messages.info(request, "This item was not in your cart.")
            return redirect("frypan:product", product_id)
    else:
        messages.info(request, "You do not have an active order.")
        return redirect("frypan:product", product_id)

@login_required
def remove_from_cart(request, product_id):
    item = get_object_or_404(Item, id=product_id)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(items__id=item.id).exists():
            order_item = OrderItem.objects.filter(
                items=item,
                user = request.user,
                ordered = False
                )[0]
            order_item.quantity = 0
            order_item.save()   
            order.items.remove(order_item)

            messages.info(request, "This item was removed from your cart.")
            return redirect("frypan:order_summary")
        else:
            messages.info(request, "This item was not in your cart.")
            return redirect("frypan:product", product_id)
    
    else:
        messages.info(request, "You do not have an active order.")
        return redirect("frypan:product", product_id)

@csrf_exempt
def stripe_webhook(request):
    print('WEBHOOK!!!')

    endpoint_secret = 'whsec_4BlUJxkrnKD7JB9miblHVmywsG9YZnEI'

    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)
    if event['type'] == 'checkout.session.completed':

        session = event['data']['object']
    return HttpResponse(status=200)