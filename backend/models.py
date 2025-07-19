from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractUser
from django.core.validators import FileExtensionValidator

from phonenumber_field.modelfields import PhoneNumberField

from backend.db_models import mini_models,location
from backend.accessories_codes import id_generator
import choices


class UserManager(BaseUserManager):
    def create_user(self, user_id=None, first_name=None, last_name=None, date_of_birth=None, user_type=None, middle_name='', password=None, **extra_fields):
        
        if not user_type:
            raise ValueError("User type is required")
        if not user_id:
            if user_type == 'staff':
                user_id = id_generator.id_gen(staff=True)
            elif user_type == 'guardian':
                user_id = id_generator.id_gen(guardian=True)  
            else:
                user_id = id_generator.id_gen()
        

        user = self.model(
            user_id=user_id,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            user_type=user_type,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, **kwargs):
        kwargs.setdefault("user_type", "staff")
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_active", True)

        if not kwargs.get("is_staff") or not kwargs.get("is_superuser"):
            raise ValueError("Superuser must have is_staff=True and is_superuser=True.")

        return self.create_user(**kwargs)
    
class User(AbstractUser):
    # Unique identifier for the user
    user_id = models.CharField(max_length=50, unique=True, editable=False, verbose_name="User ID")
    
    # Personal information fields
    first_name = models.CharField(max_length=30, verbose_name="First Name")
    middle_name = models.CharField(max_length=30, verbose_name="Middle Name", blank=True)
    last_name = models.CharField(max_length=30, verbose_name="Last Name")
    date_of_birth = models.DateField(verbose_name="Date of Birth")
    
    # User type (e.g., staff, student, guardian)
    user_type = models.CharField(max_length=20, choices=[
        ('staff', 'Staff'),
        ('student', 'Student'),
        ('guardian', 'Guardian')
        
    ], verbose_name="User Type")

    
    username = None  # Disable username field
    # Required fields for user creation
    USERNAME_FIELD = "user_id"
    REQUIRED_FIELDS = ["first_name", "middle_name", "last_name","date_of_birth", "user_type"]

    def __str__(self):
        return f"{self.first_name} {self.middle_name} {self.last_name} ({self.user_id})"
    def save(self, *args, **kwargs):
        if not self.user_id:
            # Generate a new user ID based on the user type
            if self.user_type == 'staff':
                self.user_id = id_generator.id_gen(staff=True)
            elif self.user_type == 'guardian':
                self.user_id = id_generator.id_gen(guardian=True)
            else:
                self.user_id = id_generator.id_gen()
        super().save(*args, **kwargs)
    


class Staff(models.Model):
    """
    Staff model inheriting from User.
    This can be extended with additional staff-specific fields if needed.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff')
    
    # Contact information
    phone_number = PhoneNumberField(
        region="ET", # default region (Ethiopia) for parsing
        unique=True, verbose_name="Phone Number"
    )
    email = models.EmailField(max_length=254, verbose_name="Email Address", unique=True)
    address = models.ForeignKey(location.Kebele, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Address")
    emergency_contact = PhoneNumberField(
        region="ET", # default region (Ethiopia) for parsing
    )
    
    # Role related fields
    staff_role = models.CharField(
        max_length=50, verbose_name="Staff Role", 
        choices=choices.STAFF_ROLE_CHOICES, default='teacher'
    )
    employment_type = models.CharField(
        max_length=20, choices=[
            ('full_time', 'Full Time'),
            ('part_time', 'Part Time'),
            ('contract', 'Contract')
        ], verbose_name="Employment Type", default='full_time'
    )
    
    
    # Additional staff-specific fields
    marital_status = models.CharField(
        max_length=20,
        choices=[
            ('unmarried', 'Unmarried'),
            ('married', 'Married')
        ]
        , verbose_name="Marital Status", default='unmarried')
    
    
    class Meta:
        verbose_name = "Staff"
        verbose_name_plural = "Staff"
    
    def __str__(self):
        return f"Staff: {self.first_name} {self.last_name} ({self.user_id})"
    
    
class StaffQualification(models.Model):
    """
    Model to store staff qualifications. Like CV(Resume), Certificates and other documents
    """
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='qualification')
    qualification_type = models.CharField(
        max_length=50, choices=[
            ('cv', 'CV'),
            ('certificate', 'Certificate'),
            ('recommendation_letter', 'Recommendation Letter'),
            ('other', 'Other')
        ], verbose_name="Qualification Type"
    )
    qualification_file = models.FileField(
        upload_to='staff/qualifications/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'])],
        verbose_name="Qualification File")