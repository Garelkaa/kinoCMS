from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# Установите переменную окружения для Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kinoCMS.settings')

# Создайте экземпляр Celery
app = Celery('kinoCMS')

# Укажите брокера сообщений как Redis
app.conf.broker_url = 'redis://localhost:6379/0'

# Укажите backend как Redis для хранения результатов выполнения задач
app.conf.result_backend = 'redis://localhost:6379/0'

# Укажите список модулей, которые Celery будет автоматически искать задачи
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
