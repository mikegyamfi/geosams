import hashlib
import hmac
import json
import random
from datetime import datetime
from time import sleep

import pandas as pd
from decouple import config
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, Permission
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
import requests
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from intel_app import models, forms


# @login_required(login_url='login')
def shop_home_collections(request):
    general_categories = models.Category.objects.all().order_by('name')
    context = {'general_categories': general_categories}
    return render(request, 'shop/collections.html', context=context)


@login_required(login_url='login')
def collection_products(request, category_name):
    print(category_name)
    print(models.Category.objects.filter(name=category_name).exists())
    if models.Category.objects.filter(name=category_name).exists():
        collection = models.Category.objects.get(name=category_name)
        products = models.Product.objects.filter(category=collection)
        category_name = models.Category.objects.filter(name=category_name).first()
        context = {
            'products': products,
            'category_name': category_name
        }
        return render(request, 'shop/collection_products.html', context=context)
    else:
        messages.warning(request, "Link is broken")
        return redirect('shop')


@login_required(login_url='login')
def product_details(request, category_name, prod_name):
    if models.Category.objects.filter(name=category_name):
        if models.Product.objects.filter(name=prod_name):
            product = models.Product.objects.get(name=prod_name)
            product_images = models.ProductImage.objects.filter(product=product)
            main_image = product_images.first()
            category = models.Category.objects.get(name=category_name)
            context = {
                'product': product,
                'cat_name': category.name,
                'images': product_images,
                'main_image': main_image,
                'current_date': datetime.now().date()
            }
            return render(request, 'shop/product_detail.html', context=context)
        else:
            messages.error(request, 'Something went wrong')
            return redirect('shop')
    else:
        messages.error(request, "No such category found")
        return redirect('shop')


@login_required(login_url='login')
def add_to_cart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = models.Product.objects.get(id=prod_id)
            if product_check:
                if models.Cart.objects.filter(user=request.user.id, product_id=prod_id):
                    print("hit it kama")
                    return JsonResponse({'status': "Item already in Cart"})
                else:
                    product_qty = int(request.POST.get('product_qty'))
                    if product_check.quantity >= product_qty:
                        models.Cart.objects.create(user=request.user, product_id=prod_id, product_qty=product_qty)
                        print("hit it kama")
                        return JsonResponse({'status': "Product added to Cart"})
                    else:
                        return JsonResponse(
                            {'status': "Only " + str(product_check.quantity) + " of this product is available"})
            else:
                return JsonResponse({'status': "Something went wrong"})
        else:
            return JsonResponse({'status': "Login to continue"})
    return redirect('home')


@login_required(login_url='login')
def viewcart(request):
    cart = models.Cart.objects.filter(user=request.user)
    context = {'cart': cart}
    return render(request, 'shop/cart.html', context)


@login_required(login_url='login')
def update_cart(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        if models.Cart.objects.filter(user=request.user, product_id=prod_id):
            product = models.Product.objects.get(id=prod_id)
            product_qty = int(request.POST.get('product_qty'))
            print(product_qty)
            if product.quantity < product_qty:
                return JsonResponse({'status': f'Only {product.quantity} of this product is available'})
            cart = models.Cart.objects.get(product_id=prod_id, user=request.user)
            cart.product_qty = product_qty
            cart.save()
            print("product quantity saved")
            print(cart.product_qty)
            return JsonResponse({'status': 'Item quantity updated'})
    return redirect('shop')


@login_required(login_url='login')
def delete_cart_item(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        if models.Cart.objects.filter(user=request.user, product_id=prod_id):
            cart_item = models.Cart.objects.get(product_id=prod_id, user=request.user)
            cart_item.delete()
        return JsonResponse({'status': 'Item removed from cart'})
    return redirect('cart')


@login_required(login_url='login')
def checkout(request):
    if request.method == 'POST':
        print("posted")
        form = forms.OrderDetailsForm(request.POST)
        user = models.CustomUser.objects.filter(id=request.user.id).first()
        if form.is_valid():
            new_order_items = models.Cart.objects.filter(user=request.user)
            cart = models.Cart.objects.filter(user=request.user)
            cart_total_price = 0
            for item in cart:
                cart_total_price += item.product.selling_price * item.product_qty
            print(cart_total_price)
            print(user.wallet)
            if user.wallet == 0 or user.wallet is None or cart_total_price > user.wallet:
                messages.info(request, "Not enough wallet balance")
                return redirect('checkout')
            order_form = form.save(commit=False)
            order_form.payment_mode = "Wallet"
            ref = 'BP' + str(random.randint(11111111, 99999999))
            while models.Payment.objects.filter(reference=ref) is None:
                ref = 'BP' + str(random.randint(11111111, 99999999))
            current_user = models.CustomUser.objects.filter(id=request.user.id).first()
            order_form.total_price = cart_total_price
            order_form.user = current_user
            order_form.tracking_number = ref
            order_form.save()

            for item in new_order_items:
                models.OrderItem.objects.create(
                    order=order_form,
                    product=item.product,
                    tracking_number=order_form.tracking_number,
                    price=item.product.selling_price,
                    quantity=item.product_qty
                )
                order_product = models.Product.objects.filter(id=item.product_id).first()
                order_product.quantity -= item.product_qty
                order_product.save()

            models.Cart.objects.filter(user=request.user).delete()

            user.wallet -= cart_total_price
            user.save()

            sms_headers = {
                'Authorization': 'Bearer 1334|wroIm5YnQD6hlZzd8POtLDXxl4vQodCZNorATYGX',
                'Content-Type': 'application/json'
            }

            sms_url = 'https://webapp.usmsgh.com/api/sms/send'
            sms_message = f"Order Placed Successfully\nYour order with order number {order_form.tracking_number} has been received and is being processed.\nYou will receive a message when your order is Out for Delivery.\nThank you for shopping with BestPlug"

            sms_body = {
                'recipient': f"233{order_form.phone}",
                'sender_id': 'GEO_AT',
                'message': sms_message
            }
            try:
                response1 = requests.get(
                    f"https://sms.arkesel.com/sms/api?action=send-sms&api_key=UnBzemdvanJyUGxhTlJzaVVQaHk&to=0{order_form.phone}&from=GEOS_AT&sms={sms_message}")
                print(response1.text)
            except:
                print("Could not send sms message")

            messages.success(request, "Your order has been placed")
            return redirect('cart')
        else:
            messages.error(request, "Invalid Form Submission")
            return redirect('checkout')
    raw_cart = models.Cart.objects.filter(user=request.user)
    for item in raw_cart:
        print(item.product_qty)
        print(item.product.quantity)
        if item.product_qty > item.product.quantity:
            messages.info(request, f"Only {item.product.quantity} {item.product}(s) are left")
            return redirect('cart')
        elif item.product.quantity == 0:
            messages.info(request, f"{item.product} is out of stock")
            return redirect('cart')
    cart_items = models.Cart.objects.filter(user=request.user)
    total_price = 0
    for item in cart_items:
        total_price += item.product.selling_price * item.product_qty

    total_price_paystack = total_price * 100

    ref = 'BP' + str(random.randint(11111111, 99999999))
    while models.Payment.objects.filter(reference=ref) is None:
        ref = 'BP' + str(random.randint(11111111, 99999999))
    form = forms.OrderDetailsForm(
        initial={
            'full_name': f"{request.user.first_name} {request.user.last_name}",
            'email': request.user.email,
            'phone_number': request.user.phone
        }
    )
    user = models.CustomUser.objects.filter(id=request.user.id).first()
    email = user.email
    db_user_id = request.user.id
    context = {'cart_items': cart_items, 'id': db_user_id, 'total_price': total_price, 'amount': total_price_paystack,
               'ref': ref, 'email': email, 'form': form, 'wallet': user.wallet}
    return render(request, 'shop/checkout.html', context)


@login_required(login_url='login')
def orders(request):
    all_orders = models.Order.objects.filter(user=request.user).order_by('-created_at')
    context = {'orders': all_orders}
    return render(request, 'shop/order-page.html', context)


@login_required(login_url='login')
def view_order(request, t_no):
    if request.user.is_superuser:
        order = models.Order.objects.filter(tracking_number=t_no).first()
    else:
        order = models.Order.objects.filter(tracking_number=t_no).filter(user=request.user).first()
    order_items = models.OrderItem.objects.filter(order=order)
    context = {'order_items': order_items, 'order': order}
    return render(request, 'shop/view_order.html', context)


@login_required(login_url='login')
def admin_orders(request):
    if request.user.is_superuser or request.user.is_staff:
        all_orders = models.Order.objects.all().order_by('-created_at')
        context = {'orders': all_orders, 'admin': 'Yes'}
        return render(request, 'shop/order-page.html', context)
    else:
        messages.error(request, "Access Denied")
        return redirect('shop')


def product_list_ajax(request):
    products = models.Product.objects.filter().values_list('name', flat=True)
    product_list = list(products)

    return JsonResponse({'products': product_list}, safe=False)


def search_product(request):
    if request.method == 'POST':
        product_searched = request.POST.get('prod_search')
        if product_searched == "":
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            product = models.Product.objects.filter(name__contains=product_searched).first()

            if product:
                return redirect(product.category.name + '/' + product.name + '/details')
            else:
                messages.info(request, "No product matched your search")
                return redirect(request.META.get('HTTP_REFERER'))
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def change_order_status(request, t_no, stat):
    order = models.Order.objects.filter(tracking_number=t_no).first()
    if request.user.is_superuser:
        if stat == "out":
            order.status = "Out for Delivery"
            order.save()
            sms_headers = {
                'Authorization': 'Bearer 1334|wroIm5YnQD6hlZzd8POtLDXxl4vQodCZNorATYGX',
                'Content-Type': 'application/json'
            }

            sms_url = 'https://webapp.usmsgh.com/api/sms/send'
            sms_message = f"Hello {order.full_name},\nYour Order with tracking number {t_no} is out for delivery. You will receive a call from our delivery contact soon. Thank You"

            sms_body = {
                'recipient': f"233{order.phone}",
                'sender_id': 'GEO_AT',
                'message': sms_message
            }
            try:
                response1 = requests.get(
                    f"https://sms.arkesel.com/sms/api?action=send-sms&api_key=UnBzemdvanJyUGxhTlJzaVVQaHk&to=0{order.phone}&from= GEO_AT&sms={sms_message}")
                print(response1.text)
            except:
                print("Could not send sms message")
        elif stat == "Completed":
            order.status = "Completed"
            order.save()
            sms_headers = {
                'Authorization': 'Bearer 1334|wroIm5YnQD6hlZzd8POtLDXxl4vQodCZNorATYGX',
                'Content-Type': 'application/json'
            }

            sms_url = 'https://webapp.usmsgh.com/api/sms/send'
            sms_message = f"Hello {order.full_name},\nYour Order with tracking number {t_no} has been delivered successfully. Thank you for your patronage. Keep Shopping!"

            sms_body = {
                'recipient': f"233{order.phone}",
                'sender_id': 'GEO_AT',
                'message': sms_message
            }
            try:
                response = requests.request('POST', url=sms_url, params=sms_body, headers=sms_headers)
                print(response.text)
            except:
                print("Could not send sms message")
        elif stat == "Canceled":
            order.status = "Canceled"
            order.save()
            sms_headers = {
                'Authorization': 'Bearer 1334|wroIm5YnQD6hlZzd8POtLDXxl4vQodCZNorATYGX',
                'Content-Type': 'application/json'
            }

            sms_url = 'https://webapp.usmsgh.com/api/sms/send'
            sms_message = f"Hello {order.full_name},\nYour Order with tracking number {t_no} has been canceled due to some reasons. Thank you for your patronage. Keep Shopping!"

            sms_body = {
                'recipient': f"233{order.phone}",
                'sender_id': 'GEO_AT',
                'message': sms_message
            }
            try:
                response1 = requests.get(
                    f"https://sms.arkesel.com/sms/api?action=send-sms&api_key=UnBzemdvanJyUGxhTlJzaVVQaHk&to=0{order.phone}&from= GEO_AT&sms={sms_message}")
                print(response1.text)
            except:
                print("Could not send sms message")
        messages.success(request, "Order Status Changed")
        return redirect('view_order', t_no=t_no)
    else:
        messages.error(request, "Access Denied")
        return redirect('view_order', t_no=t_no)
