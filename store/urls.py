from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('', views.storehome, name='storehome'),        # (1)
    path('aboutus', views.aboutus, name='aboutus'),     # (2)
    path('reviews', views.reviews, name='reviews'),     # (3)
    path('shop', views.shop, name='shop'),
    path('shop/<str:category>/', views.shop, name='shop'),
    path('product/<int:product_id>', views.product, name='product'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
]
urlpatterns += staticfiles_urlpatterns()