from rest_framework import status
from rest_framework.decorators import api_view
from noteally_app.decorators import cognito_login_required
from rest_framework.response import Response
from noteally_app.serializers import MaterialSerializer
from noteally_app.models import Material, User

ERROR_RESPONSE = {'error': 'Error while getting posts'}

def get_posts(request):
    try:
        user_id = request.headers['User-id']
        user = User.objects.get(id=user_id)
        materials = Material.objects.filter(user=user).order_by('-upload_date')
        serializer = MaterialSerializer(materials, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as _:
        return Response(ERROR_RESPONSE, status=status.HTTP_400_BAD_REQUEST)
    

def get_posts_by_user(user_id):
    try:
        user = User.objects.get(id=user_id)
        materials = Material.objects.filter(user=user).order_by('-upload_date')
        serializer = MaterialSerializer(materials, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as _:
        return Response(ERROR_RESPONSE, status=status.HTTP_400_BAD_REQUEST)


def delete_post(request, material_id):
    try:
        user_id = request.headers['User-id']
        user = User.objects.get(id=user_id)

        if Material.objects.filter(id=material_id, user=user).exists():
            material = Material.objects.get(id=material_id)
            material.delete()
            return Response({'success': 'Post deleted'}, status=status.HTTP_200_OK)
        
        return Response({'error': 'Post does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as _:
        return Response(ERROR_RESPONSE, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@cognito_login_required
def handle(request):
    if request.method == 'GET':
        return get_posts(request)
    
@api_view(['DELETE'])
@cognito_login_required
def handle_id(request, material_id):
    if request.method == 'DELETE':
        return delete_post(request, material_id)
    
@api_view(['GET'])
@cognito_login_required
def handle_user_id(request, user_id):
    if request.method == 'GET':
        return get_posts_by_user(user_id)


