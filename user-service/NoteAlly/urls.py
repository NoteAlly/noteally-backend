from django.urls import path
from django.conf import settings
from noteally_app.webservices import ws_user

urlpatterns = [
    path('update_profile/', ws_user.update_profile, name="update_profile"),
    path('unlock_premium/', ws_user.unlock_premium, name="unlock_premium"),
    path('subscribe/<int:user_id>/', ws_user.subscribe, name='subscribe'),
    path('unsubscribe/<int:user_id>/', ws_user.unsubscribe, name='unsubscribe'),
    path('get_subscriptions/', ws_user.get_subscriptions, name='get_subscriptions'), 
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
