import uuid
from django.db import models
from django.contrib.auth.models import Group, User
from django.utils import timezone

class Entity(models.Model):
    
    name = models.CharField(max_length=20)
    
    code = models.CharField(max_length=6, unique=True, null=True, editable=False)  # Auto-generated unique code, not editable

    description = models.CharField(max_length=300, null=True)
   
    creator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,  # Set to null if the user is deleted
        null=True,
        related_name='entities' 
    )
    
    created_at = models.DateTimeField(default=timezone.now)  # Automatically set current time on creation

    group = models.OneToOneField(Group, on_delete=models.CASCADE, null=True, blank=True)  # Link to the Django Group model
    
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
