from django.db import models
from django import forms
from django.core import validators
from django.utils.translation import ugettext as _
from conf.utils import internationalize_number


MOBILE_VALIDATOR = validators.RegexValidator(r'^(0|256|\+256)7(0|1|2|4|5|7|8|9)\d{7,7}$',
                                              _('Invalid mobile number.'))

PHONE_VALIDATOR = validators.RegexValidator(r'^(0|256|\+256||)(7|4|3)(0|1|2|4|5|7|8|9)\d{7,7}$',
                                              _('Invalid phone number.'))

MTNUG_VALIDATOR = validators.RegexValidator(r'^(0|256|\+256)(77|78|76)([0-9])(\d{6,6})$',
                                              _('Invalid MTN phone number.'))

AIRTELUG_VALIDATOR = validators.RegexValidator(r'^(0|256|\+256)(75|70)([0-9])(\d{6,6})$',
                                              _('Invalid Airtel phone number.'))


class UGMobileNumberField(models.CharField):
    def get_prep_value(self, value):
        return internationalize_number(value)


class UGMobileNumberFormField(forms.CharField):
    default_validators = [MOBILE_VALIDATOR]


class UGPhoneNumberFormField(forms.CharField):
    default_validators = [PHONE_VALIDATOR]


class MTNUGPhoneNumberFormField(forms.CharField):
    default_validators = [MTNUG_VALIDATOR]


class AirtelUGPhoneNumberFormField(forms.CharField):
    default_validators = [AIRTELUG_VALIDATOR]

