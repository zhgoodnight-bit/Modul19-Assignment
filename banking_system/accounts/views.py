from django.shortcuts import render, redirect, get_object_or_404
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from .models import BankAccount, Transaction
from .forms import RegistrationForm, AccountForm, DepositForm, WithdrawForm
from django.contrib.auth import logout
# ==========================================
# 1. REGISTER VIEW
# ==========================================
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful!')
            return redirect('login')
    else:
        form = RegistrationForm()
        
    return render(request, 'register.html', {'form': form})

# ==========================================
# 2. CREATE BANK ACCOUNT VIEW
# ==========================================
@login_required
def create_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user  
            account.save()  
            messages.success(request, 'Bank account created successfully!')
            return redirect('dashboard')
    else:
        form = AccountForm()
        
    return render(request, 'create_account.html', {'form': form})

# ==========================================
# 3. DASHBOARD VIEW
# ==========================================
@login_required
def dashboard(request):
    account = BankAccount.objects.filter(user=request.user).first()

    if not account:
        messages.warning(request, 'Please create a bnak Account first')
        return redirect ('create_account')

    total_deposit = Transaction.objects.filter(
        user=request.user,
        transaction_type='deposit'
    ).aggregate(Sum('amount'))

    total_withdraw = Transaction.objects.filter(
        user=request.user,
        transaction_type='withdraw'
    ).aggregate(Sum('amount'))

    total_transactions = Transaction.objects.filter(user=request.user).count()

    return render(
        request,
        'dashboard.html',
        {
            'account': account,
            'total_deposit': total_deposit,
            'total_withdraw': total_withdraw,
            'total_transactions': total_transactions
        }
    )

# ==========================================
# 4. DEPOSIT MONEY VIEW
# ==========================================
@login_required
def deposit(request):
    account = get_object_or_404(BankAccount, user=request.user)
    
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            account.balance += amount
            account.save()

            Transaction.objects.create(
                user=request.user,
                transaction_type='deposit',
                amount=amount,
                balance_after_transaction=account.balance
            )
            messages.success(request, 'Deposit successful!')
            return redirect('dashboard')  
    else:
        form = DepositForm()
        
    return render(request, 'deposit.html', {'form': form})

# ==========================================
# 5. WITHDRAW MONEY VIEW
# ==========================================
@login_required
def withdraw(request):
    account = get_object_or_404(BankAccount, user=request.user)
    
    if request.method == 'POST':
        form = WithdrawForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            
            if amount > account.balance:
                messages.error(request, 'Insufficient balance.')
                return redirect('withdraw')
            else:
                account.balance -= amount
                account.save()

                Transaction.objects.create(
                    user=request.user,
                    transaction_type='withdraw',
                    amount=amount,
                    balance_after_transaction=account.balance
                )
                messages.success(request, 'Withdrawal successful!')
                return redirect('dashboard')
    else:
        form = WithdrawForm()
        
    return render(request, 'withdraw.html', {'form': form})

# ==========================================
# 6. TRANSACTION LOG VIEW
# ==========================================
@login_required
def transactions(request):
    transaction_type = request.GET.get('type')
    date = request.GET.get('date')

    transactions_list = Transaction.objects.filter(user=request.user)

    if transaction_type:
        transactions_list = transactions_list.filter(transaction_type=transaction_type)
        
    if date:
        transactions_list = transactions_list.filter(created_at__date=date)
        
    return render(
        request,
        'transactions.html',
        {'transactions': transactions_list.order_by('-created_at')} 
    )
# ==========================================
# 7. Custom Logout View
# ==========================================
def user_logout(request):
    logout(request)
    return redirect('login')