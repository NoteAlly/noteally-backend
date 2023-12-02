from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from noteally_app.CustomPagination import CustomPagination
from noteally_app.serializers import SubsUserSerializer, FollowerSerializer
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
        user = User.objects.get(id=request.headers['User-id'])
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
def get_subscriptions(request):
    user = User.objects.get(id=request.headers['User-id'])
    users = user.followers.all()  
    
    # Filtering
    if "karma_score" in request.GET:
        users = users.filter(karma_score__gte=request.GET["karma_score"]) 

    if "study_areas" in request.GET:
        study_areas = request.GET.getlist("study_areas")
        users = users.filter(study_areas__in=study_areas)
        
    if "name" in request.GET:
        names = request.GET["name"].strip().split(" ")
        if len(names) != 0:
            if len(names) == 1:
                users = users.filter(first_name__icontains=names[0]) | users.filter(last_name__icontains=names[0])
            else:
                users = users.filter(first_name__icontains=names[0], last_name__icontains=names[1])


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
     


# Used to get a list of the users subscribed to "user_id" user
def get_subscribers(user_id):
    user = User.objects.get(id=user_id)
    subscribers = user.followers_set.all()  
    
    return subscribers



@api_view(['POST'])
def handle(request):
    if request.method == 'POST':
        return unlock_premium(request)