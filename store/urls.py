from django.urls import path
from .views import product_view, show_view, products_page_view, cart_view, cart_add_view, cart_del_view

urlpatterns = [
    path('product/', product_view),
    path('product/<slug:page>.html', products_page_view),
    path('product/<int:page>', products_page_view),
    path('cart/', cart_view),
    path('cart/add/<str:id_product>', cart_add_view),
    path('cart/del/<str:id_product>', cart_del_view),
    path('', show_view),
]
