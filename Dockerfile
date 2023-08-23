# 공식 Python 런타임을 기반 이미지로 사용합니다.
FROM alpine:3.18

# 환경 변수 설정
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=core.settings

# Python 및 PostgreSQL에 필요한 시스템 패키지를 설치합니다.
RUN apk update \
    && apk add --no-cache python3 py3-pip python3-dev \
    && apk add --no-cache postgresql-dev gcc musl-dev jpeg-dev zlib-dev \
    && python3 -m ensurepip \
    && pip3 install --no-cache --upgrade pip setuptools

# 컨테이너 내 작업 디렉토리를 /app으로 설정합니다.
WORKDIR /app

# 현재 디렉토리의 내용을 컨테이너의 /app에 복사합니다.
COPY . /app

# requirements.txt에 지정된 패키지를 설치합니다.
RUN pip install -r requirements.txt

# 컨테이너 외부에서 8000 포트에 액세스할 수 있도록 합니다.
EXPOSE 8000

# Django 서버를 시작하는 명령을 실행합니다.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
