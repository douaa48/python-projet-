from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('frontend.urls')),
    path('reservations/', include('reservations.urls')),
    path('voyages/', include('voyages.urls')),
    path('payments/', include('payments.urls')),
    path('', include('users.urls')),
    path('notifications/', include('notifications.urls')),
    path('documents/', include('documents.urls')),
    path('dashboard/', include('dashboard.urls')),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)