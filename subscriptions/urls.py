from django.urls import path
from . import views

urlpatterns = [
    path('', views.subscription_list, name='subscription_list'),
    path('<int:pk>/checkout/', views.subscription_checkout, name='subscription_checkout'),
]
