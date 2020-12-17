from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    '''
        User can be Investor or Borrower
        - Inverstor : accept loan request from borrowers 
        - Borrower : make a loan reuqest 
    '''

    USER_TYPES = (
        ('I','Inverstor'),
        ('B', 'Borrower')
    )

    user_type = models.CharField(choices=USER_TYPES, max_length=1)
    balance = models.FloatField(default=0)

    # if user is investor 
    annual_interest_rate = models.FloatField(default=0)

    def __str__(self):
        return self.username


'''
class User(AbstractUser):

    class Meta:
        abstract = True

class Investor(User):

    balance = models.PositiveIntegerField(default=0)
    annual_interest_rate = models.PositiveIntegerField(default=0)

class Borrower(User):

    balance = models.PositiveIntegerField(default=0)

'''