from wtforms import widgets

import sl_validators


def generateCustomKwargs(field, error_class, kwargs):
    if field.errors:
        c = kwargs.pop('class', '') or kwargs.pop('class_', '')
        kwargs['class'] = '%s %s' % (error_class, c)

    if not kwargs.get('placeholder'):
        kwargs['placeholder'] = field.label.text

    # Integrate with clientside validation.
    for validator in field.validators:
        if isinstance(validator, sl_validators.SayluaValidator):
            clientName = validator.clientValidatorName()
            if clientName:
                if 'data-slform-validators' not in kwargs:
                    kwargs['data-slform-validators'] = ''
                else:
                    kwargs['data-slform-validators'] += ' '

                kwargs['data-slform-validators'] += clientName
                val = validator.clientValidatorValue()
                if val:
                    kwargs['data-slform-validators'] += ':' + str(val)

                message = validator.clientValidatorMessage()
                if message:
                    kwargs['data-slform-' + clientName + '-message'] = message
    return kwargs


class SlInput(widgets.TextInput):
    def __init__(self, error_class='error'):
        self.error_class = error_class

    def __call__(self, field, **kwargs):
        kwargs = generateCustomKwargs(field, self.error_class, kwargs)

        return super(SlInput, self).__call__(field, **kwargs)


class SlTextArea(widgets.TextArea):
    def __init__(self, error_class='error'):
        self.error_class = error_class

    def __call__(self, field, **kwargs):
        kwargs = generateCustomKwargs(field, self.error_class, kwargs)
        return super(SlTextArea, self).__call__(field, **kwargs)


class SlPasswordInput(SlInput):
    input_type = 'password'

    def __init__(self, hide_value=True, **kwargs):
        super(SlPasswordInput, self).__init__(**kwargs)
        self.hide_value = hide_value

    def __call__(self, field, **kwargs):
        if self.hide_value:
            kwargs['value'] = ''
        return super(SlPasswordInput, self).__call__(field, **kwargs)


class SlCheckboxInput(SlInput):
    input_type = 'checkbox'

    def __call__(self, field, **kwargs):
        if getattr(field, 'checked', field.data):
            kwargs['checked'] = True
        return super(SlCheckboxInput, self).__call__(field, **kwargs)


class SlFileInput(SlInput):
    input_type = 'file'


class SlNumberInput(SlInput):
    input_type = 'number'
