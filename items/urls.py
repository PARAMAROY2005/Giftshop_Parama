from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path('gift/<int:id>/', views.gift_detail, name='gift_detail'),

    path('wishlist/', views.wishlist, name='wishlist'),

    path('cart/', views.cart, name='cart'),

    path('wishlist/add/<int:id>/', views.add_to_wishlist, name='add_to_wishlist'),

    path('cart/add/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/increase/<int:id>/', views.increase_quantity, name='increase_quantity'),

path('cart/decrease/<int:id>/', views.decrease_quantity, name='decrease_quantity'),

path('cart/delete/<int:id>/', views.delete_cart_item, name='delete_cart_item'),
path(
    'wishlist/delete/<int:id>/',
    views.delete_wishlist,
    name='delete_wishlist'
),

path(
    'wishlist/move/<int:id>/',
    views.move_to_cart,
    name='move_to_cart'
),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('faq-returns/', views.faq_returns, name='faq_returns'),
]