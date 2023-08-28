from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.db import transaction
from django.contrib.auth.models import User
from .models import Borrower, Investor, Loan, Payment
from .serializers import BorrowerSerializer, InvestorSerializer, LoanSerializer, PaymentSerializer

class BorrowerView(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        try:
            user = User.objects.get(id=user_id)
            if user:
                if Borrower.objects.filter(user=user):
                    return Response({"message": "User already exist"}, status=status.HTTP_400_BAD_REQUEST)
                
                borrower = Borrower.objects.create(user=user)
                return Response({"message": "Borrower created successfully", "borrower":borrower.id}, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        borrowers = Borrower.objects.all()
        serializer = BorrowerSerializer(borrowers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class InvestorView(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        account_balance = request.data.get("account_balance")
        try:
            user = User.objects.get(id=user_id)
            if user:
                if Investor.objects.filter(user=user):
                    return Response({"message": "User already exist"}, status=status.HTTP_400_BAD_REQUEST)
                
                investor = Investor.objects.create(user=user, account_balance=float(account_balance))
                return Response({"message": "Investor created successfully", "investor":investor}, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        investors = Investor.objects.all()
        serializer = InvestorSerializer(investors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LoanView(APIView):
    def post(self, request):
        borrower_id = request.data.get("borrower_id")
        loan_amount = request.data.get("loan_amount")
        loan_period = request.data.get("loan_period")
        lenme_fee = 3.0  # Assuming lenme fee is fixed
        
        borrower = Borrower.objects.get(id=borrower_id)
        loan = Loan.objects.create(borrower=borrower, loan_amount=loan_amount,
                                   loan_period=loan_period,
                                   lenme_fee=lenme_fee)
        loan.save()

        return Response({"message": "Loan Created successfully"}, status=status.HTTP_201_CREATED)
    
    def get(self, request):
        loans = Loan.objects.all()
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LoanFundedView(APIView):
    def post(self, request):
        loan_id = request.data.get("loan_id")
        investor_id = request.data.get("investor_id")
        loan_period = request.data.get("loan_period")
        annual_interest_rate = request.data.get("annual_interest_rate")
        lenme_fee = 3.0  # Assuming lenme fee is fixed
        
        loan = Loan.objects.get(id=loan_id)
        investor = Investor.objects.get(id=investor_id)
        monthly_interest_rate = annual_interest_rate / 12
        total_loan_amount = loan.loan_amount + (loan.loan_amount * monthly_interest_rate * loan_period) + lenme_fee
        loan.investor = investor
        loan.annual_interest_rate = annual_interest_rate
        loan.total_loan_amount = total_loan_amount
        loan.funded_date = timezone.now()
        loan.loan_status = "Funded"  # Change default value 
        loan.save()

        monthly_payment_amount = loan.total_loan_amount / loan.loan_period
        payment_duedate = loan.funded_date + timezone.timedelta(days=30)
        with transaction.atomic():
            for _ in range(loan.loan_period):
                Payment.objects.create(loan=loan, payment_duedate=payment_duedate, amount=monthly_payment_amount)
                payment_duedate = payment_duedate + timezone.timedelta(days=30)  # Assuming 30 days per month


        return Response({"message": "Loan funded successfully"}, status=status.HTTP_201_CREATED)

class PaymentView(APIView):
    def post(self, request):
        payment_id = request.data.get("payment_id")

        try:
            payment = Payment.objects.get(id=payment_id)
            payment.payment_date = timezone.now()
            payment.is_completed = True  # Change default value 
            payment.save()

            # Check if all payments are completed
            loan = payment.loan
            payments_remaining = Payment.objects.filter(loan=loan, is_completed=False).count()
            if payments_remaining == 0:
                loan.loan_status = "Completed"  # Change loan status value after all installments complete
                loan.save()

            return Response({"message": "Payment processed successfully"}, status=status.HTTP_201_CREATED)
        except Payment.DoesNotExist:
            return Response({"message": "Payment record not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def get(self, request):
        payments = Payment.objects.all()
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)