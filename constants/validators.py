from django.core.validators import RegexValidator

msg = "Please enter a valid phone number in the format '+234**********'"
validate_phone = RegexValidator(
    regex=r'^\+[0-9]{1,13}$', message=msg, code='Not set')
