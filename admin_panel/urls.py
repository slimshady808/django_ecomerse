from django.urls import path

from . import views

urlpatterns=[
    path('admin',views.admin_page,name='admin_page'),
    path('',views.admin_login,name='admin_login'),
    path('add_product',views.add_product,name='add_product'),
    
]


"""path('delete_user/<int:user_id>/',views.delete_user,name='delete_user'),
    path('<int:id>/',views.edit_user,name='update_user'),
    path('create_user',views.create_user,name='create_user'),"""
   