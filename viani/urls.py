"""viani URL Configuration"""

from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.home),
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('shop/', include('shop.urls')),
    path('personnel/', include('personnel.urls')),
]

urlpatterns += [
    path('social/', include('social_django.urls', namespace='social')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += path('__debug__/', include(debug_toolbar.urls)),
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
