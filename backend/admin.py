from django.contrib import admin
from backend.db_models import mini_models
from backend import models
@admin.register(mini_models.IDTracker)
class IDTrackerAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Disable add if instance already exists
        return not mini_models.IDTracker.objects.exists()
    def has_delete_permission(self, request, obj = ...):
        return False  # Disable delete permission
admin.site.register(mini_models.Occupation)

admin.site.register(models.User)
admin.site.register(models.Staff)
admin.site.register(models.StaffQualification)