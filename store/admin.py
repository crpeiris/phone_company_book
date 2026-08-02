from django.contrib import admin
from .models import Category, Profile, Product,Order,OrderProduct

# Register your models here.
admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderProduct)
