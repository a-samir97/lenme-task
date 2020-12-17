from django.utils import timezone

from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response

from users.models import User

from .models import Loan
from .utils import schedule_payment
from .permissions import (
    IsBorrower,
    IsInvestor,
    IsOwner
)
from .serializers import (
    LoanCreateSerializer,
    LoanSerializer
)

class LoanAPIViewSet(viewsets.ModelViewSet):
    
    '''
     Loan Viewset : 
        - create: borrower can make a loan request
        - delete: borrower can delete a requested loan
        - list : get all loan requests
        - get : get specific loan request by id
        - upadte : borrower can update a requested loan 
    '''

    def get_serializer_class(self):
        if self.action == 'create':
            return LoanCreateSerializer
        else:
            return LoanSerializer
    
    def get_queryset(self):
        return Loan.objects.all()


class InvestorMakeOffer(APIView):
    '''
        Investor make offer for a specific loan request
    '''
    permission_classes = (IsInvestor,)

    def post(self, request, loan_id):

        investor = request.user

        try:
            loan_object = Loan.objects.get(id=loan_id)
        
        except Loan.DoesNotExist:
            return Response(
                {'error': 'Loan id does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )

        # check if the balance of the investor is sufficient or not
        is_sufficient = loan_object.check_investor_balance(investor)

        if is_sufficient:
            # put the investor to the requested investors list for the specific loan
            loan_object.requested_investors.add(investor)
            return Response(
                {'data': '%s has make offer for the loan request' %(investor.username,) },
                status=status.HTTP_200_OK
            )
        else:
            # return bad request response , investor's balance is not enough 
            return Response(
                {'error': '%s balance is not enough' %(investor.username,)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
class InvestorOffersForSpecificLoan(APIView):
    '''
        To get all investors requests for a specific loan 
    '''
    def get(self, request, loan_id):
        try:
            get_loan = Loan.objects.get(id=loan_id)
            loan_serializer = LoanSerializer(get_loan)
            return Response(
                {'data': loan_serializer.data},
                status=status.HTTP_200_OK
            )

        except Loan.DoesNotExist:
            return Response(
                {'error': 'Loan id is not exists'},
                status=status.HTTP_404_NOT_FOUND
            )

class BorrowerAcceptTheOffer(APIView):
    '''
        Borrower accept the offer from requested investor offers 
    '''
    
    permission_classes = (IsOwner, IsBorrower)
    
    def post(self, request, loan_id):

        # check if the requested data contains investor_id
        investor_id = request.data.get('investor_id')
        if not investor_id:
            return Response (
                {"error": 'please provide investor id'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # get loan by loan_id
        try:
            loan_object = Loan.objects.get(id=loan_id)
            self.check_object_permissions(request, loan_object)

            # check if the load has investor 
            if loan_object.investor:
                return Response(
                    {'details': 'this loan has an investor'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Loan.DoesNotExist:
            return Response(
                {'error': 'Loan id is not exists'},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            # get investor id from requested data
            investor_obj = User.objects.get(id=investor_id, user_type='I')
            # check if the investor in the requested investors to this loan
            if investor_obj in loan_object.requested_investors.all():
                
                loan_object.investor = investor_obj
                
                loan_object.borrower_accepted_at = timezone.now()

                # change status of the loan to funded
                loan_object.status = 'F'

                # take total amount loan from investor balance 
                investor_obj.balance -= loan_object.calculate_total_loan_amount()
                
                investor_obj.save()
                loan_object.save()

                # make schedule for borrower payments
                schedule_payment(loan_object)

                return Response(
                    {'data': '%s accept offer from %s' %(loan_object.borrower.username, investor_obj.username)},
                    status=status.HTTP_200_OK
                )

            # else if investor does not exist in requested investors
            else:
                return Response(
                    {'error': 'Selected investor does not exit in the requested investors list'},
                    status=status.HTTP_404_NOT_FOUND
                )

        except User.DoesNotExist:
            return Response(
                {'error': 'Investor id is not exists'},
                status=status.HTTP_404_NOT_FOUND
            )
