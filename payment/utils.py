import re
import traceback
import logging
import sys
import unicodedata
import requests
import base64
import json
from datetime import datetime
from conf.utils import log_debug, log_error, generate_alpanumeric


def payment_transction(msisdn, amount, reference):
        if True:
            return {"status": "OK", "transactionStatus": "SUCCESSFUL", "transactionReference": generate_alpanumeric()}

        msisdn = msisdn
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = 'W3E4g8weR5TgH0Td2344'
        accountid = 'andrew'
        token = base64.urlsafe_b64encode(accountid + password + timestamp)
        http_auth = base64.urlsafe_b64encode('andrew:hamwe')
        url = 'https://payments.hamwepay.com/endpoint/service/transaction/'
        # url = 'https://payments-dev.hamwepay.com/endpoint/service/transaction/'

        try:
            data = {
                "reference": reference,
                "method": "COLLECTION",
                "amount": "%s" % amount,
                "timestamp": timestamp,
                "token": token,
                "phonenumber": msisdn,
                "accountid": accountid
            }

            log_debug("Sending Airtime: %s" % data)
            headers = {'content-type': 'application/json', 'Authorization': 'Basic %s' % http_auth}

            req = requests.post(url, data=json.dumps(data), headers=headers)
            jr = json.loads(req.text)
            if 'transactionStatus' in jr:
                if jr['transactionStatus'] == 'SUCCESSFUL':
                    log_debug(jr)
            log_debug("Response From Server %s" % req.text)
            return jr
        except Exception as err:
            log_error()
            return {"status": "ERROR", "statusMessage": "Server Error"}


def transaction_status(reference):
    # if True:
    #     return {"status": "FAILED", "statusMessage": "Test Complete"}
    msisdn = msisdn
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    password = 'W3E4g8weR5TgH0Td2344'
    accountid = 'andrew'
    token = base64.urlsafe_b64encode(accountid + password + timestamp)
    http_auth = base64.urlsafe_b64encode('andrew:hamwe')
    url = 'https://payments.hamwepay.com/endpoint/service/transaction/%s' % reference
    try:
        log_debug("Checking Status: %s" % reference)
        headers = {'content-type': 'application/json', 'Authorization': 'Basic %s' % http_auth}

        req = requests.get(url, headers=headers)
        jr = json.loads(req.text)
        if 'transactionStatus' in jr:
            if jr['transactionStatus'] == 'SUCCESSFUL':
                log_debug(jr)
        log_debug("Response From Server %s" % req.text)
        return jr
    except Exception as err:
        log_error()
        return {"status": "ERROR", "statusMessage": "Server Error"}