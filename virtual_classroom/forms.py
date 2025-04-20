from django import forms
from .models import VirtualClassroom

class VirtualClassroomForm(forms.ModelForm):
    start_time = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                'placeholder': '2025-04-20 00:00:00',
                'class': 'form-control'
            }
        )
    )

    class Meta:
        model = VirtualClassroom
        fields = ['course', 'title', 'description', 'start_time', 'duration']
