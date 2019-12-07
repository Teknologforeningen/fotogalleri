from django.template import Library


register = Library()


@register.filter(name='view')
def view(value):
    return '/view/{value}'.format(value=value)
