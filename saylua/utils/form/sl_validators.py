import re
from wtforms import validators

from saylua import app
from saylua.modules.users.models.db import User


# Base class for other validators. This is mostly used for two reasons:
# - The custom validators have custom default error messages.
# - Validators that implement this class integrate with Saylua's custom
#   clientside validation library.
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

    # This is the name for the data attribute of the client side.
    def clientValidatorName(self):
        return None

    # This specifies a parameter to pass into the clientside validator.
    def clientValidatorValue(self):
        return None

    # Tells the client to overwrite its default message with the server's
    # custom message if a custom message exists.
    def clientValidatorMessage(self):
        return self.message


class Required(SayluaValidator):
    def __init__(self, message=None):
        self.message = message
        self.defaultMessage = '<field> is required.'

    def validate(self, form, field):
        return field.data

    def clientValidatorName(self):
        return 'required'


class AtLeast(SayluaValidator):
    def __init__(self, minval, message=None):
        self.message = message
        self.defaultMessage = '<field> must be at least %d.' % min
        self.min = minval

    def validate(self, form, field):
        return field.data >= self.min

    def clientValidatorValue(self):
        return str(self.min)

    def clientValidatorName(self):
        return 'atleast'


class NotNegative(AtLeast):
    def __init__(self, message=None):
        self.message = message
        self.defaultMessage = '<field> cannot be negative.'
        self.min = 0

    def clientValidatorMessage(self):
        return self.message or self.defaultMessage


class NotBlank(SayluaValidator):
    def __init__(self, message=None):
        self.message = message
        self.defaultMessage = '<field> cannot be only spaces.'

    def validate(self, form, field):
        return not field.data.isspace()

    def clientValidatorName(self):
        return 'notblank'


class EqualTo(SayluaValidator):
    def __init__(self, fieldname, message=None):
        self.fieldname = fieldname
        self.message = message

    def validate(self, form, field):
        try:
            other = form[self.fieldname]
        except KeyError:
            raise validators.ValidationError(field.gettext(
                "Invalid field name '%s'.") % self.fieldname)

        self.defaultMessage = '<field> must match %s.' % other.label.text
        return field.data == other.data

    def clientValidatorName(self):
        return 'equalto'

    def clientValidatorValue(self):
        return self.fieldname


class Min(SayluaValidator):
    def __init__(self, length, message=None):
        self.message = message
        self.defaultMessage = '<field> must be at least %d characters long.' % length
        self.length = length

    def validate(self, form, field):
        return len(field.data) >= self.length

    def clientValidatorName(self):
        return 'min'

    def clientValidatorValue(self):
        return str(self.length)


class Max(SayluaValidator):
    def __init__(self, length, message=None):
        self.message = message
        self.defaultMessage = '<field> cannot be more than %d characters long.' % length
        self.length = length

    def validate(self, form, field):
        return len(field.data) <= self.length

    def clientValidatorName(self):
        return 'max'

    def clientValidatorValue(self):
        return str(self.length)


class IsNot(SayluaValidator):
    def __init__(self, pattern, message=None):
        self.pattern = pattern
        self.defaultMessage = '<field> cannot be %s.' % pattern
        self.message = message

    def validate(self, form, field):
        return field.data != self.pattern

    def clientValidatorName(self):
        return 'isnot'

    def clientValidatorValue(self):
        return self.pattern


class EndsWith(SayluaValidator):
    def __init__(self, suffix, message=None):
        self.message = message
        self.defaultMessage = '<field> must end with %s.' % suffix
        self.suffix = suffix

    def validate(self, form, field):
        return field.data.lower().endswith(self.suffix.lower())

    def clientValidatorName(self):
        return 'endswith'

    def clientValidatorValue(self):
        return self.suffix


class MatchesRegex(SayluaValidator):
    def __init__(self, regex, message=None):
        self.message = message
        self.defaultMessage = '<field> is incorrectly formatted!'
        self.regex = regex

    def validate(self, form, field):
        pattern = re.compile(self.regex)
        return pattern.match(field.data)

    def clientValidatorName(self):
        return 'regex'

    def clientValidatorValue(self):
        return self.regex


class CanonName(MatchesRegex):
    def __init__(self, message=None):
        self.regex = app.config['CANON_NAME_REGEX']
        self.message = message
        self.defaultMessage = 'Canon names may only contain lowercase letters, numbers, and _'

    def clientValidatorMessage(self):
        return self.message or self.defaultMessage


class Email(MatchesRegex):
    def __init__(self, message=None):
        self.regex = app.config['EMAIL_REGEX']
        self.message = message
        self.defaultMessage = '<field> must be a valid email!'

    def clientValidatorMessage(self):
        return self.message or self.defaultMessage


class Username(MatchesRegex):
    def __init__(self, message=None):
        self.regex = app.config['USERNAME_REGEX']
        self.message = message
        self.defaultMessage = 'Usernames may only contain letters, numbers, and +~._-'

    def clientValidatorMessage(self):
        return self.message or self.defaultMessage


class UsernameOrEmail(MatchesRegex):
    def __init__(self, message=None):
        # This is pretty ugly but it makes this work easily on the clientside
        # validator as well.
        self.regex = ('(' + app.config['EMAIL_REGEX'] + '|' +
            app.config['USERNAME_REGEX'] + ')')
        self.message = message
        self.defaultMessage = 'Please enter a valid username or email.'

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
        return not User.by_username(username)


class EmailUnique(SayluaValidator):
    def __init__(self, message=None):
        self.message = message
        self.defaultMessage = 'A user with that email already exists.'

    def validate(self, form, field):
        email = field.data
        return not User.from_email(email)
