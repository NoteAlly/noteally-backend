from rest_framework import status
from rest_framework.decorators import api_view
from noteally_app.decorators import cognito_login_required
from rest_framework.response import Response
from noteally_app.models import Material, Download, User
from noteally_app.serializers import MaterialSerializer
from django.conf import settings
import boto3
from botocore.client import Config


def get_materials_id_download(request, material_id):
    try:
        user_id = request.headers['User-id']
        user = User.objects.get(id=user_id)
        material = Material.objects.get(id=material_id)

        # Presigned URL - S3
        s3 = boto3.client(
            service_name='s3',
            region_name=settings.AWS_REGION_NAME,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            endpoint_url=f'https://s3.{settings.AWS_REGION_NAME}.amazonaws.com',
            config=Config(signature_version='s3v4')
        )

        bucket_name = settings.AWS_S3_PRIVATE_BUCKET_NAME
        key = material.file.name

        url = s3.generate_presigned_url(
            ClientMethod = 'get_object',
            ExpiresIn = 60,
            Params = {
                'Bucket': bucket_name,
                'Key': key
            }
        )

        # FOR LOCAL DEVELOPMENT ONLY --> Comment the above code and uncomment next line
        # url = material.file.url

        if not Download.objects.filter(user=user, resource=material).exists():
            author = material.user
            author.karma_score += 5
            author.save()

            material.total_downloads += 1
            material.save()
            download = Download(user=user, resource=material)
            download.save()
    except Exception as _:
        return Response({'error': 'Error while downloading material'}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({"name": material.file_name, "link": url}, status=status.HTTP_200_OK)


def get_downloads(request):
    try:
        user_id = request.headers['User-id']
        downloads = Download.objects.filter(user=user_id)
        materials = [material.resource for material in downloads]
        serializer = MaterialSerializer(materials, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as _:
        return Response({'error': 'Error while getting downloads'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@cognito_login_required
def handle(request):
    if request.method == 'GET':
        return get_downloads(request)
        
   
@api_view(['GET'])
@cognito_login_required
def handle_id(request, material_id):
    if request.method == 'GET':
        return get_materials_id_download(request, material_id)
        
