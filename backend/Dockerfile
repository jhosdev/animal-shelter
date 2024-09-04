# syntax = docker/dockerfile:1.2

FROM python:3.12-alpine

WORKDIR /app

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN --mount=type=secret,id=_env,dst=/app/.env cat /app/.env

RUN chmod +x /app/script.sh

EXPOSE 8000

CMD ["./script.sh"]