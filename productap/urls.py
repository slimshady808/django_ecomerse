from django.urls import path

from . import views

urlpatterns=[
    path('',views.home,name='home'),
    path('product_view',views.product_view,name='product_view'),
    path('products/<slug:slug>/', views.view_item, name='view_item'),
    path('check_out',views.check_out,name='check_out'),
    path('check_out1',views.check_out1,name='check_out1'),
    path('check_out_add_address',views.check_out_add_address,name='check_out_add_address')
] 
