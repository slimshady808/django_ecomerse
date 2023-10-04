
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
