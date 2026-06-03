from django.contrib.auth import views as auth_views
from django.urls import path

from . import storefront_views

urlpatterns = [
    path('', storefront_views.catalog_page, name='storefront_catalog'),
    path('products/<int:product_id>/', storefront_views.product_detail_page, name='storefront_product_detail'),
    path('cart/', storefront_views.cart_page, name='storefront_cart'),
    path('cart/add/<int:product_id>/', storefront_views.add_to_cart, name='storefront_add_to_cart'),
    path('cart/items/<int:item_id>/update/', storefront_views.update_cart_item, name='storefront_update_cart_item'),
    path('cart/items/<int:item_id>/remove/', storefront_views.remove_cart_item, name='storefront_remove_cart_item'),
    path('checkout/', storefront_views.checkout_page, name='storefront_checkout'),
    path('signup/', storefront_views.signup_page, name='storefront_signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='storefront_login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='storefront_catalog'), name='storefront_logout'),
]
