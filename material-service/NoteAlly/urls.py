from django.contrib import admin
from django.urls import path
from django.conf import settings
from noteally_app.webservices import ws_materials, ws_rating, ws_downloads

urlpatterns = [
    path('', ws_materials.handle, name="materials"),
    path('<int:material_id>/', ws_materials.handle_id, name="materials_id"),
    path('downloads/', ws_downloads.handle, name="downloads"),
    path('downloads/<int:material_id>/', ws_downloads.handle_id, name="downloads_id"),
    path('like/<int:material_id>/', ws_rating.handle_like, name="like"),
    path('dislike/<int:material_id>/', ws_rating.handle_dislike, name="dislike")
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
