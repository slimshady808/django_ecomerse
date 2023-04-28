from django.urls import path

from . import views

urlpatterns=[
    path('',views.add_whishlist,name='add_whishlist'),
    path('view_whishlist',views.view_whishlist,name='view_whishlist'),
    path('delete_whishlist/<int:product_id>',views.delete_whishlist,name='delete_whishlist'),
    
] 