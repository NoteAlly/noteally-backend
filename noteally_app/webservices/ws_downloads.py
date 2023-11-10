from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from noteally_app.models import Material, Download, User
from noteally_app.serializers import MaterialSerializer


def get_materials_id_download(request, material_id):
    try:
        user_id = request.headers['User-id']
        user = User.objects.get(id=user_id)

        material = Material.objects.get(id=material_id)

        if not Download.objects.filter(user=user, resource=material).exists():
            author = material.user
            author.karma_score += 5
            author.save()

            material.total_downloads += 1
            material.save()
            download = Download(user=user, resource=material)
            download.save()

    except:
        return Response({'error': 'Error while downloading material'}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({"name": material.file_name, "link": material.file.url}, status=status.HTTP_200_OK)


def get_downloads(request):
    try:
        user_id = request.headers['User-id']
        downloads = Download.objects.filter(user=user_id)
        materials = [material.resource for material in downloads]
        serializer = MaterialSerializer(materials, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    except:
        return Response({'error': 'Error while getting downloads'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def handle(request):
    if request.method == 'GET':
        return get_downloads(request)
        
   
@api_view(['GET'])
def handle_id(request, material_id):
    if request.method == 'GET':
        return get_materials_id_download(request, material_id)
        
