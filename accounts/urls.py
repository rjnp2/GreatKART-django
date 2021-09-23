from django.urls import path
from .views import register, resetpassword,login, logout,activate,dashboard,changepassword
from .views import my_orders,forgetpassword,resetpassword_validate,edit_profile,order_details

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('forgetpassword/', forgetpassword, name='forgetpassword'),
    path('resetpassword/', resetpassword, name='resetpassword'),
    path('', dashboard, name='dashboard'),

    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('resetpassword_validate/<uidb64>/<token>', resetpassword_validate, name='resetpassword_validate'),
    
    path('my_orders/', my_orders, name='my_orders'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('changepassword/', changepassword, name='changepassword'),
    path('order_details/<int:order_id>', order_details, name='order_details'),

]