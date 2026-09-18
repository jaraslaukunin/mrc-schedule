from django.db import models
from django.db.models import Sum

class Teacher(models.Model):
    name = models.CharField(max_length=100)

    @property
    def total_hours(self):
        # Исправлено: используем academicplan_set вместо plans
        return self.academicplan_set.aggregate(total=Sum('total_hours'))['total'] or 0

    @property
    def plans(self):
        # Добавлен метод plans для совместимости с шаблонами
        return self.academicplan_set.all()

    def __str__(self):
        return self.name


class Subject(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Group(models.Model):
    name = models.CharField(max_length=50)
    specialty = models.CharField(max_length=255, blank=True)
    curator = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='curated_groups')

    @property
    def plans(self):
        return self.academicplan_set.all()

    def __str__(self):
        return self.name


class AcademicPlan(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name="Группа", related_name='academicplan_set')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Предмет")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="Преподаватель")
    total_hours = models.PositiveIntegerField(verbose_name="Часов по плану")

    class Meta:
        verbose_name = "Учебный план"
        verbose_name_plural = "Учебные планы"
        constraints = [models.UniqueConstraint(fields=['group', 'subject', 'teacher'], name='unique_plan')]

    def __str__(self):
        return f"{self.group} - {self.subject} ({self.total_hours} ч.)"


class Schedule(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    date = models.DateField(verbose_name="Дата занятия", db_index=True)

    duration = models.CharField(
        max_length=10,
        choices=[('half1', '1 половина'), ('half2', '2 половина'), ('full', 'Полная пара')],
        default='full'
    )
    time = models.TimeField()
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    classroom_number = models.CharField(max_length=20, verbose_name="Аудитория", blank=True)
    classroom_floor = models.IntegerField(verbose_name="Этаж", blank=True, null=True)
    building = models.CharField(max_length=50, verbose_name="Корпус", blank=True)

    class Meta:
        ordering = ['date', 'time']

    def __str__(self):
        return f"{self.date} - {self.group} - {self.subject}"

    def get_classroom_full(self):
        parts = []
        if self.building: parts.append(f"Корпус {self.building}")
        if self.classroom_number: parts.append(f"ауд. {self.classroom_number}")
        return ", ".join(parts) if parts else "Не указана"