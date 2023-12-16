from django.urls import path
from django.conf import settings
from noteally_app.webservices import ws_info

urlpatterns = [
    path('', ws_info.handle, name="info")
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
