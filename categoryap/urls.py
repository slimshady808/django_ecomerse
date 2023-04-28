from django.urls import path

from . import views

urlpatterns=[
    
    path('',views.cate_view,name='cate_view'),
    path('category/<slug:slug>/', views.category_item, name='category_item'),
    path('filter-data',views.filter_data,name='filter_data'),
    
]