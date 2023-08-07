from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from .serializers import AuthorizationValidateSerializer, RegistrationValidateSerialiser
from django.contrib.auth.models import User
from rest_framework.views import APIView

@api_view(['POST'])
def registration_api_view(request):
    serializer = RegistrationValidateSerialiser(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data.get('username')
    password = serializer.validated_data.get('password')

    user = User.objects.create_user(username=username, password=password)
    return Response(status=201, data={'user_id': user.id})


class AuthorizationAPIView(APIView):
    def post(self, request):

        # 0. Step: Validation
        serializer = AuthorizationValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 1. Step: Get Data from client
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        # 2. Step: Search user by credentials
        user = authenticate(username=username, password=password)

        # 3. Return key
        if user is not None:
             token_, created = Token.objects.get_or_create(user=user)
             return Response(data={'key': token_.key})

        # 4. Return Error
        return Response(status=401, data={'message': 'User not found'})


