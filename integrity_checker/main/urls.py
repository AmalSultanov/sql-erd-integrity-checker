from django.urls import path

from integrity_checker.main import views


app_name = 'main'

urlpatterns = [
    path('', views.homepage, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]
