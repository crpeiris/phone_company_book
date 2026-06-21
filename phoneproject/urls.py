from django.contrib import admin
from django.urls import path, include
from store import views as storeviews


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', storeviews.storehome),  # This handles the root URL
    path('store/', include('store.urls')),
]
