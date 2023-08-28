from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Borrower(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Investor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_balance = models.FloatField()

class Loan(models.Model):
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE, null=True, blank=True)
    loan_amount = models.FloatField()
    loan_period = models.PositiveIntegerField()
    annual_interest_rate = models.FloatField(null=True, blank=True)
    lenme_fee = models.FloatField()
    total_loan_amount = models.FloatField(null=True, blank=True)
    funded_date = models.DateTimeField(null=True, blank=True)
    loan_status = models.CharField(max_length=20, choices=[("Pending", "Pending"), ("Funded", "Funded"), ("Completed", "Completed")], default="Pending")



class Payment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    payment_duedate = models.DateField()
    payment_date = models.DateTimeField(null=True, blank=True)
    amount = models.FloatField()
    is_completed = models.BooleanField(default=False)
