from django.urls import path
from .views import wishlist_view, wishlist_json, wishlist_del_json, wishlist_add_json

app_name = 'wishlist'

urlpatterns = [
    path('', wishlist_view, name='wishlist_view'),
    path('api/', wishlist_json, name='wishlist_json'),
    path('api/del/<str:id_product>/', wishlist_del_json, name='wishlist_del_json'),
    path('api/add/<str:id_product>/', wishlist_add_json, name='wishlist_add_json'),

]