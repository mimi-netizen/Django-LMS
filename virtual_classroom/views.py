from django.views.generic import ListView, CreateView, DetailView, View, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.conf import settings
from django.utils.translation import gettext_lazy as _  # Add this import
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.urls import reverse_lazy
from .models import VirtualClassroom, Recording
from course.models import Course
import json
from .forms import VirtualClassroomForm

class ClassroomListView(LoginRequiredMixin, ListView):
    model = VirtualClassroom
    template_name = 'virtual_classroom/classroom_list.html'
    context_object_name = 'classrooms'

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return VirtualClassroom.objects.all()
        elif user.is_lecturer or user.is_superuser:  # Allow both lecturers and admins
            return VirtualClassroom.objects.filter(course__allocated_course__lecturer=user)
        else:  # student
            enrolled_courses = Course.objects.filter(students=user)
            return VirtualClassroom.objects.filter(course__in=enrolled_courses)

class ClassroomDetailView(LoginRequiredMixin, DetailView):
    model = VirtualClassroom
    template_name = 'virtual_classroom/classroom_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'ice_servers': settings.WEBRTC_ICE_SERVERS,
            'room_id': self.object.id,
            'is_lecturer': self.request.user.is_lecturer,
        })
        return context

    def get(self, request, *args, **kwargs):
        classroom = self.get_object()
        if not classroom.is_active and not (request.user.is_lecturer or request.user.is_superuser):
            messages.error(request, 'This classroom session is not active.')
            return redirect('virtual_classroom:classroom_list')
        return super().get(request, *args, **kwargs)

class ClassroomCreateView(LoginRequiredMixin, CreateView):
    model = VirtualClassroom
    template_name = 'virtual_classroom/classroom_form.html'
    form_class = VirtualClassroomForm
    success_url = '/classroom/'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class ClassroomUpdateView(LoginRequiredMixin, UpdateView):
    model = VirtualClassroom
    template_name = 'virtual_classroom/classroom_form.html'
    form_class = VirtualClassroomForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Edit Virtual Classroom')  # Now using translated string
        return context

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user.is_superuser or (request.user.is_lecturer and obj.created_by == request.user):
            return super().dispatch(request, *args, **kwargs)
        return redirect('virtual_classroom:classroom_list')

class ClassroomActivateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        classroom = get_object_or_404(VirtualClassroom, pk=pk)
        if request.user.is_superuser or (request.user.is_lecturer and classroom.created_by == request.user):
            classroom.activate_session()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error'}, status=403)

class ClassroomDeactivateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        classroom = get_object_or_404(VirtualClassroom, pk=pk)
        if request.user.is_superuser or (request.user.is_lecturer and classroom.created_by == request.user):
            classroom.deactivate_session()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error'}, status=403)

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
