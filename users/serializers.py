from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from .models import Profile



class UserAuthenticationSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

# class UserRegistrationSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField()
#
#     def validate_username(self, username):
#         if User.objects.filter(username=username).exists():
#             raise ValidationError("User already exists!")
#         return username
#

class MyActivationCodeSerializer(serializers.Serializer):
    code = serializers.CharField(
        max_length=50,
        error_messages={
            'required': 'Введите код!',
            'max_length': 'Максимальное количество символов 50'
        }
    )

    def save(self, profile):
        profile.code = self.validated_data['code']
        profile.save()
        return profile

class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(
        required=True,
        max_length=15,
        min_length=2,
        error_messages={
            'required': 'Введите имя пользователя!',
            'max_length': 'Максимальное количество символов 15',
            'min_length': 'Минимальное количество символов 2'
        }
    )
    password1 = serializers.CharField(write_only=True, min_length=3, max_length=30)
    password2 = serializers.CharField(write_only=True, min_length=3, max_length=30)
    firstname = serializers.CharField(required=True, max_length=25)

    class Meta:
        model = User
        fields = (
            'username',
            'firstname',
            'email',
            'password1',
            'password2'
        )

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Пользователь с таким именем уже существует.")
        return value

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Пароли не совпадают.")
        return data
    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['firstname'],
            is_active=False
        )
        user.set_password(validated_data['password1'])
        user.save()
        return user
