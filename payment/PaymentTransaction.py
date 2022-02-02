import datetime
from payment.utils import payment_transction
from payment.models import MobileMoneyRequest
from account.models import AccountTransaction

from conf.utils import generate_alpanumeric, log_debug, log_error


class PaymentTransaction:
    amount = None
    phone_number = None
    account = None
    
    def __init__(self, account, phone_number, amount):
        self.phone_number = phone_number
        self.amount = amount
        self.account = account

    def mobile_money_transation(self, internal_reference, reason):
        try:
            transaction_reference = generate_alpanumeric('WC', 12)
           
            phone_number = self.phone_number
            amount = self.amount
            status = 'PENDING'
            request = ''
            
            mm_request = AccountTransaction.objects.create(
                account = self.account,
                reference = transaction_reference,
                internal_reference = internal_reference,
                phone_number = phone_number,
                request_date = datetime.datetime.now(),
                balance_before = self.account.balance,
                amount = amount,
                status = status,
                category = 'ORDER PAYMENT',
                transaction_type='CREDIT',
                request = request
            )
            
            reference = mm_request.reference
            res = payment_transction(phone_number, amount, reference)
            # res['transactionStatus'] = "SUCCESSFUL" # Delete once done testing
            status = res['status']
            if res['status'] == 'ERROR':
                status = 'FAILED'
            if res['status'] == 'OK':
                status = res['transactionStatus']
                mm_request.provider_reference = res.get('transactionReference')
            mm_request.status = status
            mm_request.response = res
            mm_request.response_date = datetime.datetime.now()
            mm_request.save()
            return {"status": mm_request.status}
        except Exception as e:
            log_error()
            return {"status": "FAILED"}
            
        