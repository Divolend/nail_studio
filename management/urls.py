from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='mng_dashboard'),

    # Услуги
    path('services/', views.service_list, name='mng_service_list'),
    path('services/new/', views.service_create, name='mng_service_create'),
    path('services/<int:pk>/edit/', views.service_edit, name='mng_service_edit'),
    path('services/<int:pk>/delete/', views.service_delete, name='mng_service_delete'),

    # Мастера
    path('masters/', views.master_list, name='mng_master_list'),
    path('masters/new/', views.master_create, name='mng_master_create'),
    path('masters/<int:pk>/delete/', views.master_delete, name='mng_master_delete'),

    # Типы абонементов
    path('subscription-types/', views.subscription_type_list, name='mng_subscription_type_list'),
    path('subscription-types/new/', views.subscription_type_create, name='mng_subscription_type_create'),
    path('subscription-types/<int:pk>/edit/', views.subscription_type_edit, name='mng_subscription_type_edit'),
    path('subscription-types/<int:pk>/delete/', views.subscription_type_delete, name='mng_subscription_type_delete'),
]
