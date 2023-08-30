# celery.py
import os
from django.conf import settings

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

# 이 부분은 Django의 settings.py 파일을 사용하여 Celery를 구성합니다.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Django의 앱 config에서 task 모듈을 로드합니다.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
