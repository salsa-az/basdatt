from django.urls import path
from . import views
from .views import remove_from_cart

urlpatterns = [
    path('logout/', views.logoutUser, name="logout"),
    path('register_login/', views.register_or_login, name="register_or_login"),
    
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('user/<str:userId>/cart/remove/<int:id>/', remove_from_cart, name='remove_from_cart'),
    # path('empty_cart/', views.empty_cart, name='empty_cart'),
    
    path('face/', views.face, name="face"),
    path('lip/', views.lip, name="lip"),
    path('eye/', views.eye, name="eye"),
]