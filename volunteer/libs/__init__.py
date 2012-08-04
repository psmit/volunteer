from datetime import datetime
import json
from urllib import urlopen, urlencode
import boto

from decimal import Decimal

from ..models import (
    DBSession,
    SmsMessage,
    SmsMessagePart,
)

def send_sms(number,message,settings,prefix="sms.",from_name=None):
    base_url = "https://rest.nexmo.com/sms/json"
    api_key = settings[prefix+"key"]
    api_secret = settings[prefix+"secret"]
    if from_name is None:
        from_name = settings[prefix+"from"]

    response = urlopen("%s?%s"%(base_url,urlencode({'username':api_key,
                                                    'password':api_secret,
                                                    'from':from_name,
                                                    'to':number,
                                                    'text':message,
                                                    })))

    sms = None
    if response.code == 200:
        ret = json.load(response)
        sms = SmsMessage()
        sms.from_name = from_name
        sms.to = number
        sms.text = message
        sms.time = datetime.now()

        DBSession.add(sms)

        sms.num_message_parts = int(ret['message-count'])

        for i,message in enumerate(ret['messages']):
            part = SmsMessagePart()
            part.part_id = i
            part.sms_message = sms
            part.message_id = message['message-id']
            part.to = message['to']
            part.status = int(message['status'])

            part.remaining_balance = int(Decimal(message['remaining-balance'])*10**5)
            part.message_price = int(Decimal(message['message-price'])*10**5)

            if 'error-text' in message:
                part.error_text = message['error-text']

            DBSession.add(part)

    return sms



def send_email(mailaddress,subject,message,settings,prefix="aws."):
    from_email = "volunteer@smitmail.eu"

    connection = boto.connect_ses(settings[prefix+'access_key_id'],
                                  settings[prefix+'secret_access_key'])

    connection.send_email(from_email,subject,message,[mailaddress])