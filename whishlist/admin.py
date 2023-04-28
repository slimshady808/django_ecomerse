from django.contrib import admin
from .models import Whishlist
# Register your models here.



# admin.site.register(Whishlist)


from import_export.admin import ExportMixin

class WhishlistAdmin(ExportMixin, admin.ModelAdmin):
    pass

admin.site.register(Whishlist,WhishlistAdmin)
