from django import forms
from .models import Transaction
from account_app.models import UserAccount

# 1 ta form jeta ki na inherit korbe sob gula page a 
class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            'amount',
            'transaction_type'
        ]

    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account')
        super().__init__(*args, **kwargs)
        self.fields['transaction_type'].disabled = True
        self.fields['transaction_type'].widget = forms.HiddenInput()

    def save(self, commit=True):
        self.instance.account = self.account
        self.instance.balance_after_transaction = self.account.balance
        return super().save()




class DepositForm(TransactionForm):
    def clean_amount(self): 
        min_deposit_amount = 100
        amount = self.cleaned_data.get('amount') 
        if amount < min_deposit_amount:
            raise forms.ValidationError(
                f'You need to deposit at least {min_deposit_amount} $'
            )

        return amount


class WithdrawForm(TransactionForm):

    def clean_amount(self):
        account = self.account
        min_withdraw_amount = 500
        max_withdraw_amount = 20000
        balance = account.balance # 1000
        amount = self.cleaned_data.get('amount')
        if amount < min_withdraw_amount:
            raise forms.ValidationError(
                f'You can withdraw at least {min_withdraw_amount} $'
            )

        if amount > max_withdraw_amount:
            raise forms.ValidationError(
                f'You can withdraw at most {max_withdraw_amount} $'
            )

        if amount > balance: 
            raise forms.ValidationError(
                f'You have {balance} $ in your account. '
                'You can not withdraw more than your account balance'
            )

        return amount



class LoanRequestForm(TransactionForm):
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')

        return amount
 


class TransferForm(forms.Form):
    recipient_account = forms.ModelChoiceField(queryset=UserAccount.objects.all())
    amount = forms.DecimalField(max_digits=10, decimal_places=2)

    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account', None)
        super().__init__(*args, **kwargs)

    def clean_account_no(self):
        account_no = self.cleaned_data['account_no']
        if not UserAccount.objects.filter(account_no=account_no).exists():
            raise forms.ValidationError(f'Account with number {account_no} does not exist.')
        return account_no

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if self.account is None:
            raise forms.ValidationError('Account information is required.')
        if amount  > self.account.balance:
            raise forms.ValidationError('Insufficient balanced in your account.')
        return amount

    def clean(self):
        cleaned_data = super().clean()
        account_no = cleaned_data.get('account_no')

        if account_no:
            self.to_account = UserAccount.objects.get(account_no=account_no)

        return cleaned_data

    def save(self, commit=True):
        amount = self.cleaned_data['amount']
        self.account.balance -= amount
        self.to_account.balance += amount
        if commit:
            self.account.save()
            self.to_account.save()
        return self.account, self.to_account

