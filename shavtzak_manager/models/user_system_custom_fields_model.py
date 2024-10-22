from django.contrib.auth.models import User
from django.db import models
from enum import Enum


class UserType(Enum):
    ENTITY_INITIALIZER = 'entity_initializer'
    SHAVTZAK_MANAGER = 'shavtzak_manager'
    REGULAR_USER = 'regular_user'


class UserSystemCustomFields(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_system_custom_fields')
    
    user_type = models.CharField(
        max_length=30,
        choices=[(option.value, option.name.replace('_', ' ').title()) for option in UserType],
        default=UserType.REGULAR_USER.value 
    )

    def __str__(self):
        return f'{self.user.username} is of type {self.user_type}'

