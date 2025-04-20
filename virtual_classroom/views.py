from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.conf import settings  # Add this import
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from .models import VirtualClassroom, Recording
from course.models import Course
import json

class ClassroomListView(LoginRequiredMixin, ListView):
    model = VirtualClassroom
    template_name = 'virtual_classroom/classroom_list.html'
    context_object_name = 'classrooms'

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return VirtualClassroom.objects.all()
        elif user.is_lecturer:
            return VirtualClassroom.objects.filter(course__allocated_course__lecturer=user)
        else:  # student
            enrolled_courses = Course.objects.filter(students=user)
            return VirtualClassroom.objects.filter(course__in=enrolled_courses)

class ClassroomDetailView(LoginRequiredMixin, DetailView):
    model = VirtualClassroom
    template_name = 'virtual_classroom/classroom_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ice_servers'] = settings.WEBRTC_ICE_SERVERS  # Fix settings access
        return context

class ClassroomCreateView(LoginRequiredMixin, CreateView):
    model = VirtualClassroom
    template_name = 'virtual_classroom/classroom_form.html'
    fields = ['course', 'title', 'start_time', 'duration']
    success_url = '/classroom/'  # Add success_url

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

@require_http_methods(["POST"])
def save_recording(request, classroom_id):
    try:
        classroom = get_object_or_404(VirtualClassroom, id=classroom_id)
        recording_file = request.FILES.get('recording')
        
        if recording_file:
            recording = Recording.objects.create(
                classroom=classroom,
                file=recording_file
            )
            return JsonResponse({'status': 'success', 'recording_id': recording.id})
        
        return JsonResponse({'status': 'error', 'message': 'No recording file provided'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
