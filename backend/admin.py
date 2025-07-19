from django.contrib import admin
from backend.db_models.mini_models import IDTracker

@admin.register(IDTracker)
class IDTrackerAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Disable add if instance already exists
        return not IDTracker.objects.exists()
    def has_delete_permission(self, request, obj = ...):
        return False  # Disable delete permission