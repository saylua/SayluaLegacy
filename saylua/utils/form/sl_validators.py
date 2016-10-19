import re
from wtforms import validators

from saylua.models.user import User

# Base class for other validators
class SayluaValidator:
    def __init__(self, message=None):
        self.message = message
        self.defaultMessage = '<field> is invalid.'

    def __call__(self, form, field):
        if not self.validate(form, field):
            if self.message:
                message = self.message
            else:
                message = self.defaultMessage
            message = message.replace('<field>', field.label.text)
            raise validators.StopValidation(message)

    def validate(self, form, field):
        return True

    # This is the name for the data attribute of the client side
    def clientValidatorName(self):
        return None

    def clientValidatorValue(self):
        return None

    # Tells the client to overwrite its default message with the server's
    # custom message if a custom message exists
    def clientValidatorMessage(self):
        return self.message


class Required(SayluaValidator):
    def __init__(self, message=None):
        self.message = message
        self.defaultMessage = '<field> is required.'

    def validate(self, form, field):
        return field.data

    def clientValidatorName(self):
        return 'data-slform-required'

class NotBlank(SayluaValidator):
    def __init__(self, message=None):
        self.message = message
        self.defaultMessage = '<field> cannot be blank!'

    def validate(self, form, field):
        return field.data and not field.data.isspace()

    def clientValidatorName(self):
        return 'data-slform-notblank'

class EqualTo(SayluaValidator):
    def __init__(self, fieldname, message=None):
        self.fieldname = fieldname
        self.message = message

    def validate(self, form, field):
        try:
            other = form[self.fieldname]
        except KeyError:
            raise ValidationError(field.gettext("Invalid field name '%s'.") % self.fieldname)

        self.defaultMessage = '<field> must match %s!' % other.label.text
        return field.data == other.data

    def clientValidatorName(self):
        return 'data-slform-equalto'

    def clientValidatorValue(self):
        return self.fieldname

class Min(SayluaValidator):
    def __init__(self, length, message=None):
        self.message = message
        self.defaultMessage = '<field> must be at least %d characters long!' % length
        self.length = length

    def validate(self, form, field):
        return len(field.data) >= self.length

    def clientValidatorName(self):
        return 'data-slform-min'

    def clientValidatorValue(self):
        return self.length


class Max(SayluaValidator):
    def __init__(self, length, message=None):
        self.message = message
        self.defaultMessage = '<field> cannot be greater than %d characters long!' % length
        self.length = length

    def validate(self, form, field):
        return len(field.data) <= self.length

    def clientValidatorName(self):
        return 'data-slform-max'

    def clientValidatorValue(self):
        return self.length

class IsNot(SayluaValidator):
    def __init__(self, pattern, message=None):
        self.pattern = pattern
        self.defaultMessage = '<field> cannot be %s!' % pattern
        self.message = message

    def validate(self, form, field):
        return field.data != self.pattern

    def clientValidatorName(self):
        return 'data-slform-matches'

    def clientValidatorValue(self):
        return self.pattern

class MatchesRegex(SayluaValidator):
    def __init__(self, regex, message=None):
        self.message = message
        self.defaultMessage = '<field> is incorrectly formatted!'
        self.regex = regex

    def validate(self, form, field):
        pattern = re.compile(self.regex)
        return pattern.match(field.data)

    def clientValidatorName(self):
        return 'data-slform-regex'

    def clientValidatorValue(self):
        return self.regex


class Email(MatchesRegex):
    def __init__(self, message=None):
        self.regex = '(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
        self.message = message
        self.defaultMessage = '<field> must be a valid email!'

    def clientValidatorMessage(self):
        return self.message or self.defaultMessage

class Username(MatchesRegex):
    def __init__(self, message=None):
        self.regex = '^[A-Za-z0-9+~._-]+$'
        self.message = message
        self.defaultMessage = 'Usernames may only contain letters, numbers, and these characters: +~._-'

    def clientValidatorMessage(self):
        return self.message or self.defaultMessage

class UsernameUnique(SayluaValidator):
    def __init__(self, whitelist=None, message=None):
        self.message = message
        self.defaultMessage = 'A user with that username already exists.'
        self.whitelist = whitelist

    def validate(self, form, field):
        username = field.data.lower()
        if self.whitelist and username in self.whitelist:
            return True
        return not User.key_by_username(username)
