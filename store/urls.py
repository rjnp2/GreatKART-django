from django.urls import path, include
from .views import store,product_detail,search

urlpatterns = [
    path('', store, name='store'),
    path('category/<slug:category_slug>/', store, name='product_by_categories'),
    path('category/<slug:category_slug>/<slug:product_slug>/', product_detail, name='product_detail'),
    path('search/', search, name='search'),
]