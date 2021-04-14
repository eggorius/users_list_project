from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('login', views.login_view, name='login'),
    path('registration', views.registration_view, name='registration'),
    path('logout', views.logout_user, name='logout'),
]
