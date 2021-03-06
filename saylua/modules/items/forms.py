from flask_wtf import FlaskForm
from wtforms.fields import SelectField

from saylua.utils.form import sl_validators
from saylua.utils.form.fields import SlField, SlFileField, SlTextAreaField


class ItemUploadForm(FlaskForm):
    name = SlField('Item Name', [
        sl_validators.Required(),
        sl_validators.NotBlank()])
    canon_name = SlField('Canon Name', [
        sl_validators.CanonName(),
        sl_validators.NotBlank()])
    image = SlFileField('Image File', [])
    category_id = SelectField('Category', coerce=int)
    description = SlTextAreaField('Description', [
        sl_validators.Required(),
        sl_validators.NotBlank()])
