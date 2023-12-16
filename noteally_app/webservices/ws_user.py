from rest_framework import status
from rest_framework.decorators import api_view
from noteally_app.decorators import cognito_login_required
from rest_framework.response import Response
from noteally_app.CustomPagination import CustomPagination
from noteally_app.serializers import SubsUserSerializer, FollowerSerializer
from noteally_app.models import User, Follower
from noteally_app.webservices.ws_auth import get_cognito_user
import boto3
from botocore.client import Config
from django.conf import settings

USER_NOT_FOUND_RESPONSE = {'error': 'User not found'}

def unlock_premium(request):
    try:
        user = User.objects.get(id=request.headers['User-id'])
    except User.DoesNotExist:
        return Response(USER_NOT_FOUND_RESPONSE, status=status.HTTP_400_BAD_REQUEST)
    except KeyError:
        return Response({'error': 'User-id header not found'}, status=status.HTTP_400_BAD_REQUEST)
    
    if user.premium:
        return Response({'error': 'User is already premium'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Update user's premium status
    user.premium = True
    user.save()
    
    return Response({'user_id': user.id, 'message': 'Premium unlocked'}, status=status.HTTP_200_OK)

# Subscribe the user to the SNS topic to allow notifications of new uploads
def subscribe_to_sns_topic(user, user_to_follow):
    # Obtain the topic ARN
    topic_name = f'uploads-user-{user_to_follow.id}'
    topic_arn = f'arn:aws:sns:{settings.AWS_REGION_NAME}:{settings.AWS_ACCOUNT_ID}:{topic_name}'
    print(f"Topic ARN: {topic_arn}")

    # Presigned URL - SNS
    sns_client = boto3.client(
        service_name='sns',
        region_name=settings.AWS_REGION_NAME,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        config=Config(signature_version='s3v4')
    )

    # Create a new topic for the user to follow if it doesn't exist
    response = sns_client.list_topics()
    existing_topics = [topic['TopicArn'] for topic in response.get('Topics', [])]
    if topic_arn not in existing_topics:
        # Create a new topic for the user to follow if it doesn't exist
        sns_client.create_topic(Name=topic_name)

    # Subscribe the user to the topic
    sns_client.subscribe(
        TopicArn=topic_arn,
        Protocol='email',  
        Endpoint=user.email  
    )

@api_view(['POST']) 
def subscribe(request, user_id): 
    try:
        user_to_follow = User.objects.get(id=user_id)
        user = User.objects.get(id=request.headers['User-id'])
    except User.DoesNotExist:
        return Response(USER_NOT_FOUND_RESPONSE, status=status.HTTP_404_NOT_FOUND) 

    # Check if the user is already following
    if Follower.objects.filter(follower=user, following=user_to_follow).exists():
        return Response({'error': 'Already following this user'}, status=status.HTTP_400_BAD_REQUEST)

    # Create a new follower relationship
    Follower.objects.create(follower=user, following=user_to_follow)

    # Subscribe the user to the SNS topic of the user to follow
    subscribe_to_sns_topic(user, user_to_follow)

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