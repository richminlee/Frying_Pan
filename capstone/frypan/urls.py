from django.urls import path
from . import views

app_name = 'frypan'

urlpatterns = [
    path('', views.home, name='home'),
    path('checkout/', views.checkout, name='checkout'),
    path('about_us/', views.about_us, name='about_us'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('order_summary/', views.order_summary, name='order_summary'),
    path('product/<int:product_id>/', views.product, name='product'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('remove_single_from_cart/<int:product_id>/', views.remove_single_from_cart, name='remove_single_from_cart'),
]