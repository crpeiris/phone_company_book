from django.urls import path
from . import views

urlpatterns = [
    path('', views.storehome, name='storehome'),        # (1)
    path('aboutus', views.aboutus, name='aboutus'),     # (2)
    path('reviews', views.reviews, name='reviews'),     # (3)
]
