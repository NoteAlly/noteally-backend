from django.contrib import admin
from django.urls import path
from django.conf import settings
from noteally_app.webservices import ws_info, ws_materials, ws_tutors, ws_rating, ws_test, ws_auth, ws_downloads, ws_posts, ws_user

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
    path('downloads/<int:material_id>/', ws_downloads.handle_id, name="downloads_id"),
    path('like/<int:material_id>/', ws_rating.handle_like, name="like"),
    path('dislike/<int:material_id>/', ws_rating.handle_dislike, name="dislike"),
    path('posts/', ws_posts.handle, name="posts"),
    path('tutorposts/<int:user_id>/', ws_posts.handle_user_id, name="posts_user_id"),
    path('posts/<int:material_id>/', ws_posts.handle_id, name="posts_id"),
    path('unlock_premium/', ws_user.handle, name="unlock_premium"),
    path('subscribe/<int:user_id>/', ws_user.subscribe, name='subscribe'),
    path('unsubscribe/<int:user_id>/', ws_user.unsubscribe, name='unsubscribe'),
    path('get_subscriptions/', ws_user.get_subscriptions, name='get_subscriptions'), 
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
