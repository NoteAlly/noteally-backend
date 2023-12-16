from django.urls import path
from noteally_app.webservices import ws_auth

urlpatterns = [
    path('login/', ws_auth.handle, name="login")
]
