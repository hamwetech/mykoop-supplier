import re
import logging
import string
import traceback
import uuid
import random, string
from django import forms
from django.contrib.admin.utils import NestedObjects
from django.utils.text import capfirst
from django.utils.encoding import force_text
from conf.models import MessageTemplates, SystemSettings

log = logging.getLogger("umis")
PHONE_REGEX = re.compile(r'^(0|256|\+256|)(3|4|7)([0-9])(\d{7,7})$')

def log_error():
    return log.error(traceback.format_exc())
    
def log_debug(text):
    return log.debug(text)

def get_message_template():
    q = MessageTemplates.objects.filter(pk=1)
    if q.exists():
        return q[0]
    return None
    

def internationalize_number(number):
    number = str(number)
    number = number.replace(" ", "").replace("-", "")
    match = PHONE_REGEX.match(number)
    if match:
        sections = list(match.groups())
        sections[0] = '256'
        return ''.join(sections)
    raise ValueError("Incorrect phone number.")

def generate_alpanumeric(prefix="", size=16):
    x = ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(size))
    return '{}{}'.format(prefix, x)

def generate_numeric(size = 16, prefix=""):
    x = ''.join(random.choice(string.digits) for i in range(size))
    return '{}{}'.format(prefix, x)

def genetate_uuid4():
    return str(uuid.uuid4())

def get_consontant_upper(string, size=3):
    vowels = ['a','e','i','o','u']
    cons = re.sub('|'.join(vowels), "", string.upper(), flags=re.IGNORECASE)
    sstr = cons[:size]
    return sstr

def float_to_intstring(value):
    try:
        value = str(int(value))
    except:
        pass
    return value

def get_deleted_objects(objs): 
    collector = NestedObjects(using='default')
    collector.collect(objs)
    #
    
    def format_callback(obj):
        
        opts = obj._meta
        no_edit_link = '%s: %s' % (capfirst(opts.verbose_name),
                                   force_text(obj))
        
        return no_edit_link            
    #
    
    to_delete = collector.nested(format_callback)
    protected = [format_callback(obj) for obj in collector.protected]
    model_count = {model._meta.verbose_name_plural: len(objs) for model, objs in collector.model_objs.items()}
    #
    return to_delete, model_count, protected

def bootstrapify(cls):
    fields = cls.base_fields
    for field in fields.values():
        if 'class' not in field.widget.attrs:
            field.widget.attrs.update({'class': ''})

        # HTML5 form validation on the browser end for forms
        if field.required:
            field.widget.attrs['class'] += 'required '

        # # don't do for files and images
        # if isinstance(field, (forms.ImageField, forms.FileField)):
        #     continue

        # don't do for radios and checkboxes
        if isinstance(field.widget, (forms.RadioSelect, forms.CheckboxSelectMultiple)):
            continue
        
        #ignore dates
        if isinstance(field, (forms.DateTimeField, forms.DateField)):
            continue
        
        if isinstance(field.widget, forms.CheckboxInput):
            field.widget.attrs['data-md-icheck'] = ''
            continue

        # bootstrapify here
        field.widget.attrs['class'] += ' md-input '

        # specially for textareas
        if isinstance(field.widget, (forms.Textarea)):
            field.widget.attrs['class'] += ' text-area '

        # specially for datetime fields
        # if isinstance(field, (forms.DateTimeField)):
        #     field.widget.attrs['class'] += 'date-time '
        # 
        # # specially for date fields
        # if isinstance(field, (forms.DateField)):
        #     field.widget.attrs['data-uk-datepicker'] = "{format:'YYYY-MM-DD'}"
        #     
        # if isinstance(field, (forms.DateTimeField)):
        #     field.widget.attrs['data-uk-datepicker'] = "{format:'YYYY-MM-DD HH:MM'}"
            
         # specially for date fields
        if isinstance(field, (forms.FileField)):
            
            field.widget.attrs['class'] = ' dropify '
            
        # specially for selectbox fields
        if isinstance(field.widget, (forms.Select)):
            field.widget.attrs['class'] += ' label-fixed selectize '
            
        
        # specially for selectbox fields
        if isinstance(field.widget, (forms.SelectMultiple)):
            field.widget.attrs['class'] = ''