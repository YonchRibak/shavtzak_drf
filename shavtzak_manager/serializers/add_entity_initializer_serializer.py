from rest_framework import serializers
from django.contrib.auth.models import User, Group
from ..models import UserSystemCustomFields, UserType, Entity

# Serializer for adding a user as an entity initializer without an entity
class AddEntityInitializerSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=150)

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']

        # Create the user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        # Create the UserSystemCustomFields instance as an entity initializer
        UserSystemCustomFields.objects.create(
            user=user,
            user_type=UserType.ENTITY_INITIALIZER.value,
        )

        return user