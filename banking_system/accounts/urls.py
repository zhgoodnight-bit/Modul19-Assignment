from django.urls import path
from . import views
################################################
urlpatterns = [
    path (
            'register/',
            views.register,
            name = 'register'
    ),
    path (
            'dashboard/',
            views.dashboard,
            name = 'dashboard'
        ),
    path (
            'account/create/',
            views.create_account,
            name = 'create_account'
        ),
    path (
            'deposit/',
            views.deposit,
            name = 'deposit'
        ),
      path (
            'withdraw/',
            views.withdraw,
            name = 'withdraw'
            ),
    path (
            'transactions/',
            views.transactions,
            name = 'transactions'
        ),
]