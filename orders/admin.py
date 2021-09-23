from django.contrib import admin
from .models import Payment,Order,Order_Product

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['payment_id','user','payment_method','amount_paid','created_at']

class Order_ProductInline(admin.TabularInline):
    model = Order_Product
    readonly_fields =  ['payment','user','product','created_at','is_ordered', ]

    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['full_name','status','order_number','address','is_ordered','created_at']

    list_filter = ['status', 'is_ordered']

    search_fields = ['order_number','full_name']
    list_per_page = 20
    inlines = [Order_ProductInline]

class Order_ProductAdmin(admin.ModelAdmin):
    list_display = ['payment','user','product','created_at','is_ordered']



# Register your models here.
admin.site.register(Payment,PaymentAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(Order_Product,Order_ProductAdmin)