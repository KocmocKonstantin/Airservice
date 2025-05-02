from django.urls import path

from . import views

urlpatterns = [
    path('', views.flight_list, name='flight_list'),
    path('upload/', views.ticket_upload, name='upload_ticket'),
    path('ticket/<int:pk>/', views.ticket_detail, name='ticket_detail'),
    path('calendar_auth/', views.calendar_auth, name='calendar_auth'),
    path('oauth2callback/', views.oauth2callback, name='oauth2callback'),
]