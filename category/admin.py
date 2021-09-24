from django.contrib import admin
from .models import Category
import admin_thumbnails

@admin_thumbnails.thumbnail('cat_images')
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug': ('category_name',)}

    list_display = ['category_name','slug']

# Register your models here.
admin.site.register(Category,CategoryAdmin)