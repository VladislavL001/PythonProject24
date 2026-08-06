FROM python:3.14-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false
RUN poetry install --no-root --without lint --without dev

COPY . .

WORKDIR /app/myproject

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]