from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, UserProfile
from django.utils.html import format_html
import admin_thumbnails

class AccountAdmin(UserAdmin):
    list_display = ['email','username', 'first_name','last_name','last_login',
                    'data_joined','is_active']
                    
    list_display_links = ('email','username')
    readonly_fields = ('last_login','data_joined')
    ordering = ('-data_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

@admin_thumbnails.thumbnail('profile_pics')
class UserProfileAdmin(admin.ModelAdmin):

    def thumbnail(self, object):
        return format_html('<img src="{}" width ="30" style="border-radius:50%;">'.format(object.profile_pics.url))

    thumbnail.short_description = 'Profile Pics'
    list_display = ['thumbnail','user', 'city','state','country']

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

# Register your models here.
admin.site.register(Account,AccountAdmin)
admin.site.register(UserProfile,UserProfileAdmin )