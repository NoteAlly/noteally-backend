from rest_framework import status
from rest_framework.decorators import api_view
from noteally_app.decorators import cognito_login_required
from rest_framework.response import Response
from noteally_app.models import Material, User, Like

# How karma works: if like, +3 to author, if dislike, no change to author


def like(request, material_id):
    try:
        user_id = request.headers['User-id']
        user = User.objects.get(id=user_id)
        material = Material.objects.get(id=material_id)

        if not Like.objects.filter(user=user, resource=material).exists():
            like = Like(user=user, resource=material, like=True)
            like.save()

            author = material.user
            author.karma_score += 3
            author.save()

            material.total_likes += 1
            material.save()
        
        elif Like.objects.get(user=user, resource=material).like == False:
            like = Like.objects.get(user=user, resource=material)
            like.like = True
            like.save()
            author = material.user
            author.karma_score += 3
            author.save()
            material.total_likes += 1
            material.total_dislikes -= 1
            material.save()

        else:
            return Response({"Success": "Already Liked"}, status=status.HTTP_200_OK)

        return Response({"Success": "Successfully Liked"}, status=status.HTTP_200_OK)
        
    except Material.DoesNotExist:
        return Response({'error': 'Material does not exist'}, status=status.HTTP_404_NOT_FOUND)


def dislike(request, material_id):
    try:
        user_id = request.headers['User-id']
        user = User.objects.get(id=user_id)
        material = Material.objects.get(id=material_id)

        if not Like.objects.filter(user=user, resource=material).exists():
            like = Like(user=user, resource=material, like=False)
            like.save()

            material.total_dislikes += 1
            material.save()

        elif Like.objects.get(user=user, resource=material).like == True:
            like = Like.objects.get(user=user, resource=material)
            like.like = False
            like.save()
            author = material.user
            author.karma_score -= 3
            author.save()
            material.total_likes -= 1
            material.total_dislikes += 1
            material.save()

        else:
            return Response({"Success": "Already Disliked"}, status=status.HTTP_200_OK)

        return Response({"Success": "Successfully Disliked"}, status=status.HTTP_200_OK)
    
    except Material.DoesNotExist:
        return Response({'error': 'Material does not exist'}, status=status.HTTP_404_NOT_FOUND)


def delete(request, material_id):
    try:
        user_id = request.headers['User-id']
        user = User.objects.get(id=user_id)
        material = Material.objects.get(id=material_id)

        if Like.objects.filter(user=user, resource=material).exists():
            like = Like.objects.get(user=user, resource=material)
            if like.like:
                author = material.user
                author.karma_score -= 3
                author.save()
                material.total_likes -= 1
                material.save()
            else:
                material.total_dislikes -= 1
                material.save()
            like.delete()

        return Response({"Success": "Successfully deleted"}, status=status.HTTP_200_OK)
        
    except Material.DoesNotExist:
        return Response({'error': 'Material does not exist'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST', 'DELETE'])
@cognito_login_required
def handle_like(request, material_id):
    if request.method == 'POST':
        return like(request, material_id)
    elif request.method == 'DELETE':
        return delete(request, material_id)


@api_view(['POST', 'DELETE'])
@cognito_login_required
def handle_dislike(request, material_id):
    if request.method == 'POST':
        return dislike(request, material_id)
    elif request.method == 'DELETE':
        return delete(request, material_id)
