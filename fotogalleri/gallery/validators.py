from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from backend.models import ImagePath


def validate_path_name(value):
    forbidden_strings = ['/', '\\', '.', ' ', '\'', '\"']
    if any(forbidden in value for forbidden in forbidden_strings):
        raise ValidationError(
            _('The folder name can\'t contain any of the following characters:' +
              'slashes ( / , \\ ), quotation marks ( \", \'),  dots, spaces'),
            params={'value': value},
        )
    return value


def validate_path_parent(value):
    value = value[:-1] if value[-1] == '/' else value
    # List of strings each describing a directory
    parents = value.split('/')[2:]
    # An ImagePath-object
    previous = None
    for current in parents:
        parent = ImagePath.objects.filter(path=current, parent=previous)
        if parent:
            previous = parent[0]
        else:
            raise ValidationError(_('Parent directory does not exist'), params={'value': value})
