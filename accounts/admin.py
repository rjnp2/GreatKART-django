from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

class AccountAdmin(UserAdmin):
    list_display = ['email','username', 'first_name','last_name','last_login',
                    'data_joined','is_active']
                    
    list_display_links = ('email','username')
    readonly_fields = ('last_login','data_joined')
    ordering = ('-data_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


# Register your models here.
admin.site.register(Account,AccountAdmin)