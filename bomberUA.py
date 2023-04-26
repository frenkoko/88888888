import user_agent
import random
import requests
import uuid

iteration = 0
_name = ''
for x in range(12):
    _name = _name + random.choice(list('123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'))
    password = _name + random.choice(list('123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'))
    username = _name + random.choice(list('123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'))


def sendUA(phone):
    request_timeout = 0.00001
    iteration = 0
    _email = _name + f'{iteration}' + '@gmail.com'
    email = _name + f'{iteration}' + '@gmail.com'
    _phone = phone
    number = _phone
    phone_9 = _phone[2:]
    phone_plus = "+" + _phone

    try:
        requests.post('https://my.telegram.org/auth/send_password', params={'phone': "+" + _phone})
    except Exception as e:
        pass
