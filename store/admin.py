from django.contrib import admin
from .models import Product,Variation, ReviewRating, ProductGallery
import admin_thumbnails

@admin_thumbnails.thumbnail('prod_images')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery

    extra = 1

@admin_thumbnails.thumbnail('prod_images')
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug': ('product_name',)}

    list_display = ['product_name','slug','price','category','modified_date','is_available']
    inlines = [ProductGalleryInline]


class VariationProductAdmin(admin.ModelAdmin):

    list_display = ['product','variation_category','variation_value','is_active']
    list_editable = ('is_active',)
    list_filter = ['product','variation_category','variation_value']

class ReviewRatingAdmin(admin.ModelAdmin):

    list_display = ['user','product','subject','review','rating']
    list_filter = ['user','product','review','rating']



# Register your models here.
admin.site.register(Product,ProductAdmin)
admin.site.register(Variation,VariationProductAdmin)
admin.site.register(ReviewRating,ReviewRatingAdmin)
admin.site.register(ProductGallery)