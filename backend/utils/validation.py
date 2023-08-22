from django.contrib.auth.password_validation import MinimumLengthValidator, CommonPasswordValidator, \
    NumericPasswordValidator


def password_validation(password: str):
    validators = [MinimumLengthValidator, NumericPasswordValidator, CommonPasswordValidator]
    for validator in validators:
        validator().validate(password)
