from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from apps.dashboard import views as dashboard_views

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('', dashboard_views.landing, name='home'),
    path('accounts/', include('apps.accounts.urls')),
    path('gigs/', include('apps.marketplace.urls')),
    path('projects/', include('apps.collaboration.urls')),
    path('communication/', include('apps.communication.urls')),
    path('engagement/', include('apps.engagement.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
