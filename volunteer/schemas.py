from colander import MappingSchema, SchemaNode, String, Integer, DateTime
from volunteer.models import PhoneNumberFormatter

from wtforms import Form, TextField, validators, IntegerField, SelectField, HiddenField
from wtforms.fields import Field
from wtforms.widgets import TextInput

class SmsSchema(MappingSchema):
    username = SchemaNode(String(),missing=None)
    password = SchemaNode(String(),missing=None)
    type = SchemaNode(String(),missing=None)
    to = SchemaNode(String(),missing=None)
    msisdn = SchemaNode(String())
    network_code = SchemaNode(String(),missing=None)
    message_id = SchemaNode(String(),missing=None)
    message_timestamp = SchemaNode(DateTime(),missing=None)
    text = SchemaNode(String(),missing=None)
    concat = SchemaNode(String(),missing=None)
    concat_ref = SchemaNode(String(),missing=None)
    concat_total = SchemaNode(Integer(),missing=None)
    concat_part = SchemaNode(Integer(),missing=None)


def empty_to_none(data):
    if data is None or len(data.strip()) == 0:
        return None
    else:
        return data.strip()

class PhoneNumberField(Field):
    widget=TextInput()
    formatter = PhoneNumberFormatter()

    def _value(self):
        return self.data and self.formatter.format(self.data) or ''

    def process_formdata(self, valuelist):
        if valuelist:
            phone_number = valuelist[0]

            if not phone_number or len(phone_number.strip()) == 0:
                self.data = None
            else:
                self.data = self.formatter.normalize(phone_number)

class HiddenFlagField(HiddenField):
    def __init__(self,*args,**kwargs):
        super(HiddenFlagField, self).__init__(*args,**kwargs)
        self.flags.hidden = True

class UserForm(Form):
    name = TextField('Name', [validators.Length(min=4, max=60)])
    email = TextField('Email Address', [validators.Optional(),validators.Length(min=6, max=35)],filters=[empty_to_none])
    phone = PhoneNumberField('Phone number', [validators.Optional()])


class UserTeamForm(Form):
    team = HiddenFlagField()
    user = SelectField('User',choices=[])


