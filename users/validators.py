from django.core.validators import RegexValidator

validate_phone = RegexValidator(
    regex=r"^998\d{9}$",
    message="Phone number must begin with 998 and contain only 12 numbers",
)