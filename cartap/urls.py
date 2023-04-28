from django.urls import path

from . import views

urlpatterns=[
    
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('show_cart',views.show_cart,name='show_cart'),
    path('pluscart',views.plus_cart),
    path('minuscart',views.minus_cart),
    path('removecart',views.remove_cart),
    
]