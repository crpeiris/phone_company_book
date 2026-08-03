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
]
urlpatterns += staticfiles_urlpatterns()