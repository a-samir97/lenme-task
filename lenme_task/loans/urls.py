from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import (
    LoanAPIViewSet,
    InvestorOffersForSpecificLoan,
    BorrowerAcceptTheOffer,
    InvestorMakeOffer,
)

router = DefaultRouter()

router.register('', LoanAPIViewSet, basename='loans')

urlpatterns = [
    path('investors-offers/<int:loan_id>/', InvestorOffersForSpecificLoan.as_view()),
    path('accept-offer/<int:loan_id>/', BorrowerAcceptTheOffer.as_view()),
    path('investor-offer/<int:loan_id>/', InvestorMakeOffer.as_view()),
]

urlpatterns += router.urls