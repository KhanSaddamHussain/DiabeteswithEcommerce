# from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerPage, name="registerPage"),
    path('login/', views.loginPage, name="loginPage"),
    path('logout/', views.logout, name="logout"),
    path('predict/', views.predict, name="predict"),
    path('predict/result', views.result, name="result"),
    path('', views.home, name="home"),
    path('store/', views.store, name="store"),
    path('store/<slug:slug>', views.productdetailview, name="productdetailview"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),
    
    path('update_item/', views.updateItem, name="update_item"),
    # path('checkout/', views.shippingData, name="shippingData"),
    path('thankyou/', views.thankYou, name="thankyou"),
    path('report/', views.report, name="report"),
    
    
]
