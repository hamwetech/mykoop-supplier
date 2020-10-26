import logging
import traceback
from messaging.models import OutgoingMessages
from messaging.messaging_process import MessagingTransaction
from conf.utils import log_debug, log_error

def depr__sendSMS(msisdn, message, **kwargs):
    try:
        res = None
        account = kwargs.get('account', '')
        outgoing = OutgoingMessages()
        outgoing.msisdn = msisdn
        outgoing.message = message
        outgoing.account = account if account else None
        try:
            sm = MessagingTransaction('BkKda32wkdqUeMWUBYPY')
            res = sm.sendOneSMS(msisdn, message)
            log_debug("Sent Message... %s" % res)
        except Exception:
            log_debug("Sending Failed... %s" % traceback.format_exc())
            outgoing.status = 'FAILED'
        outgoing.response = res
        outgoing.save() 
    except Exception as e:
        #Die silently
        log_error()
        
def sendSMS(request, msisdn, message):
    mt = MessagingTransaction(password='IvJhk4THhCMPBkjfC8R4', user=request.user)
    res = mt.send_message(msisdn, message)
    
