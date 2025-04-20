from django.urls import path
from . import views

app_name = 'virtual_classroom'

urlpatterns = [
    path('', views.ClassroomListView.as_view(), name='classroom_list'),
    path('create/', views.ClassroomCreateView.as_view(), name='classroom_create'),
    path('<int:pk>/', views.ClassroomDetailView.as_view(), name='classroom_detail'),
    path('<int:classroom_id>/save-recording/', views.save_recording, name='save_recording'),
]
