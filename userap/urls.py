from django.urls import path

from . import views

urlpatterns=[
    
    path('log_in',views.log_in,name='log_in'),
    path('sign_up',views.sign_up,name='sign_up'),
    path('sign_out',views.sign_out,name='sign_out'),
    path('user_dashboard',views.user_dashboard,name='user_dashboard'),
    path('activate/<uidb64>/<token>',views.ActivateAccountView.as_view(), name='activate'),
    path('user_profile',views.user_profile,name='user_profile'),
    path('edit_user_profile',views.edit_user_profile,name='edit_user_profile'),
    path('request-reset-email',views.RequestResetEmailView.as_view(),name='request-reset-email'),
    path('set-new-password/uidb64/<uidb64>/token/<token>',views.SetNewPasswordView.as_view(),name='set-new-password'),
    path('change_password',views.change_password,name='change_password'),
    path('user_address',views.user_address,name='user_address'),
    path('add_address',views.add_address,name='add_address'),
    path('address/<int:address_id>/delete/', views.delete_address, name='address_delete'),
    path('order_history',views.order_history,name='order_history'),
    path('addresses/<int:address_id>/edit/', views.edit_address, name='edit_address'),
]