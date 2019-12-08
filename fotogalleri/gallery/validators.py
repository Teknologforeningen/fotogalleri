from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_path_name(value):
    forbidden_strings = ['/', '\\', '.', ' ', '\'', '\"']
    if any(forbidden in value for forbidden in forbidden_strings):
        raise ValidationError(
            _('The folder name can\'t contain any of the following characters: slashes ( / , \ ), quotation marks ( \", \'),  dots, spaces'),
            params={'value': value},
        )
