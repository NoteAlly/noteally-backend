from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from noteally_app.CustomPagination import CustomPagination
from noteally_app.serializers import UserSerializer
from noteally_app.models import User 



def get_tutors(request):
    users = User.objects.filter(karma_score__gte=1)

    # Filtering
    if "karma_score" in request.GET:
        users = users.filter(karma_score__gte=request.GET["karma_score"])

    if "university" in request.GET:
        users = users.filter(university__id=request.GET["university"])

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
    serializer = UserSerializer(paginated_users, many=True)
    paginated_response = paginator.get_paginated_response(serializer.data)

    return Response(paginated_response.data, status=status.HTTP_200_OK)

def get_tutors_id(request, user_id):
    try: 

        user = User.objects.get(id=user_id) 
        
        serializer = UserSerializer(user)
        data = serializer.data.copy() 
        
    except User.DoesNotExist:
        return Response({'error': 'Tutor does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def handle(request):
    if request.method == 'GET':
        return get_tutors(request)

   
   
@api_view(['GET'])
def handle_id(request, user_id):
    if request.method == 'GET':
        return get_tutors_id(request, user_id)