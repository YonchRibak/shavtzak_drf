from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import UserSystemCustomFields, UserType, Entity


# Serializer for adding users and adding them to an existing entity
class AddUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    entity_id = serializers.IntegerField()
    entity_code = serializers.CharField(max_length=6)
    user_type = serializers.ChoiceField(choices=[UserType.REGULAR_USER.value, UserType.SHAVTZAK_MANAGER.value])
    
    def validate(self, data):
        entity_id = data.get('entity_id')
        entity_code = data.get('entity_code')
        user_type = data.get('user_type')

        # Validate the entity
        try:
            entity = Entity.objects.get(id=entity_id)
            if entity.code != entity_code:
                raise serializers.ValidationError('Entity credentials are invalid.')
            data['entity'] = entity # Store entity in validated_data
        except Entity.DoesNotExist:
            raise serializers.ValidationError('Entity does not exist.')

        # Validate user_type
        if user_type not in [UserType.REGULAR_USER.value, UserType.SHAVTZAK_MANAGER.value]:
            raise serializers.ValidationError('Invalid user type.')

        return data

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        entity = validated_data['entity']
        user_type = validated_data['user_type']

        # Create the user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Add user to the entity's group
        group = entity.group
        group.user_set.add(user)

        # Create the UserSystemCustomFields instance with the provided user_type
        UserSystemCustomFields.objects.create(
            user=user,
            user_type=user_type,
        )

        return user