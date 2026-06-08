from django.urls import path
from . import views

urlpatterns = [
    # Клиент
    path('book/<int:master_pk>/', views.book_appointment, name='book_appointment'),
    path('appointment/<int:pk>/cancel/', views.cancel_appointment, name='cancel_appointment'),

    # Мастер
    path('schedule/', views.master_schedule, name='master_schedule'),
    path('slot/<int:pk>/delete/', views.slot_delete, name='slot_delete'),
    path('appointments/', views.master_appointments, name='master_appointments'),
    path('appointment/<int:pk>/complete/', views.complete_appointment, name='complete_appointment'),
]
