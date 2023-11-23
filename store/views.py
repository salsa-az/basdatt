from django.shortcuts import render

# Create your views here.

def store(request):
    context = {}
    return render(request, 'store/store.html', context)

def cart(request):
    context = {}
    return render(request, 'store/cart.html', context)

def checkout(request):
    context = {}
    return render(request, 'store/checkout.html', context)

def face(request):
    context = {}
    return render(request, 'store/face.html', context)

def lip(request):
    context = {}
    return render(request, 'store/lip.html', context)

def eye(request):
    context = {}
    return render(request, 'store/eye.html', context)
