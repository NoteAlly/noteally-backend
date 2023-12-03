from rest_framework import status
from rest_framework.decorators import api_view
from noteally_app.decorators import cognito_login_required
from rest_framework.response import Response
from noteally_app.CustomPagination import CustomPagination
from noteally_app.serializers import SubsUserSerializer, FollowerSerializer
from noteally_app.models import User, Follower


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
@cognito_login_required
def subscribe(request, user_id): 
    try:
        user_to_follow = User.objects.get(id=user_id)
        user = User.objects.get(id=request.headers['User-id'])
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND) 

    # Check if the user is already following
    if Follower.objects.filter(follower=user, following=user_to_follow).exists():
        return Response({'error': 'Already following this user'}, status=status.HTTP_400_BAD_REQUEST)

    # Create a new follower relationship
    Follower.objects.create(follower=user, following=user_to_follow)

    return Response({'message': 'Successfully subscribed'}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@cognito_login_required 
def get_subscriptions(request):
    user = User.objects.get(id=request.headers['User-id'])
    users = user.followers.all()   
    
    # Ordering
    order_options = ["first_name", "-first_name", "last_name", "-last_name", "karma_score", "-karma_score"]

    if "order_by" in request.GET and request.GET["order_by"] in order_options:
        users = users.order_by(request.GET["order_by"])
    else:
        users = users.order_by('-karma_score', 'first_name')

    paginator = CustomPagination()  # Use your custom pagination class
    paginated_users = paginator.paginate_queryset(users, request)
    serializer = SubsUserSerializer(paginated_users, many=True)
    paginated_response = paginator.get_paginated_response(serializer.data)

    return Response(paginated_response.data, status=status.HTTP_200_OK)
    

@api_view(['POST'])
@cognito_login_required
def unsubscribe(request, user_id):
    user = User.objects.get(id=request.headers['User-id'])
    try:
        user_to_unsubscribe = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND) 

    # Check if the user is currently following
    try:
        follower_relation = Follower.objects.get(follower=user, following=user_to_unsubscribe)
    except Follower.DoesNotExist:
        return Response({'error': 'Not currently subscribed to this user'}, status=status.HTTP_400_BAD_REQUEST)

    # Remove the follower relationship
    follower_relation.delete()

    return Response({'message': 'Successfully unsubscribed'}, status=status.HTTP_200_OK)  


@api_view(['POST'])
@cognito_login_required
def handle(request):
    if request.method == 'POST':
        return unlock_premium(request)