from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.conf import settings
import random
import datetime
from .models import Profile
from .serializers import RegistrationSerializer, MyActivationCodeSerializer,  UserAuthenticationSerializer

def generate_code():
    random.seed()
    return str(random.randint(10000, 99999))

@api_view(['POST'])
def register_api_view(request):
    if request.user.is_authenticated:
        return Response({'detail': 'Already authenticated'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password1')
        user = User.objects.get(username=username, email=email, is_active=False)
        code = generate_code()

        while Profile.objects.filter(code=code).exists():
            code = generate_code()

        Profile.objects.create(user=user, code=code, date=datetime.datetime.now())

        send_mail(
            'код подтверждения',
            code,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False
        )

        return Response({'detail': 'Registration successful, activation code sent'}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def endreg(request):
    if request.user.is_authenticated:
        return Response({'detail': 'Already authenticated'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = MyActivationCodeSerializer(data=request.data)
    if serializer.is_valid():
        code_use = serializer.validated_data.get("code")
        try:
            profile = Profile.objects.get(code=code_use)
        except Profile.DoesNotExist:
            return Response({'detail': 'Invalid activation code'}, status=status.HTTP_400_BAD_REQUEST)

        if not profile.user.is_active:
            profile.user.is_active = True
            profile.user.save()
            login(request, profile.user)
            profile.delete()
            return Response({'detail': 'Activation successful'}, status=status.HTTP_200_OK)

        return Response({'detail': 'Account already activated'}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# @api_view(['POST'])
# def registration_api_view(request):
#     serializer = UserRegistrationSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#
#     username = serializer.validated_data.get('username')
#     password = serializer.validated_data.get('password')
#
#     User.objects.create_user(username=username, password=password)
#
#     return Response(status=status.HTTP_200_OK)

class Authorization_api_view(APIView):
    def post(self, request):
        serializer = UserAuthenticationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        user = authenticate(username=username, password=password)
        print(user)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response(status=status.HTTP_200_OK, data={'key': token.key})
        return Response(status=status.HTTP_404_NOT_FOUND, data={'This is user not authorized'})
