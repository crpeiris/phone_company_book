from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('', views.storehome, name='storehome'),        # (1)
    path('aboutus', views.aboutus, name='aboutus'),     # (2)
    path('reviews', views.reviews, name='reviews'),     # (3)
]
urlpatterns += staticfiles_urlpatterns()