from django.contrib import admin
from .models import Product



class ProductAdmin(admin.ModelAdmin):
    list_display= ('product_name', 'price' , 'stock', 'category', 'is_available')
    filter_horizontal=()
    list_filter=()
    fieldsets = ()
    

admin.site.register(Product,ProductAdmin)





