"""
URL configuration for NoteAlly project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from noteally_app.webservices import ws_info, ws_materials, ws_tutors, ws_rating, ws_test, ws_auth, ws_downloads, ws_posts, ws_user
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('info/', ws_info.handle, name="info"),
    path('populate/', ws_test.populate_db, name="populate"),
    path('login/', ws_auth.handle, name="login"),
    path('update_profile/', ws_auth.update_profile, name="update_profile"),
    path('materials/', ws_materials.handle, name="materials"),
    path('materials/<int:material_id>/', ws_materials.handle_id, name="materials_id"),
    path('tutors/', ws_tutors.handle, name="tutors"),
    path('tutors/<int:tutors_id>/', ws_tutors.handle_id, name="tutors_id"),
    path('downloads/', ws_downloads.handle, name="downloads"),
    path('downloads/<int:material_id>', ws_downloads.handle_id, name="downloads_id"),
    path('like/<int:material_id>', ws_rating.handle_like, name="like"),
    path('dislike/<int:material_id>', ws_rating.handle_dislike, name="dislike"),
    path('posts/', ws_posts.handle, name="posts"),
    path('posts/<int:user_id>', ws_posts.handle_user_id, name='posts_user_id'),
    path('posts/<int:material_id>', ws_posts.handle_id, name="posts_id"),
    path('unlock_premium/', ws_user.handle, name="unlock_premium"),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
