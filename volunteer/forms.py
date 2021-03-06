from volunteer.models import PhoneNumberFormatter

from wtforms import Form, TextField, validators, SelectField, HiddenField, DateTimeField, DateField, IntegerField
from wtforms.fields import Field
from wtforms.widgets import TextInput

class SmsForm(Form):
    type = TextField()
    to = TextField()
    msisdn = TextField()
    network_code = TextField()
    message_id = TextField()
    message_timestamp = DateTimeField(format="%Y-%m-%d %H:%M:%S")
    text = TextField()
    concat = TextField()
    concat_ref = TextField()
    concat_total = IntegerField()
    concat_part = IntegerField()

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

class EventForm(Form):
    date = DateTimeField('Date', [validators.Required()], format='%d.%m.%Y %H:%M')
    title = TextField('Title', [validators.Optional()],filters=[empty_to_none])
    theme = TextField('Theme', [validators.Optional()],filters=[empty_to_none])

class UserForm(Form):
    name = TextField('Name', [validators.Length(min=4, max=60)])
    email = TextField('Email Address', [validators.Optional(),validators.Length(min=6, max=35)],filters=[empty_to_none])
    phone = PhoneNumberField('Phone number', [validators.Optional()])


class UserTeamForm(Form):
    team = HiddenFlagField()
    user = SelectField('User',choices=[])


class GenEventForm(Form):
    start_date = DateField('Start date', [validators.Required()], format='%d.%m.%Y')
    end_date = DateField('End date', [validators.Required()], format='%d.%m.%Y')
    gen_day = SelectField('Day of week', choices=[(7, 'Sunday'), (1, 'Monday'), (2, 'Tuesday'), (3,'Wednesday'),(4,'Thursday'),(5,'Friday'),(6,'Saturday')],coerce=int,default=7)
    gen_time = TextField('Time', [validators.Required()],default="10:00")
    gen_title = TextField('title string', [validators.Required()], default="%A %B %d %H:%M")


class SmsDeliveryForm(Form):
    to = TextField()
    network_code = TextField()
    message_id = TextField()
    msisdn = TextField()
    status = TextField()
    err_code = IntegerField()
    scts = DateTimeField(format="%y%m%d%H%M")
    message_timestamp = DateTimeField(format="%Y-%m-%d %H:%M:%S")