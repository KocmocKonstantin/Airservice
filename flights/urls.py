from django.urls import path
from airservice import settings
from . import views
from django.conf.urls.static import static

urlpatterns = [ 
     
    path('', views.flight_list, name='flight_list'),  
    path('upload/', views.ticket_upload, name='upload_ticket'),
    path('ticket/<int:pk>/', views.ticket_detail, name='ticket_detail'),
    path('oauth2callback/', views.oauth2callback, name='oauth2callback'),
    path('calendar_auth/', views.calendar_auth, name='calendar_auth'),
    path('oauth2callback/', views.oauth2callback, name='oauth2callback'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)