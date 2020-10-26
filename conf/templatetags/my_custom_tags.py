from django import template
from django.forms import CheckboxInput

register = template.Library()

@register.filter(name='is_checkbox')
def is_checkbox(field):
  return field.field.widget.__class__.__name__ == CheckboxInput().__class__.__name__

@register.simple_tag
def wizard_checkbox(field):
     field = field.widget.attrs['class'] = ' wizard-ichecks '
     return field
    
@register.filter(name='gender')
def gender(value):
    if value == 'm':
        return "Male"
    if value == 'f':
        return "Female"
    return ""

@register.filter(name='maritual')   
def maritual(value):
    if value == 'm':
        return "Married"
    if value == 's':
        return "Single"
    if value == 'w':
        return "Widow"
    if value == 'd':
        return "Divorced"
    return ""
    
@register.filter(name='add_attr')
def add_attr(field, css):
    attrs = {}
    definition = css.split(',')

    for d in definition:
        if ':' not in d:
            attrs['class'] = d
        else:
            key, val = d.split(':')
            attrs[key] = val
    return field.as_widget(attrs=attrs)


@register.filter(name='htmlattributes')
def htmlattributes(value, arg):
    value.field.widget.attrs = {}
    attrs = value.field.widget.attrs
    data = arg.replace(' ', '')   
    kvs = data.split('|') 

    for string in kvs:
        kv = string.split('=')
        attrs[kv[0]] = kv[1]

    rendered = value
    
    return rendered

register.filter('htmlattributes', htmlattributes)
