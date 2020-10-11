from base64 import b64encode

from django.template.defaulttags import register


@register.filter
def binary2str(_bin):
    if _bin is not None: return b64encode(_bin).decode('utf-8')


@register.filter
def formatpercent(val):
    if val is not None: return val * 100
