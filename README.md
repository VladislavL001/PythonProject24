# LMS API

REST API для системы онлайн-обучения, разработанный на Django REST Framework.

## Используемые технологии

* Python 3.14
* Django 6
* Django REST Framework
* PostgreSQL
* Redis
* Celery
* Celery Beat
* Docker
* Docker Compose
* Poetry

## Запуск проекта

### 1. Клонировать репозиторий

```bash
git clone <ссылка_на_репозиторий>
cd PythonProject24
```

### 2. Создать файл `.env`

Пример содержимого:

```env
SECRET_KEY=your_secret_key

POSTGRES_DB=lms
POSTGRES_USER=postgres
POSTGRES_PASSWORD=12345678

DB_HOST=db
DB_PORT=5432

REDIS_HOST=redis
REDIS_PORT=6379

STRIPE_SECRET_KEY=your_stripe_secret_key

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=your_email@gmail.com
```

### 3. Собрать и запустить контейнеры

```bash
docker compose up --build
```

После запуска автоматически:

* запускается PostgreSQL;
* запускается Redis;
* выполняются миграции Django;
* запускается Celery Worker;
* запускается Celery Beat;
* запускается Django.

## Создание суперпользователя

В новом терминале выполните:

```bash
docker compose exec web python manage.py createsuperuser
```

## Остановка проекта

```bash
docker compose down
```

## Структура сервисов

* **web** — Django-приложение;
* **db** — PostgreSQL;
* **redis** — Redis;
* **celery** — Celery Worker;
* **celery-beat** — Celery Beat Scheduler.

## Доступ к приложению

Главная страница:

```
http://localhost:8000/
```

Административная панель:

```
http://localhost:8000/admin/
```

## Используемые Docker Volume

* `postgres_data` — хранение данных PostgreSQL.
* `redis_data` — хранение данных Redis.
