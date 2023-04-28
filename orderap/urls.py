from django.urls import path

from . import views

urlpatterns=[
   path('order/<int:order_id>/', views.order_detail, name='order_detail'),
  
   path('create_order',views.create_order,name='create_order'),
    path('cancel-order/<int:order_id>/', views.cancel_order, name='cancel_order'),
   

]