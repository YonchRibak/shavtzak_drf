from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import UserSystemCustomFields, UserTypeChoices, Entity


# Serializer for adding users and adding them to an existing entity
class AddUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    entity = serializers.PrimaryKeyRelatedField(queryset=Entity.objects.all())
    entity_id = serializers.IntegerField()
    entity_code = serializers.CharField(max_length=6)
    user_type = serializers.ChoiceField(choices=[UserTypeChoices.REGULAR_USER.value, UserTypeChoices.SHAVTZAK_MANAGER.value])
    
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

        return data

    def validate_user_type(self, value):
        if value not in UserTypeChoices.allowed_users_for_something:
            raise serializers.ValidationError('Invalid user type.')


    def create(self, validated_data):
        entity = validated_data.pop('entity', None)
        user_type = validated_data.pop("user_type", None)

        # Create the user
        user = User.objects.create_user(
            **validated_data
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