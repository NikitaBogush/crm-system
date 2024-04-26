from django.core.exceptions import ValidationError


def phone_regex(value):
    if value != r"^(\+7)(\d{10})$":
        raise ValidationError(
            "Номер телефона должен быть введен в формате: '+79999999999'"
        )
