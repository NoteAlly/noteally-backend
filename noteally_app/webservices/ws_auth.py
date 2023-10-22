
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from noteally_app.models import Download, Like, Material, StudyArea, User, University
from noteally_app.serializers import RegisterSerializer, LoginSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout   

@api_view(['POST']) 
def login_(request):
    '''Login a user''' 
    
    print(request.data['email'])
    if 'email' not in request.data or 'password' not in request.data:
            return Response({'error': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)
    email = request.data['email']
    password = request.data['password']
    if (User.objects.filter(email=email).exists() ):  
        if (User.objects.get(email=email).check_password(password)):
            user = User.objects.get(email=email)  
            return Response({"Success": "Successfully Logged",'id': user.id,'name': user.name, 'email': user.email}, status=status.HTTP_200_OK)
       
    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
 


@api_view(['POST'])
def register(request):  
    data_ = request.data.copy() 

    serializer = RegisterSerializer(data=request.data)
   
    if serializer.is_valid():    
        
        if User.objects.filter(email=data_['email']).exists():
            return Response({'message': 'Email already in use!'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()  
        return Response({"Success": "Successfully Registered"},
                         status=status.HTTP_200_OK)
    return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
     
     