from django.urls import path

from . import views

app_name = 'catalogue'

urlpatterns = [
  path('', views.all_products, name='catalogue_home'),  
  path('<slug:slug>/', views.product_detail, name='product_detail'),
  path('store/<slug:category_slug>/', views.category_list, name='category_list'),
]
