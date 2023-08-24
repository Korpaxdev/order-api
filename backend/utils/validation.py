from django.contrib.auth.password_validation import (CommonPasswordValidator, MinimumLengthValidator,
                                                     NumericPasswordValidator)


def password_validation(password: str):
    validators = [MinimumLengthValidator, NumericPasswordValidator, CommonPasswordValidator]
    for validator in validators:
        validator().validate(password)
