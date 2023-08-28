from django.urls import path
from .views import BorrowerView, InvestorView, LoanView, LoanFundedView, PaymentView

urlpatterns = [
    path('borrowers/', BorrowerView.as_view(), name='borrower'),
    path('investors/', InvestorView.as_view(), name='investor'),
    path('loans/', LoanView.as_view(), name='loan'),
    path('loans_funded/', LoanFundedView.as_view(), name='loan_funded'),
    path('payments/', PaymentView.as_view(), name='payment'),
]