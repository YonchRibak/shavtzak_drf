import uuid

from django.contrib.auth.models import Group
from django.db import models


# TODO: questions - why so many null=True?
class Entity(models.Model):
    class Meta:
        verbose_name = "ישות"
        verbose_name_plural = "ישויות"

    name = models.CharField(max_length=20, verbose_name="שם", unique=True)
    code = models.CharField(max_length=6, unique=True, null=True, editable=False,
                            verbose_name="קוד")  # Auto-generated unique code, not editable
    description = models.CharField(max_length=300, null=True, verbose_name="תיאור")
    creator = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,  # Set to null if the user is deleted
        null=True,
        related_name='entities',
        verbose_name="יוצר"
    )
    created_at = models.DateTimeField(auto_now=True,
                                      verbose_name="זמן יצירה")  # Automatically set current time on creation
    group = models.OneToOneField("auth.Group", on_delete=models.CASCADE, null=True, blank=True,
                                 verbose_name="קבוצת הרשאות")  # Link to the Django Group model

    def save(self, *args, **kwargs):

        # Automatically generate the code if it doesn't exist:
        if not self.code:
            self.code = self.generate_unique_code()

        # Create the Group instance if it doesn't exist:
        if self.group is None:
            group = Group.objects.create(name=self.name)  # Use the name of the Entity as the Group name
            self.group = group
            group.user_set.add(self.creator)  # Automatically add user creating Group to said group

        super().save(*args, **kwargs)

    def generate_unique_code(self):
        """Generate a unique 6-character code based on a UUID."""
        code = str(uuid.uuid4())[:6].replace("-", "").upper()
        while Entity.objects.filter(code=code).exists():
            code = str(uuid.uuid4())[:6].replace("-", "").upper()
        return code

    def __str__(self):
        return self.name
