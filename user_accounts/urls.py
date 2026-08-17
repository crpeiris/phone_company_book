from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('login',views.login_user, name='login_user'), 
    path('register_user/', views.register_user, name='register_user'),
    path('logout/', views.logout_user, name='logout_user'),

]
urlpatterns += staticfiles_urlpatterns()