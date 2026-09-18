from django.urls import path
from . import views

urlpatterns = [
    path('', views.schedule_view, name='schedule'),
    path('teachers/', views.teachers_list, name='teachers'),
    path('teacher/<int:teacher_id>/', views.teacher_detail, name='teacher_detail'),
    path('subjects/', views.subjects_list, name='subjects'),
    path('groups/', views.groups_list, name='groups'),
    path('groups/<int:group_id>/', views.group_detail, name='group_detail'),
    path('subjects/<int:subject_id>/', views.subject_detail, name='subject_detail'),
    path('teachers/<int:teacher_id>/', views.teacher_detail, name='teacher_detail'),
    path('matrix/', views.matrix_view, name='matrix'),

]