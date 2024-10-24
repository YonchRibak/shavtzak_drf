from django.db import models


class UserTypeChoices(models.TextChoices):
    ENTITY_INITIALIZER = 'entity_initializer'
    SHAVTZAK_MANAGER = 'shavtzak_manager'
    REGULAR_USER = 'regular_user'


class UserSystemCustomFields(models.Model):
    
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE, related_name='user_system_custom_fields', verbose_name="משתמש")
    
    user_type = models.CharField(
        max_length=30,
        choices=UserTypeChoices,
        default=UserTypeChoices.REGULAR_USER.value,
        verbose_name="סוג משתמש"
    )

    def __str__(self):
        return f'{self.user.username} is of type {self.user_type}'

    class Meta:
        verbose_name = 'שדה נוסף למשתמש'
        verbose_name_plural = 'שדות נוספים למשתמש'
