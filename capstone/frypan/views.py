from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from  .models import Item, OrderItem, Order
from .forms import CheckoutForm

def home(request):
    context = {
        'items':Item.objects.all()
    }
    return render(request,'home.html',context)

def about_us(request):
    return render(request, 'aboutUs.html')

def contact_us(request):
    return render(request, 'contactUs.html')

def checkout(request):
    form = CheckoutForm()
    context = {
        'form': form
    }
    return render(request, 'checkout.html', context)

def checkout_submit(request):
    form = CheckoutForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)
        print("form is valid")
        return redirect('frypan:checkout')

@login_required
def order_summary(request):
    try:
        order = Order.objects.get(user=request.user, ordered=False)
        context = {
            'order': order
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