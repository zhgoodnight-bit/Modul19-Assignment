from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BankAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_holder_name = models.CharField(max_length=150)
    account_number = models.CharField(max_length=20, unique=True)
    balance = models.DecimalField(max_digits=12,decimal_places=2,default=0)

    def __str__(self):
        return f"{self.account_holder_name}"

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('deposit','Deposit'),
        ('withdraw','Withdraw'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    balance_after_transaction = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.transaction_type}"