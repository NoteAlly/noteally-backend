from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from noteally_app.CustomPagination import CustomPagination
from noteally_app.serializers import MaterialIDSerializer, PostMaterialSerializer, MaterialSerializer
from noteally_app.models import Material, Download, User, Like 
import uuid
import boto3
from botocore.client import Config
from django.conf import settings

def post_materials(request):
    user_id = request.headers['User-id']
    user = User.objects.get(id=user_id)
    user.karma_score += 3
    user.save()

    data_ = request.data.copy()

    if 'file' in request.FILES:
        data_['file_name'] = request.FILES['file'].name
        data_['file_size'] = request.FILES['file'].size
    
    serializer = PostMaterialSerializer(data=data_)
    
    if serializer.is_valid():
        if 'file' in request.FILES:
            serializer.validated_data['file'].name = str(uuid.uuid4()) + '.' + data_['file_name'].split('.')[-1]
        object_ = serializer.save()
        
        #Notify all subscribers
        subscribers = user.followers_set.all()  

        # Create topic for user if it doesn't exist
        #if not user.sns_topic_arn:
        topic_name = f'uploads-user-{user.id}'
        #else: 
        #    topic_name = user.sns_topic_arn.split(':')[-1]

        # Publish message to SNS topic for each subscriber
        topic_arn = f'arn:aws:sns:{settings.AWS_REGION_NAME}:{settings.AWS_ACCOUNT_ID}:{topic_name}'

        # Presigned URL - SNS
        sns_client = boto3.client(
            service_name='sns',
            region_name=settings.AWS_REGION_NAME,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            config=Config(signature_version='s3v4')
        )

        # Create a message to publish
        message = f"New material posted by {user.first_name} {user.last_name} with title {serializer.validated_data['file'].name}"  # Adjust the message as needed

        # Create a subject for the message
        subject = f"New material posted by {user.first_name} {user.last_name}"  # Adjust the subject as needed
        
        # Publish message to SNS in the topic 
        try:
            sns_client.publish(
                TopicArn=topic_arn,
                Message=message,
                Subject=subject,
                MessageStructure='string'
            )
        except Exception as e:
            print(f"Failed to publish message to subscribers: {str(e)}")
    
        return Response({"Success": "Successfully Created", "created_id": object_.id}, status=status.HTTP_201_CREATED)
        
    return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST) 

def get_materials(request):
    materials = Material.objects.all()

    # filtering
    if "name" in request.GET:
        materials = materials.filter(name__icontains=request.GET["name"])

    if "author" in request.GET:
        names = request.GET["author"].strip().split(" ")
        if len(names) != 0:
            if len(names) == 1:
                materials = materials.filter(user__first_name__icontains=names[0]) | materials.filter(user__last_name__icontains=names[0])
            else:
                materials = materials.filter(user__first_name__icontains=names[0], user__last_name__icontains=names[1])

    if "study_areas" in request.GET:
        study_areas = request.GET.getlist("study_areas")
        materials = materials.filter(study_areas__in=study_areas)

    if "university" in request.GET:
        materials = materials.filter(university__id=request.GET["university"])

    if "min_likes" in request.GET:
        materials = materials.filter(total_likes__gte=request.GET["min_likes"])

    if "min_downloads" in request.GET:
        materials = materials.filter(total_downloads__gte=request.GET["min_downloads"])

    if "free" in request.GET:
        if request.GET["free"] == "true":
            materials = materials.filter(price=0)
        
        if "max_price" in request.GET:
            materials = materials.filter(price__lte=request.GET["max_price"])
    
    # ordering
    order_options = ["name", "-name", "price", "-price", "total_downloads", "-total_downloads", "total_likes", "-total_likes", "upload_date", "-upload_date"]

    if "order_by" in request.GET and request.GET["order_by"] in order_options:
        materials = materials.order_by(request.GET["order_by"])
    else:
        materials = materials.order_by('-total_downloads', '-total_likes')

    paginator = CustomPagination()
    paginated_materials = paginator.paginate_queryset(materials, request)
    serializer = MaterialSerializer(paginated_materials, many=True)
    paginated_response = paginator.get_paginated_response(serializer.data)
    
    return Response(paginated_response.data, status=status.HTTP_200_OK)


def get_materials_id(request, material_id):
    try:
        user_id = request.headers['User-id']
        user = User.objects.get(id=user_id)

        material = Material.objects.get(id=material_id)
        owned = Download.objects.filter(user=user, resource=material).exists()
        liked = Like.objects.filter(user=user, resource=material).exists()


        serializer = MaterialIDSerializer(material)
        data = serializer.data.copy()
        data["owned"] = owned

        if material.price == 0:
            data["owned"] = False

        if material.user.id == user.id:
            data["owned"] = True

        if liked:
            like = Like.objects.get(user=user, resource=material)
            data["like"] = like.like
        else:
            data["like"] = None
        
    except Material.DoesNotExist:
        return Response({'error': 'Material does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def handle(request):
    if request.method == 'POST':
        return post_materials(request)
    elif request.method == 'GET':
        return get_materials(request)
   
   
@api_view(['GET', 'PUT', 'DELETE'])
def handle_id(request, material_id):
    if request.method == 'GET':
        return get_materials_id(request, material_id)