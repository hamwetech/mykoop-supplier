from account.models import Account, AccountTransaction
from conf.utils import log_debug, log_error


class AccountActivity:
    account = None

    def __init__(self, account):
        self.account = account

    def credit_account(self, amount):
        balance = self.account.balance
        new_balance = balance + amount
        self.account.balance = new_balance
        self.account.save()
        log_debug("Account %s credited: before %s after %s" % (self.account, balance, new_balance))


    def debit_account(self, amount):
        balance = self.account.balance
        new_balance = balance - amount
        self.account.balance = new_balance
        self.account.save()
        log_debug("Account %s debited: before %s after %s" % (self.account, balance, new_balance))

