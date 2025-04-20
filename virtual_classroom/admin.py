from django.contrib import admin
from .models import VirtualClassroom

@admin.register(VirtualClassroom)
class VirtualClassroomAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'start_time', 'is_active', 'created_by')
    list_filter = ('is_active', 'course', 'created_by')
    search_fields = ('title', 'course__title')
