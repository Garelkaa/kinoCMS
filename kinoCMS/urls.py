import debug_toolbar
from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include
from . import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', include(('customadmin.urls', 'customadmin'), namespace='adminlte')),
    path('', include(('main.urls', 'main'), namespace='main')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('celery-progress/', include('celery_progress.urls')),
]

urlpatterns += i18n_patterns(
    path('admin/', include(('customadmin.urls', 'customadmin'))),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
