from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.doctor_list, name='doctor_list'),
    path('book/<int:doctor_id>/', views.book_appointment, name='book_appointment'),
]


