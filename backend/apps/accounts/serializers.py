from django.contrib.auth.models import User
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({
                'password': 'Passwords do not match.'
            })
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({
                'username': 'Username already exists.'
            })
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({
                'email': 'Email already exists.'
            })
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        user.is_active = False
        user.save()
        return user