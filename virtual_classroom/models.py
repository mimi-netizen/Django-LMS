from django.db import models
from django.conf import settings
from django.utils import timezone
from course.models import Course
from django.urls import reverse

class VirtualClassroom(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='virtual_classes')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    duration = models.IntegerField(help_text="Duration in minutes")
    is_active = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='attended_sessions', blank=True)
    chat_messages = models.ManyToManyField('ChatMessage', related_name='classroom_chats', blank=True)

    class Meta:
        ordering = ['-start_time']

    def __str__(self):
        return f"{self.course.title} - {self.title}"

    def get_absolute_url(self):
        return reverse('virtual_classroom:classroom_detail', kwargs={'pk': self.pk})

    def activate_session(self):
        self.is_active = True
        self.save()

    def deactivate_session(self):
        self.is_active = False
        self.save()

class Recording(models.Model):
    classroom = models.ForeignKey(VirtualClassroom, on_delete=models.CASCADE, related_name='recordings')
    file = models.FileField(upload_to='classroom_recordings/')
    recorded_at = models.DateTimeField(auto_now_add=True)

class ChatMessage(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']
