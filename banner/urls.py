from django.urls import path

from . import views

urlpatterns=[
    path('',views.banner,name='banner'),

 
    
]


