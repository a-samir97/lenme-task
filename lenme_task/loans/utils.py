from django_celery_beat.models import PeriodicTask, IntervalSchedule

from datetime import datetime, timedelta

import json

def schedule_payment(loan_object):
    
    schedule, created = IntervalSchedule.objects.get_or_create(
            every=30,
            period=IntervalSchedule.DAYS,
    )
    
    PeriodicTask.objects.create(
            interval=schedule,                  
            name='loan_id:%s' %(loan_object.id,),          
            task='loans.tasks.schedule_borrower_payment_every_month',
            args=json.dumps([loan_object.id]),
            # schedule expires after completing loan_period
            expires=datetime.utcnow() + timedelta(days=30*loan_object.loan_period)
    )