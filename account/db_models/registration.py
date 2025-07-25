from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import AbstractBaseUser

from account.db_models import mini_models,location,cloudinary_field
from account.accessories_codes import id_generator,mini_functions
from account.accessories_codes import id_generator



class PendingStudent(AbstractBaseUser):
    temp_id = models.CharField(editable=False)
    # Personal information fields of the pending student
    first_name = models.CharField(max_length=30, verbose_name="First Name")
    middle_name = models.CharField(max_length=30, verbose_name="Middle Name", blank=True)
    last_name = models.CharField(max_length=30, verbose_name="Last Name")
    gender = models.CharField(
        max_length=10, choices=[("male","Male"),("female","Female")]
        )
    date_of_birth = models.DateField(verbose_name="Date of Birth")
    
    status = models.CharField(
        max_length=20, 
        choices=[("pending", "Pending"), ("approved", "Approved")],
        default="pending",
        verbose_name="Registration Status"
    )
    
    @property
    def fullname(self):
        """
        Returns the full name of the student.
        """
        return f"{self.first_name} {self.middle_name} {self.last_name}".strip()

class PendingStudentRegistrationInformation(models.Model):
    
    
    # Registration information fields
    pending_student = models.ForeignKey(
        PendingStudent, on_delete=models.CASCADE, related_name="registration_info"
        )
    info_type = models.CharField(
        max_length=50, choices=[
            ("exit_letter", "Exit Letter"),
            ("Certificate", "Certificate"),
            ("support_letter", "Support Letter"),
            ("birth_certificate", "Birth Certificate"),
            ("other", "Other")]
    )
    info_file = cloudinary_field.CustomCloudinaryField(
        'file',
        upload_func=mini_functions.get_file_upload_directory_path,
        category='registration',
        user_type='student',
        prefix='pending/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'])],
        quality=50)
    
    @property
    def fullname(self):
        return self.pending_student.fullname