from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('account/', views.account, name='account'),
    path('account/change-password/', views.password_change_required, name='password_change_required'),
    path('account/master/edit/', views.edit_master_profile, name='edit_master_profile'),
]
