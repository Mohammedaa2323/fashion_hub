from django.contrib import admin
from store.models import Category,Size,Product,OrderItems,Order,Tags

# Register your models here.

admin.site.register(Category)
admin.site.register(Size)
admin.site.register(Product)
admin.site.register(OrderItems)
admin.site.register(Order)
admin.site.register(Tags)