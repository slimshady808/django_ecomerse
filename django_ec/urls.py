"""django_ec URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from django.urls import *


urlpatterns = [
    

    # path('jet/dashboard/',include('jet.dashboard.urls','jet-dashboard')),
    # path('jet/',include('jet.urls')),
  
    path('admin/', admin.site.urls),
    path('admin1/',include('admin_panel.urls')),
    path('user/',include('userap.urls')),
    path('',include('productap.urls')),
    path('category/',include('categoryap.urls')),
    path('cart/',include('cartap.urls')),
    path('order/',include('orderap.urls')),
    path('whishlist/',include('whishlist.urls')),
    path('banner/',include('banner.urls')),
     path('sales/',include('sales.urls')),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
