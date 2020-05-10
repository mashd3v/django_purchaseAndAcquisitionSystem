from django.urls import path
from django.contrib.auth import views as authViews
from bases.views import Home, HomeNoPermission

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('login/', authViews.LoginView.as_view(template_name='bases/login.html'),
        name='login'),
    path('logout/', authViews.LogoutView.as_view(template_name='bases/login.html'),
        name='logout'),
    path('noPermission/', HomeNoPermission.as_view(), name='noPermission')
]