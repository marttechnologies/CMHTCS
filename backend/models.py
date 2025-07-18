from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractUser

from phonenumber_field.modelfields import PhoneNumberField

class User(AbstractUser):
    # Unique identifier for the user
    user_id = models.CharField(max_length=50, unique=True, verbose_name="User ID")
    
    # Personal information fields
    first_name = models.CharField(max_length=30, verbose_name="First Name")
    middle_name = models.CharField(max_length=30, verbose_name="Middle Name", blank=True)
    last_name = models.CharField(max_length=30, verbose_name="Last Name")
    date_of_birth = models.DateField(verbose_name="Date of Birth")

    # Contact information
    phone_number = PhoneNumberField(
        region="ET", # default region (Ethiopia) for parsing
        blank=True,
        null=True,)
    email = models.EmailField(max_length=254, verbose_name="Email Address", unique=True)

    # User type (e.g., staff, student, guardian)
    user_type = models.CharField(max_length=20, choices=[
        ('staff', 'Staff'),
        ('student', 'Student'),
        ('guardian', 'Guardian')
        
    ], verbose_name="User Type")
    
    
    password = models.CharField(max_length=128, verbose_name="Password")
    
    username = None  # Disable username field
    # Required fields for user creation
    USERNAME_FIELD = "user_id"
    REQUIRED_FIELDS = ["first_name", "middle_name", "last_name", "user_type"]

    def __str__(self):
        return f"{self.first_name} {self.middle_name} {self.last_name} ({self.user_id})"
    


class Staff(models.Model):
    """
    Staff model inheriting from User.
    This can be extended with additional staff-specific fields if needed.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff')
    
    class Meta:
        verbose_name = "Staff"
        verbose_name_plural = "Staff"
    
    def __str__(self):
        return f"Staff: {self.first_name} {self.last_name} ({self.user_id})"