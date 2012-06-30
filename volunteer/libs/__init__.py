from urllib import urlopen, urlencode


def send_sms(number,message,settings,prefix="sms."):
    base_url = "https://rest.nexmo.com/sms/json"
    api_key = settings[prefix+"key"]
    api_secret = settings[prefix+"secret"]
    from_name = settings[prefix+"from"]

    response = urlopen("%s?%s"%(base_url,urlencode({'username':api_key,
                                                    'password':api_secret,
                                                    'from':from_name,
                                                    'to':number,
                                                    'text':message,
                                                    })))


