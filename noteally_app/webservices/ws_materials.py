# Load the rest framework libraries
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Load the serializers
from noteally_app.serializers import PostMaterialSerializer

# Load the models
from noteally_app.models import Material


def post_materials(request):
    data_ = request.data.copy()
    if 'file' in request.FILES:
        data_['file_name'] = request.FILES['file'].name
    
    serializer = PostMaterialSerializer(data=data_)
    
    if serializer.is_valid():
        object_ = serializer.save()
        return Response({"Success": "Successfully Created", "created_id": object_.id}, status=status.HTTP_201_CREATED)
        
    return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def handle(request):
    try:
        if request.method == 'POST':
            return post_materials(request)
    except Exception as e:
       return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)