from django.shortcuts import render, get_object_or_404
from django.db.models import Sum, Case, When, IntegerField
from .models import Schedule, Group, Teacher, Subject, AcademicPlan
from datetime import datetime, time, timedelta
from django.utils import timezone
import pytz
import locale

# Настройка временных интервалов для пар
LESSON_TIMES = [
    {'num': 1, 'start': time(8, 0), 'end': time(9, 40)},
    {'num': 2, 'start': time(9, 50), 'end': time(11, 30)},
    {'num': 3, 'start': time(11, 50), 'end': time(13, 30)},
    {'num': 4, 'start': time(13, 40), 'end': time(15, 20)},
    {'num': 5, 'start': time(15, 40), 'end': time(17, 20)},
    {'num': 6, 'start': time(17, 30), 'end': time(19, 10)},
    {'num': 7, 'start': time(19, 20), 'end': time(21, 00)},
]

DAYS_FULL = {
    0: 'Понедельник', 1: 'Вторник', 2: 'Среда',
    3: 'Четверг', 4: 'Пятница', 5: 'Суббота', 6: 'Воскресенье'
}


def get_stats(group_id=None, teacher_id=None):
    """Подсчет вычитанных часов на основе AcademicPlan"""
    filters = {}
    if group_id: filters['group_id'] = group_id
    if teacher_id: filters['teacher_id'] = teacher_id

    plans = AcademicPlan.objects.filter(**filters).select_related('group', 'subject', 'teacher')
    results = []
    for p in plans:
        spent = Schedule.objects.filter(
            group=p.group, subject=p.subject, teacher=p.teacher
        ).aggregate(
            total=Sum(Case(When(duration='full', then=2), default=1, output_field=IntegerField()))
        )['total'] or 0

        results.append({
            'plan': p,
            'spent': spent,
            'remains': p.total_hours - spent,
            'percent': int((spent / p.total_hours * 100)) if p.total_hours > 0 else 0
        })
    return results


def get_selected_date(request):
    """Утилита для определения даты из GET-запроса"""
    date_mode = request.GET.get("date_mode", "today")
    custom_date = request.GET.get("custom_date")
    today = datetime.now().date()

    if date_mode == "tomorrow":
        return today + timedelta(days=1), date_mode
    elif date_mode == "custom" and custom_date:
        try:
            return datetime.strptime(custom_date, "%Y-%m-%d").date(), date_mode
        except ValueError:
            pass
    return today, "today"


def is_current_lesson(lesson_start, lesson_end, lesson_date, selected_date):
    """Проверяет, идет ли сейчас это занятие"""
    from datetime import datetime

    # Получаем текущее московское время (UTC+3)
    now_utc = datetime.utcnow()
    now_msk = datetime(now_utc.year, now_utc.month, now_utc.day,
                       now_utc.hour + 3, now_utc.minute, now_utc.second)
    now = now_msk.time()
    today = now_msk.date()

    # Только для сегодняшней даты
    if lesson_date != today:
        return False

    # Проверяем, попадает ли текущее время в интервал
    if lesson_start <= now <= lesson_end:
        return True
    return False


# --- ПРЕДСТАВЛЕНИЯ ---

def schedule_view(request):
    """Главная страница расписания группы"""
    selected_date, date_mode = get_selected_date(request)
    group_id = request.GET.get("group", 1)

    schedule_qs = Schedule.objects.filter(
        date=selected_date,
        group_id=group_id
    ).select_related('subject', 'teacher')

    table = []
    for lt in LESSON_TIMES:
        lessons = [s for s in schedule_qs if lt['start'] <= s.time < lt['end']]

        # Проверяем, идет ли сейчас эта пара
        is_now = is_current_lesson(lt['start'], lt['end'], selected_date, selected_date)

        table.append({
            'num': lt['num'],
            'time_range': f"{lt['start'].strftime('%H:%M')} - {lt['end'].strftime('%H:%M')}",
            'lessons': lessons,
            'is_now': is_now  # Добавляем флаг
        })

    return render(request, "schedule/schedule.html", {
        "groups": Group.objects.all().order_by('name'),
        "schedule_table": table,
        "selected_group": int(group_id) if str(group_id).isdigit() else group_id,
        "selected_group_obj": Group.objects.filter(id=group_id).first(),
        "selected_day_full": DAYS_FULL[selected_date.weekday()],
        "today_date": selected_date.strftime("%d.%m.%Y"),
        "hours_stats": get_stats(group_id=group_id),
        "date_mode": date_mode,
        "custom_date": request.GET.get("custom_date", "")
    })


def teacher_detail(request, teacher_id):
    """Детальная страница преподавателя с фильтром по датам"""
    teacher = get_object_or_404(Teacher, id=teacher_id)
    selected_date, date_mode = get_selected_date(request)

    current_schedule = Schedule.objects.filter(
        teacher=teacher,
        date=selected_date
    ).select_related('group', 'subject')

    table = []
    for lt in LESSON_TIMES:
        lessons = [s for s in current_schedule if lt['start'] <= s.time < lt['end']]

        # Проверяем, идет ли сейчас эта пара
        is_now = is_current_lesson(lt['start'], lt['end'], selected_date, selected_date)

        table.append({
            'num': lt['num'],
            'time_range': f"{lt['start'].strftime('%H:%M')} - {lt['end'].strftime('%H:%M')}",
            'lessons': lessons,
            'is_now': is_now  # Добавляем флаг
        })

    return render(request, 'schedule/teacher_detail.html', {
        'teacher': teacher,
        'schedule_table': table,
        'hours_info': get_stats(teacher_id=teacher_id),
        'selected_date': selected_date.strftime("%d.%m.%Y"),
        'selected_day_full': DAYS_FULL[selected_date.weekday()],
        'date_mode': date_mode,
        'custom_date': request.GET.get("custom_date", "")
    })


def matrix_view(request):
    """Общая матрица всех групп на выбранный день"""
    selected_date, date_mode = get_selected_date(request)
    groups = Group.objects.all().order_by('name')
    schedule_qs = Schedule.objects.filter(date=selected_date).select_related('subject', 'teacher', 'group')

    now_utc = datetime.utcnow()
    now_msk = now_utc + timedelta(hours=3)
    now_time = now_msk.time()
    now_date = now_msk.date()

    is_today = (selected_date == now_date)

    lesson_times_with_flag = []
    for lt in LESSON_TIMES:
        is_now = is_today and (lt['start'] <= now_time <= lt['end'])
        lesson_times_with_flag.append({
            'num': lt['num'],
            'start': lt['start'],
            'end': lt['end'],
            'is_now': is_now
        })

    matrix = []
    for g in groups:
        slots = []
        for idx, lt in enumerate(LESSON_TIMES):
            lessons = [s for s in schedule_qs if s.group_id == g.id and lt['start'] <= s.time < lt['end']]
            slots.append({
                'lessons': lessons,
                'is_now': lesson_times_with_flag[idx]['is_now']
            })
        matrix.append({'group': g, 'slots': slots})

    return render(request, 'schedule/matrix.html', {
        'matrix': matrix,
        'lesson_times': lesson_times_with_flag,
        'selected_date': selected_date.strftime("%d.%m.%Y"),
        'selected_day_full': DAYS_FULL[selected_date.weekday()],
        'date_mode': date_mode,
        'custom_date': request.GET.get("custom_date", "")
    })


def teachers_list(request):
    return render(request, 'schedule/teachers.html', {'teachers': Teacher.objects.all().order_by('name')})


def groups_list(request):
    return render(request, 'schedule/groups.html', {'groups': Group.objects.all().order_by('name')})


def subjects_list(request):
    return render(request, 'schedule/subjects.html', {'subjects': Subject.objects.all().order_by('title')})


def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    return render(request, 'schedule/group_detail.html', {
        'group': group,
        'hours_info': get_stats(group_id=group_id)
    })


def subject_detail(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    groups = Group.objects.filter(plans__subject=subject).distinct()
    return render(request, 'schedule/subject_detail.html', {'subject': subject, 'groups': groups})