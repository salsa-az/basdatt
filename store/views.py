from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
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

# user session
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST

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
                messages.success(request, 'Account was created for ' + user)
                return render(request, 'store/register_login.html', {'just_registered': True})

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

    # After processing the checkout, clear the cart
    if request.method == 'POST':
        # Clear the cart
        request.session['cart'] = {}

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
    products = Product.objects.filter(category='face')
    context = {'products':products}
    return render(request, 'store/face.html', context)


def lip(request):
    products = Product.objects.filter(category='lip')
    context = {'products': products}
    return render(request, 'store/lip.html', context)

def eye(request):
    products = Product.objects.filter(category='eye')
    context = {'products': products}
    return render(request, 'store/eye.html', context)

@require_POST
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order , created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

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

        # Empty the cart
        cart = cart.objects.get(customer=customer)
        cart.items.clear()

        messages.success(request, 'Transaction complete!')
        return redirect('store')

    messages.error(request, 'There was a problem with your transaction.')
    return redirect('checkout')
# def product_detail(request, product_id):
#     product = Product.objects.get(id=product_id)
#     context = {
#         'product': product,
#     }
#     return render(request, 'product_detail.html', context)

@require_POST
def add_to_cart(request, id):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, id=id)

        if 'productId' not in request.session:
            # Update the cart
            request.session['productId'] = id
            request.session['productTitle'] = product.title

            messages.success(request, 'Successfully added to the cart')
        else:
            messages.error(request, 'Only 1 quantity can be added to the cart')

        return redirect(f'/product/{id}')
    else:
        messages.error(request, 'Please log in to add products to your cart.')
        return redirect('/login')
    
@require_POST
def remove_from_cart(request, userId, id):
    if request.user.is_authenticated and str(request.user.id) == userId:
        product = get_object_or_404(Product, id=id)
        if product.id in request.session:
            # Remove the product from the cart
            del request.session[product.id]
            del request.session[product.title]

            # Assuming user.cart is a list of product ids
            request.user.cart.remove(product.id)
            request.user.save()

            return redirect(f'/user/{userId}/cart')
        else:
            messages.error(request, 'Product not in cart')
            return redirect(f'/user/{userId}/cart')
    else:
        messages.error(request, 'Please log in to remove products from your cart.')
        return redirect('/login')
    
# @require_POST
# def empty_cart(request):
#     if request.method == 'POST':
#         # Empty the cart
#         if request.user.is_authenticated:
#             cart = Order.objects.get(customer=request.user.customer, complete=False)
#             cart.items.clear()
#         else:
#             request.session['cart'] = {}
#         return JsonResponse({'success': True})
#     else:
#         return JsonResponse({'success': False})