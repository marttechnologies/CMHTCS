from django.contrib import admin
from account.db_models import mini_models
from account import models

@admin.register(models.StaffQualification)
class StaffQualificationAdmin(admin.ModelAdmin):
    
    def delete_model(self, request, obj):
        obj.delete()
    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()

admin.site.register(mini_models.Occupation)
admin.site.register(models.User)
admin.site.register(models.Staff)
admin.site.register(models.Student)
admin.site.register(models.StudentRegistrationInformation)