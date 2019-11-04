from django.template import Library
from django.urls import reverse


register = Library()


@register.filter(name='rev')
def rev(value):
    return reverse(value)
