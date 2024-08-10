from rest_framework import serializers
from .models import Article, User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError("Неверная почта или пароль.")
        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        user = validated_data.get('user')
        token, created = Token.objects.get_or_create(user=user)
        return {'token': token.key}


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'role']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email уже существует.")
        return value

    def validate_password(self, value):
        if (len(value) < 8 or
                not any(char.isdigit() for char in value)
                or not any(char.isalpha() for char in value)):
            raise serializers.ValidationError(
                "Пароль должен быть не менее 8 символов "
                "и содержать хотя бы одну цифру и букву.")
        return value

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = User(**validated_data)
        user.save()
        return user


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'is_published',
                  'created_at', 'updated_at']
        read_only_fields = ['author', 'created_at', 'updated_at']
