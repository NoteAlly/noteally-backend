# Load the rest framework libraries
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Load the serializers
from noteally_app.serializers import PostMaterialSerializer, MaterialSerializer

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


def get_materials(request):
    materials = Material.objects.all()

    # filtering
    if "title" in request.GET:
        materials = materials.filter(name__icontains=request.GET["title"])
    if "author" in request.GET:
        materials = materials.filter(user__name__icontains=request.GET["author"])
    if "study_area" in request.GET:
        materials = materials.filter(study_areas__id=request.GET["study_area"])
    if "university" in request.GET:
        materials = materials.filter(university__id=request.GET["university"])
    if "min_likes" in request.GET:
        materials = materials.filter(likes__gte=request.GET["min_likes"])
    if "min_downloads" in request.GET:
        materials = materials.filter(downloads__gte=request.GET["min_downloads"])
    if "free" in request.GET:
        if request.GET["free"] == "true":
            materials = materials.filter(price=0)
        elif "max_price" in request.GET:
            materials = materials.filter(price__lte=request.GET["max_price"])
    
    # ordering
    order_options = ["name", "price", "-price", "total_downloads", "-total_downloads", "total_likes", "-total_likes"]

    if "order_by" in request.GET and request.GET["order_by"] in order_options:
        materials = materials.order_by(request.GET["order_by"])
    else:
        materials = materials.order_by('-total_downloads', '-total_likes')
    
    serializer = MaterialSerializer(materials, many=True)
    return Response(serializer.data)



@api_view(['GET', 'POST'])
def handle(request):
    try:
        if request.method == 'POST':
            return post_materials(request)
        elif request.method == 'GET':
            return get_materials(request)

    except Exception as e:
       return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)