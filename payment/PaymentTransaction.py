import datetime
from payment.utils import payment_transction
from payment.models import MobileMoneyRequest

from conf.utils import generate_alpanumeric, log_debug, log_error


class PaymentTransaction:
    amount = None
    phone_number = None
    
    def __init__(self, phone_number, amount):
        self.phone_number = phone_number
        self.amount = amount
        
     
    def mobile_money_transation(self):
        try:
            transaction_reference = generate_alpanumeric('WC', 12)
           
            phone_number = self.phone_number
            amount = self.amount
            status = 'PENDING'
            request = ''
            
            mm_request = MobileMoneyRequest.objects.create(
                transaction_reference = transaction_reference,
                phone_number = phone_number,
                amount = amount,
                status = status,
                request = request
            )
            
            reference = mm_request.transaction_reference
            res = payment_transction(phone_number, amount, reference)
            status = res['status']
            if res['status'] == 'ERROR':
                status = 'FAILED'
            if res['status'] == 'OK':
                status = res['transactionStatus']
            mm_request.status = status
            mm_request.response = res
            mm_request.response_date = datetime.datetime.now()
            mm_request.save()
            return {"status": mm_request.status}
        except Exception as e:
            log_error()
            return {"status": "FAILED"}
            
        