from django.urls import path
from . import views

urlpatterns = [
    # path('register/', views.registerUser, name="register"),
    # path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register_login/', views.register_or_login, name="register_or_login"),
    
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    
    path('face/', views.face, name="face"),
    path('lip/', views.lip, name="lip"),
    path('eye/', views.eye, name="eye"),
]