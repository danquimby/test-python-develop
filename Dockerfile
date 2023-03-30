# syntax=docker/dockerfile:experimental

FROM python:3.9.7


ENV PIPENV_VENV_IN_PROJECT 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip && pip install --no-cache-dir pipenv=="2021.5.29"
WORKDIR /opt/app

COPY Pipfile .
COPY Pipfile.lock .

RUN --mount=type=ssh pipenv install --deploy --ignore-pipfile

COPY . .
ENV PYTHONPATH=/opt/app/

CMD ["pipenv", "run", "main"]
