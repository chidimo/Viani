from django.core.validators import RegexValidator

validate_branch_code = RegexValidator(
    regex='^[0-9]{4}$', message='You have to enter 4 digits', code='Not set')
msg = "Please enter a valid phone number in the format '+234**********'"
validate_contact = RegexValidator(
    regex=r'^\+[0-9]{1,13}$', message=msg, code='Not set')
