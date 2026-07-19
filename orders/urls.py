from django.urls import path

from . import views

urlpatterns=[

path('cart/',views.cart,name='cart'),

path('checkout/',views.checkout,name='checkout'),

path('payment/',views.payment,name='payment'),

path('success/',views.success,name='success'),

path('my-orders/',views.my_orders,name='my_orders'),

]