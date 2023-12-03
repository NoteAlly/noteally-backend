from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.conf import settings
from noteally_app.models import User
from noteally_app.serializers import UserSessionSerializer
from noteally_app.decorators import get_cognito_user


def authenticate(request):
    auth_data = request.data
    access_token = auth_data['access_token']
    cognito_user = get_cognito_user(access_token)

    if cognito_user is None:
        return Response({'error': 'Invalid access token or user does not exist'}, status=400)
    
    user_in_db = User.objects.filter(sub=cognito_user['sub']).count() == 1
    registered = True

    if not user_in_db:
        registered = False
        user = User(
            sub=cognito_user['sub'],
            first_name=cognito_user['first_name'],
            last_name=cognito_user['last_name'],
            email=cognito_user['email'],
        )
        user.save()

    user = User.objects.get(sub=cognito_user['sub'])
    user_data = {
        'id': user.id,
        'sub': user.sub,
        'id_token': access_token,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'premium': user.premium,
        'karma_score': user.karma_score,
        'tutoring_services': user.tutoring_services,
        'profile_picture': user.profile_picture,
        'study_areas': user.study_areas,
        'description': user.description,
        'registered': registered
    }
    session_serializer = UserSessionSerializer(user_data)
    return Response(session_serializer.data, status=200)


@api_view(['POST'])
def handle(request):
    if request.method == 'POST':
        return authenticate(request)
    
@api_view(['POST'])
def update_profile(request):
    new_data = request.data
    user_id = new_data['id']
    id_token = new_data['id']
    user_in_db = User.objects.filter(id=user_id).count() == 1
    registered = True

    if not user_in_db:
        return Response({'error': 'User not in database'}, status=400)

    # Update User Info with new data
    user = User.objects.get(id=user_id)
    user.description = new_data["description"]
    user.study_areas.set(new_data["study_areas"])
    
    if 'profile_picture' in request.FILES:
        profile_picture = request.FILES['profile_picture']
        user.profile_picture_name = profile_picture.name
        user.profile_pic_size = profile_picture.size
        user.profile_picture = profile_picture
        
    user.save()

    # Success Response
    user_data = {
        'id': user.id,
        'sub': user.sub,
        'id_token': id_token,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'premium': user.premium,
        'karma_score': user.karma_score,
        'tutoring_services': user.tutoring_services,
        'profile_picture': user.profile_picture.name,
        'study_areas': user.study_areas,
        'description': user.description,
        'registered': registered
    }

    session_serializer = UserSessionSerializer(user_data)
    return Response(session_serializer.data, status=200)
