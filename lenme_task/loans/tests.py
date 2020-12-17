from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User

from .models import Loan


class LoanTests(APITestCase):

    def setUp(self):
        self.investor = User.objects.create(
            username='investortest',
            password='investorpassword',
            balance=10000,
            annual_interest_rate=15.0,
            user_type='I' # investor
        )

        self.borrower = User.objects.create(
            username='borrowertest',
            password='borrowerpassword',
            balance=0,
            user_type='B' # borrower
        )

        self.high_loan = Loan.objects.create(
            borrower=self.borrower,
            loan_amount=150000,
            loan_period=10
        )

        self.low_loan = Loan.objects.create(
            borrower=self.borrower,
            loan_amount=5000,
            loan_period=6
        )

        # to make a loan (URL) 
        self.create_loan_url = '/api/loans/'

        # investor make an offer (URL)
        self.investor_offer_url = '/api/loans/investor-offer/'

        # borrower accept offer from investor (URL)
        self.borrower_accept_url = '/api/loans/accept-offer/'

    def test_borrower_create_loan_request(self):
        self.client.login(username='borrowertest', password='borrowerpassword')
        data = {
            'borrower':self.borrower.id,
            'loan_amount':5000,
            'loan_period':6
        }

        response = self.client.post(self.create_loan_url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Loan.objects.count(), 3)

    def test_investor_make_valid_offer(self):
        self.client.force_login(user=self.investor)

        url = self.investor_offer_url + str(self.low_loan.id) + '/'
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.investor, self.low_loan.requested_investors.all())

    # investor's balance is not enough
    def test_investor_make_invalid_offer(self):
        self.client.force_login(user=self.investor)

        url = self.investor_offer_url + str(self.high_loan.id) + '/'
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn(self.investor, self.low_loan.requested_investors.all())
    
    # borrower accept offer 
    def test_borrower_accept_offer(self):
        self.test_investor_make_valid_offer()
        
        self.client.force_login(user=self.borrower)

        url = self.borrower_accept_url + str(self.low_loan.id) + '/'

        data = {
            "investor_id": 1
        }

        response = self.client.post(url, data=data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data'], 'borrowertest accept offer from investortest')

    # borrower accept invalid offer
    def test_borrower_accept_offer_invalid_investor(self):
        self.test_investor_make_valid_offer()
        
        self.client.force_login(user=self.borrower)

        url = self.borrower_accept_url + str(self.low_loan.id) + '/'

        data = {
            "investor_id": 3
        }

        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Investor id is not exists')
    