from django.db import models
from django.conf import settings
from course.models import Course

class VirtualClassroom(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    duration = models.IntegerField(help_text="Duration in minutes")
    is_active = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['-start_time']

class Recording(models.Model):
    classroom = models.ForeignKey(VirtualClassroom, on_delete=models.CASCADE)
    file = models.FileField(upload_to='classroom_recordings/')
    recorded_at = models.DateTimeField(auto_now_add=True)
