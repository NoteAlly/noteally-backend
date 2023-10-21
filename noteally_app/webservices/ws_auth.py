
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from noteally_app.models import Download, Like, Material, StudyArea, User, University
from noteally_app.serializers import RegisterSerializer, LoginSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout  
#from rest_framework_simplejwt.tokens import RefreshToken



# @api_view(['POST'])
# @permission_classes([AllowAny])
# def register(request):
#     '''Register a new user'''
#     serializer = RegisterSerializer(data=request.data)
#     if serializer.is_valid():
#         user = serializer.save()
#         return Response({'token': AuthToken.objects.create(user)[1]},
#                         status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST']) 
def login_(request):
    '''Login a user''' 
    if 'email' not in request.data or 'password' not in request.data:
            return Response({'msg': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)
    email = request.POST['email']
    password = request.POST['password']
    user = authenticate(request, email=email, password=password)
    if user is not None:
        login(request, user)
        #auth_data = get_tokens_for_user(request.user)
        return Response({'msg': 'Login Success'}, status=status.HTTP_200_OK)
    return Response({'msg': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
 


@api_view(['POST'])
def register(request):  
    data_ = request.data.copy() 

    serializer = RegisterSerializer(data=request.data)
   
    if serializer.is_valid():    
        
        if User.objects.filter(email=data_['email']).exists():
            return Response({'message': 'Email already in use!'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save() 
        return Response({'msg': 'Register Success'},
                         status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
     
     