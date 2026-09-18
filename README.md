# 📅 Расписание МРК

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)
[![GitHub repository](https://img.shields.io/badge/GitHub-mrc--schedule-181717?style=for-the-badge&logo=github)](https://github.com/jaraslaukunin/mrc-schedule)

Веб-приложение для удобного просмотра расписания занятий **Минского радиотехнического колледжа**.

> **Автор:** jaraslaukunin  
> **Группа:** 4К9392  
> **Версия:** 1.3


---

## Содержание

- [Возможности](#возможности)
- [Технологии](#технологии)
- [Быстрый запуск](#быстрый-запуск)
- [Доступные адреса](#доступные-адреса)
- [Структура проекта](#структура-проекта)
- [Вклад в проект](#вклад-в-проект)
- [Лицензия](#лицензия)
- [Автор](#автор)

---

## Возможности

| Раздел | Возможность |
|---|---|
| Учебные группы | Просмотр расписания занятий выбранной группы |
| Преподаватели | Поиск и просмотр занятий конкретного преподавателя |
| Дисциплины | Просмотр расписания по учебному предмету |
| Матрица расписания | Сводное отображение занятий в формате «группы × пары» |
| Половины занятия | Поддержка занятий в первой и второй половине пары: `half1` и `half2` |
| Выбор даты | Просмотр расписания на сегодня, завтра или указанную дату |
| Адаптивный интерфейс | Удобная работа на компьютерах, планшетах и смартфонах |
| Интерфейс | Современное оформление, плавные анимации и понятная навигация |

---

## Технологии

- **Python 3.13**
- **Django 6**
- **SQLite** — база данных для локального запуска
- **HTML5**
- **CSS3**
- **Bootstrap Icons**
- **Google Fonts**
- Адаптивная вёрстка без CSS-фреймворков

---

## Быстрый запуск

### Требования

Перед запуском убедитесь, что установлены:

- Python 3.13 или новее;
- Git;
- `pip`.

### 1. Клонирование репозитория

```bash
git clone [https://github.com/jaraslaukunin/mrc-schedule.git](https://github.com/jaraslaukunin/mrc-schedule.git)
cd mrc-schedule
```

### 2. Создание виртуального окружения

```bash
python -m venv venv
```

### 3. Активация виртуального окружения

**Windows (PowerShell):**

```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (cmd):**

```bat
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

### 4. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 5. Применение миграций

```bash
python manage.py migrate
```

### 6. Создание администратора

Этот шаг необязателен, но нужен для добавления и редактирования расписания через Django Admin.

```bash
python manage.py createsuperuser
```

### 7. Запуск сервера разработки

```bash
python manage.py runserver
```

После запуска откройте приложение в браузере.

---

## Доступные адреса

| Раздел | Адрес |
|---|---|
| Главная страница | [http://127.0.0.1:8000/](http://127.0.0.1:8000/) |
| Панель администратора | [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) |

---

## Структура проекта

```text
mrc-schedule/
├── manage.py
├── requirements.txt
├── db.sqlite3
├── LICENSE
├── README.md
│
├── schedule/                    # Приложение расписания
│   ├── migrations/              # Миграции базы данных
│   ├── static/                  # CSS, JavaScript, изображения
│   ├── templates/               # HTML-шаблоны
│   ├── admin.py                 # Настройка Django Admin
│   ├── apps.py
│   ├── models.py                # Модели данных
│   ├── urls.py                  # Маршруты приложения
│   └── views.py                 # Обработчики страниц
│
└── config/                      # Конфигурация Django-проекта
    ├── settings.py
    ├── urls.py
    ├── asgi.py
    └── wsgi.py
```

> Фактическая структура может незначительно отличаться в зависимости от версии проекта.

---

## Вклад в проект

Предложения, исправления и Pull Request’ы приветствуются.

1. Сделайте fork репозитория.
2. Создайте отдельную ветку:

   ```bash
   git checkout -b feature/название-функции
   ```

3. Внесите изменения и создайте коммит:

   ```bash
   git add .
   git commit -m "Добавлена новая функция"
   ```

4. Отправьте ветку в свой fork:

   ```bash
   git push origin feature/название-функции
   ```

5. Откройте Pull Request в репозиторий  
   [jaraslaukunin/mrc-schedule](https://github.com/jaraslaukunin/mrc-schedule).

---

## Лицензия

Проект распространяется под лицензией [MIT](LICENSE).

Вы можете свободно использовать, изменять и распространять код при сохранении текста лицензии и информации об авторских правах.

---

## Автор

**jaraslaukunin**  
УО БГУИР, филиал «Минский радиотехнический колледж»  
Группа **4К9392**  
Специальность: *Разработка и сопровождение программного обеспечения информационных систем*

<p align="center">
  <a href="https://github.com/jaraslaukunin/mrc-schedule">
    <img
      src="https://img.shields.io/badge/Открыть_репозиторий_на_GitHub-181717?style=for-the-badge&logo=github&logoColor=white"
      alt="Открыть репозиторий на GitHub"
    />
  </a>
</p>

<p align="center">
  Если проект оказался полезным — поставьте ⭐ на GitHub.
</p>
