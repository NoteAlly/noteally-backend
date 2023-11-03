# Load the rest framework libraries
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Load the serializers
from noteally_app.serializers import InfoSerializer

# Load the models
from noteally_app.models import University, StudyArea


def get_info():
    universities = University.objects.all()
    study_areas = StudyArea.objects.all()
    serializer = InfoSerializer({"universities": universities, "study_areas": study_areas})

    return Response(serializer.data)


@api_view(['GET'])
def handle(request):
    if request.method == 'GET':
        return get_info()