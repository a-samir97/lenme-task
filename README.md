# Lenme Task

### How to run the project ?
- pip install -r requirements.txt
- celery -A lenme_task beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
- celery -A lenme_task worker -l info
- python3 manage.py makemigrations
- python3 manage.py migrate  
- python3 manage.py runserver
