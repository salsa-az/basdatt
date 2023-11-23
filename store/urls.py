from django.urls import path
from . import views

urlpatterns = [
   path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('face/', views.face, name="face"),
	path('lip/', views.lip, name="lip"),
	path('eye/', views.eye, name="eye")
]