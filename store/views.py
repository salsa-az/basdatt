from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
import json
import datetime

from .models import *
from . utils import cookieCart, cartData, guestOrder

# for userCreation
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import CreateUserForm, LoginForm
from django.contrib import messages

# authenticate user
from django.contrib.auth import authenticate, login, logout

# Create your views here

@csrf_protect
def register_or_login(request):
    register_form = CreateUserForm()
    login_form = LoginForm()  
    
    if request.method == "POST":
        if "register" in request.POST:
            register_form = CreateUserForm(request.POST)
            if register_form.is_valid():
                register_form.save()
                user = register_form.cleaned_data.get('username')
                email = register_form.cleaned_data.get('email')
                # Additional actions for registration if needed
                messages.success(request, 'Account was created for ' + user)
                return redirect('store')  # Redirect to store after successful registration
        
        elif "login" in request.POST:
            login_form = LoginForm(request.POST)
            if request.method == "POST":
                username = request.POST.get('username')
                password = request.POST.get('password')
                
                user = authenticate(request, username=username, password=password)
                if user:
                    login(request, user)
                    return redirect('store')  # Redirect to store after successful login
                else:
                    messages.info(request, 'Incorrect username or password')

    context = {'register_form': register_form, 'login_form': login_form}
    return render(request, 'store/register_login.html', context)

# def registerUser(request):
#     form = CreateUserForm()

#     if request.method=="POST":
#         form = CreateUserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             user = form.cleaned_data.get('username')
#             messages.success(request, 'Account was created for ' + form.cleaned_data.get('username'))
#             email = form.cleaned_data.get('email')

#             Customer.objects.create(username=User.objects.get(username=user), email=email)
#             return redirect('register')

#     context={'form':form}
#     return render(request, 'store/register.html',context)

# def loginUser(request):
#     if request.method =="POST":
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = authenticate(request, username=username, password=password)
#         if user:
#             login(request, user)
#             return redirect('store')
#         else:
#             messages.info(request, 'Incorrect username or password')
#     context={}
#     return render(request, 'store/login.html',context)

def logoutUser(request):
    logout(request)
    return redirect('store') 


def store(request):
    
    context = {}
    return render(request, 'store/store.html', context)

def cart(request):
    data = cookieCart(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
        
    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/cart.html', context)

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
    data = cartData(request)
    
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    
    products = Product.objects.filter(category='face')
    context = {'products':products, 'cartItems':cartItems}
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

        # cookieData = cookieCart(request)
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

    return JsonResponse('Payment complete!', safe=False)

# def product_detail(request, product_id):
#     product = Product.objects.get(id=product_id)
#     context = {
#         'product': product,
#     }
#     return render(request, 'product_detail.html', context)