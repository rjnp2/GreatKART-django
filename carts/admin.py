from django.contrib import admin
from .models import Cart, CartItem

class CartAdmin(admin.ModelAdmin):

    list_display = ['cart_id','date_added']
    list_filter = ['cart_id','date_added']

class CartItemAdmin(admin.ModelAdmin):

    list_display = ['product_id','cart_id','quantity','is_active']
    list_filter = ['product_id','cart_id','quantity']


# Register your models here.
admin.site.register(Cart,CartAdmin)
admin.site.register(CartItem, CartItemAdmin)