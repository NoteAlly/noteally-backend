from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
import requests
from noteally_app.models import User


def get_cognito_user(access_token):
    cognito_domain = settings.COGNITO_DOMAIN
    url = f'https://{cognito_domain}/oauth2/userInfo'
    headers = {'Authorization': f'Bearer {access_token}'}

    response = requests.get(url, headers=headers)
    response_data = response.json()

    if response.status_code == 200:
        cognito_user = {
            'sub': response_data['sub'],
            'email_verified': response_data['email_verified'],
            'first_name': response_data['given_name'],
            'last_name': response_data['family_name'],
            'email': response_data['email'],
            'username': response_data['username']
        }
        return cognito_user
    return None


def cognito_login_required(func):
    def wrapper(request, *args, **kwargs):
        # Request contains 'Authorization' and 'User-id' headers
        
        # Ignore decorator on test environment
        if settings.SETTINGS_MODULE == 'NoteAlly.test_settings':
            return func(request, *args, **kwargs)
        
        # Check if the user exists in the database
        user_id = request.headers['User-id']
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # validate user with cognito user pool
        user_access_token = request.headers['Authorization'].split(" ")[1]
        cognito_user = get_cognito_user(user_access_token)

        if cognito_user is None or cognito_user['sub'] != user.sub:
            return Response({'message': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        return func(request, *args, **kwargs)
        
    return wrapper
