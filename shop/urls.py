from django.urls import path
from . import views


urlpatterns = [
      path('',views.home,name='home'),
      path('register/',views.register,name='register'),
      path('logout',views.logout_page,name='logout'),
      path('login/',views.login_page,name='login'),
      path('collection/',views.collections,name='collections'),
      path('category/<int:cat_id>', views.category_products, name='category_products'),
      path('product_view/<int:pro_id>',views.product_view,name='product_view'),
      path('cart/', views.cart_view, name='cart_view'),
      path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
      path('remove-from-cart/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
      path('checkout/', views.checkout, name='checkout'),

]

