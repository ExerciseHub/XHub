#!/bin/bash

# 컨테이너 종료 및 최신화
docker compose down
docker compose pull

# 컨테이너 실행
docker compose up -d

# migration 실행
docker compose run django python manage.py makemigrations
docker compose run django python manage.py migrate