from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime

from .models import *
from . utils import cookieCart, cartData, guestOrder

# Create your views here.

def store(request):
    data = cookieCart(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
        
    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/checkout.html', context)

def cart(request):
    data = cookieCart(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
        
    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/checkout.html', context)

def checkout(request):
    data = cookieCart(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
        
    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId', productId)


    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def face(request):
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']

    products = Product.objects.filter(category='face')
    context = {'products': products}
    return render(request, 'store/face.html', context)

def lip(request):
    products = Product.objects.filter(category='lip')
    context = {'products': products}
    return render(request, 'store/lip.html', context)

def eye(request):
    products = Product.objects.filter(category='eye')
    context = {'products': products}
    return render(request, 'store/eye.html', context)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order , created = Order.objects.get_or_create(customer=customer, complete=False)
        
    # total = float(data['from']['total'])
    # order.transaction_id = transaction_id

    # if total == order.get_cart_total:
    #     order.complete = True
    # order.save()

    # if order.shipping == True:
    #     ShippingAddress.objects.create(
    #         customer=customer,
    #         order=order,
    #         address=data['shipping']['address'],
    #         city=data['shipping']['city'],
    #         province=data['shipping']['province'],
    #         zipcode=data['shipping']['zipcode'],
    #     )

    else:
        customer, order = guestOrder(request, data)
        # print('User is not logged in')

        # print('COOKIES:', request.COOKIES)
        # name = data['form']['name']
        # email = data['form']['email']

        # cookieData = cookieCaty(request)
        # items = cookiedata['items']

        # customer, created = Customer.objects.get_or_create(
        #     email=email,
        # )
        # customer.name = name
        # customer.save()

        # order = Order.objects.create(
        #     customer=customer,
        #     complete=False,
        #     )
        
        # for item in items:
        #     product = Product.objects.get(id=item['product']['id'])

        #     orderItem = OrderItem.objects.create(
        #         product=products,
        #         order=order,
        #         quantity=item['quantity']
        #         )

    total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == float(order.get_cart_total):
            order.complete = True
        order.save()
    
    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            province=data['shipping']['province'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment complete!, safe=False')
