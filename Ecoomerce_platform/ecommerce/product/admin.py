from django.contrib import admin
from .models import Product,Category

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "description"]

admin.site.register(Product,ProductAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ["c_name","slug"]
    prepopulated_fields = {'slug': ('c_name',)}

admin.site.register(Category,CategoryAdmin)