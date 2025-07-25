from django.db import models
from django.core.exceptions import ValidationError


class Occupation(models.Model):
    occupation_choices = [
        ("private", "Private"),
        ("government", "Government"),
        ("unoccupied", "Unoccupied"),]
    occupation = models.CharField(max_length=100, choices=occupation_choices, verbose_name="Occupation Name")
    
    
    def __str__(self):
        return self.occupation

class IDTracker(models.Model):
    user_type = models.CharField(max_length=50, 
                                 choices=[('staff', 'Staff'), ('guardian', 'Guardian'), ('student', 'Student')], 
                                 default='student', 
                                 verbose_name="User Type",
                                 unique=True)
    last_id = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Last index: {self.last_id}"