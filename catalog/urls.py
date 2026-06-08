from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('masters/<int:pk>/', views.master_detail, name='master_detail'),
    path('services/', views.service_list, name='service_list'),
    path('portfolio/', views.portfolio_manage, name='portfolio_manage'),
    path('portfolio/<int:pk>/delete/', views.portfolio_delete, name='portfolio_delete'),
]
