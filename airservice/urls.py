from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from flights import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('flights/', include('flights.urls')),  
    path('oauth2callback/', views.oauth2callback), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)