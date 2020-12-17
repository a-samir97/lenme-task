from django.db import models

from users.models import User

LENME_FEE = 3

class Loan(models.Model):
    '''
    '''

    STATUES_TYPES = (
        ('F', 'Funded'),
        ('C', 'Completed'),
        ('R', 'Requested')
    )

    borrower = models.ForeignKey(User,on_delete=models.CASCADE, related_name='loan_requests')
    investor = models.ForeignKey(User,on_delete=models.SET_NULL, related_name='investing_loans', null=True)
    loan_amount = models.FloatField(default=0)
    loan_period = models.PositiveIntegerField() # in months
    status = models.CharField(choices=STATUES_TYPES, default='R', max_length=1)
    borrower_payments_till_now = models.IntegerField(default=0) #in months 

    requested_investors = models.ManyToManyField(User)
    borrower_accepted_at = models.DateField(null=True)

    def __str__(self):
        return "%s make a loan request" %(self.borrower.username,) 
    
    def calculate_total_loan_amount(self):
        return self.loan_amount + LENME_FEE

    def check_investor_balance(self, investor):
        return (investor.balance >= self.calculate_total_loan_amount())
    
    def borrower_monthly_payment(self):
        monthly_intereset_rate = (self.investor.annual_interest_rate / 12.0 ) / 100
        monthly_payment = (self.loan_amount / self.loan_period) + (self.loan_amount * monthly_intereset_rate)
        return monthly_payment
    
    def borrower_total_payment(self):
        monthly_intereset_rate = (self.investor.annual_interest_rate / 12.0 ) / 100
        total_payment = self.loan_amount + (self.loan_amount * monthly_intereset_rate) * loan_period
        return total_payment
    
    def check_borrower_payments_in_months(self):
        # if true, borrower has finished payment for this loan
        return (self.borrower_payments_till_now == self.loan_period)
    