from django.urls import path
from .views import *
urlpatterns = [
    path('', ProductListView.as_view(), name='main'),
    path('more_products/', MoreProductView.as_view(), name='more'),
    path('product/<slug:slug>/  ', ProductDetailView.as_view(), name='product'),
    path('product_color/<str:color_code>/<str:category>/<str:modal>/', product_by_color, name='product_color'),
    path('category/<slug:slug>/', CategoryView.as_view(), name='category'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('add_favorite/<slug:slug>/', add_to_favorite_view, name='add_favorite'),
    path('my_favorite/', FavoriteListView.as_view(), name='my_favorite'),
    path('sales/', DiscountProduct.as_view(), name='sales'),
    path('add_product/<slug:slug>/<str:action>/', add_product_to_cart, name='add_product'),
    path('my_cart/', my_cart_view, name='my_cart'),
    path('delete/<int:order>/', delete_products_from_cart, name='delete'),
    path('change_language/<str:lang_code>/', change_language, name='change_language'),
    path('checkout/', checkout_view, name='checkout'),
    path('payment/', create_checkout_session, name='payment'),
    path('success/', success_payment, name='success'),
    path('search/', SearchResult.as_view(), name='search'),
    path('profile/', profile_view, name='profile'),
    path('change/', edit_account_profile_view, name='change'),
    path('edit_profile/', edit_profile_view, name='edit_profile'),
    path('edit_account/', edit_account_view, name='edit_account')

]