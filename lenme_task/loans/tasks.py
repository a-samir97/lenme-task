from celery import shared_task
from .models import Loan

from django_celery_beat.models import PeriodicTask

@shared_task(bind=True)
def schedule_borrower_payment_every_month(self, loan_id):
    
    # get the loan object 
    loan_object = Loan.objects.get(id=loan_id)

    # get monthly payment to the borrower
    monthly_payment = loan_object.borrower_monthly_payment()

    # take payment from the borrower
    loan_object.borrower.balance -= monthly_payment

    # increasing borrower payments till now every month
    loan_object.borrower_payments_till_now += 1

    # if the borrower has finished payments ...
    is_completed = loan_object.check_borrower_payments_in_months()

    if is_completed:
        # change status of the loan to completed
        loan_object.status = 'C'

        # to stop the schedule 
        PeriodicTask.objects.get(name='loan_id:%s'%(loan_id,)).delete()
        
    loan_object.save()

