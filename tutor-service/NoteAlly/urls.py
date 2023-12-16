from django.urls import path
from django.conf import settings
from noteally_app.webservices import ws_tutors, ws_posts

urlpatterns = [
    path('', ws_tutors.handle, name="tutors"),
    path('<int:tutors_id>/', ws_tutors.handle_id, name="tutors_id"),
    path('posts/', ws_posts.handle, name="posts"),
    path('tutorposts/<int:user_id>/', ws_posts.handle_user_id, name="posts_user_id"),
    path('posts/<int:material_id>/', ws_posts.handle_id, name="posts_id")
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
