from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from noteally_app.models import Professor

# Create your views here.
# @api_view(["GET"])
# def hello(request):
#     #usefull for testing
#     return Response({"message": "Hello, world!"}, status=status.HTTP_200_OK)

# @api_view(["GET"])
# def insertdata(request):
#     # Insert 2 professors
#     professor1 = Professor(name="John")
#     professor1.save()
#     professor2 = Professor(name="Jane")
#     professor2.save()
#     return Response({"message": "Data inserted"}, status=status.HTTP_200_OK)

# @api_view(["GET"])
# def getdata(request):
#     Professor.objects.all()
#     return Response({professor.id: professor.name for professor in Professor.objects.all()}, status=status.HTTP_200_OK)
