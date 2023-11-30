from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from noteally_app.CustomPagination import CustomPagination
from noteally_app.serializers import UserSerializer, FollowerSerializer
from noteally_app.models import User, Follower
from noteally_app.webservices.ws_auth import get_cognito_user


def unlock_premium(request):
    # Get user from database or return error if not found
    try:
        user = User.objects.get(id=request.headers['User-id'])
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)
    except KeyError:
        return Response({'error': 'User-id header not found'}, status=status.HTTP_400_BAD_REQUEST)
    
    if user.premium:
        return Response({'error': 'User is already premium'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Update user's premium status
    user.premium = True
    user.save()
    
    return Response({'user_id': user.id, 'message': 'Premium unlocked'}, status=status.HTTP_200_OK)

@api_view(['POST']) 
def subscribe(request, user_id): 
    try:
        user_to_follow = User.objects.get(id=user_id)
        user = User.objects.get(id=request.headers['user'])
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if user_to_follow == request.user:
        return Response({'error': 'Cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the user is already following
    if Follower.objects.filter(follower=user, following=user_to_follow).exists():
        return Response({'error': 'Already following this user'}, status=status.HTTP_400_BAD_REQUEST)

    # Create a new follower relationship
    Follower.objects.create(follower=user, following=user_to_follow)

    return Response({'message': 'Successfully subscribed'}, status=status.HTTP_201_CREATED)

@api_view(['GET']) 
def get_subscribers(request):
    user = User.objects.get(id=request.headers['user'])
    subscribers = user.followers.all() 
    print("\n\n")
    print(subscribers)
    print("\n\n")
    serializer = FollowerSerializer(subscribers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET']) 
def get_subscribed_to(request):
    user = User.objects.get(id=request.headers['user'])
    subscribers = user.followers_set.all() 
    print("\n\n")
    print(subscribers)
    print("\n\n")
    serializer = FollowerSerializer(subscribers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['POST'])
def handle(request):
    if request.method == 'POST':
        return unlock_premium(request)