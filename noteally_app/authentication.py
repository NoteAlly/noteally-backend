from noteally_app.models import User
from rest_framework import parsers, renderers
# from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.compat import coreapi, coreschema
from rest_framework.response import Response
from rest_framework.schemas import ManualSchema
from rest_framework.schemas import coreapi as coreapi_schema
from rest_framework.views import APIView

from django.conf import settings
from noteally_app.models import TTDToken
import pytz



import datetime

class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    if coreapi_schema.is_enabled():
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    name="email",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Email",
                        description="Valid email for authentication",
                    ),
                ),
                coreapi.Field(
                    name="password",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Password",
                        description="Valid password for authentication",
                    ),
                ),
            ],
            encoding="application/json",
        )

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
        except:
            resposta = Response({'Error': 'User not found'}, headers={"Valid_token": "False"})
            return resposta
        if User.objects.filter(user__username=user.username).exists():
            user_type = "User"
        else:
            user_type = "False"
            resposta = Response({'Error': 'User not found'}, headers={"Valid_token": "False"})
            return resposta
        # TTDToken.objects.all().delete()
        token, created = TTDToken.objects.get_or_create(user=user)


        utc_now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        if not created and token.ttd < utc_now:
            token.delete()
            token.key = TTDToken.generate_key()
            token.ttd = utc_now + settings.TOKEN_EXPIRE_TIME
            token.save()

        resposta = Response({'token': token.key}, headers={"Valid_token": user_type})
        resposta["Access-Control-Expose-Headers"] = "*, Valid_token"
        # resposta["Access-Control-Allow-Headers"] = "Content-Type"
        return resposta


def token_is_valid(token):
    try:
        token = TTDToken.objects.get(key=token)
    except TTDToken.DoesNotExist:
        return False
    utc_now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
    if token.ttd < utc_now:
        return False
    return True

def user_token(request):
    if "Token" in request.headers.keys() and token_is_valid(request.headers['Token']):
        token = TTDToken.objects.get(key=request.headers['Token'])
        if User.objects.filter(user__username=token.user.username).exists():
            return "User" 
    return "False"