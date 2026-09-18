from django.contrib import admin
from .models import Teacher, Subject, Group, Schedule, AcademicPlan

try:
    admin.site.unregister(Teacher)
    admin.site.unregister(Subject)
    admin.site.unregister(Group)
    admin.site.unregister(Schedule)
except: pass

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialty')
    search_fields = ('name',)

@admin.register(AcademicPlan)
class AcademicPlanAdmin(admin.ModelAdmin):
    list_display = ('group', 'subject', 'teacher', 'total_hours')
    list_filter = ('group', 'teacher')

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('date', 'time', 'group', 'subject', 'teacher', 'duration')
    list_filter = ('date', 'group', 'teacher')
    search_fields = ('group__name', 'subject__title', 'teacher__name')