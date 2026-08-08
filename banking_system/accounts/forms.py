from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import BankAccount
from .models import Transaction
###############################################################
class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2'
        )
class AccountForm(forms.ModelForm):
      class Meta:
           model = BankAccount
           fields = [
                'account_holder_name',
                'account_number'
           ]
class DepositForm(forms.Form):
     amount = forms.DecimalField(min_value = 1)

class WithdrawForm(forms.Form):
     amount = forms.DecimalField(min_value = 1)