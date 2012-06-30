from urllib import urlopen, urlencode


def send_sms(number,message):
    base_url = "https://rest.nexmo.com/sms/json"
    api_key = ""
    api_secret = ""
    from_name = ""

    response = urlopen("%s?%s"%(base_url,urlencode({'username':api_key,
                                                    'password':api_secret,
                                                    'from':from_name,
                                                    'to':number,
                                                    'text':message,
                                                    })))
