import requests
import logging
import threading
import time
from enum import Enum


class CapthaError(Exception):
    def __init__(self, json):
        message = json
        # Call the base class constructor with the parameters it needs
        super(AuthError, self).__init__(message)


class AuthError(Exception):
    def __init__(self, json):
        message = json
        # Call the base class constructor with the parameters it needs
        super(AuthError, self).__init__(message)

class Request(object):
    __slots__ = ('_api', '_method_name', '_method_args')

    def __init__(self, api, method_name):
        self._api = api
        self._method_name = method_name
        self._method_args = {}

    def __getattr__(self, method_name):
        return Request(self._api, self._method_name + '.' + method_name)

    def __call__(self, **method_args):
        method_args['access_token'] = self._api.access_token
        self._method_args = method_args

        return self._api.method(self)

class Client(object):
    auth_url = "https://oauth.vk.com/token"
    request_template_url = "https://api.vk.com/method/"
    id = -1

    def __getattr__(self, method_name):
        return Request(self, method_name)

    def __call__(self, method_name, **method_kwargs):
        return getattr(self, method_name)(**method_kwargs)


    def __init__(self, login="", password="", access_token=None, id=-1):
        self.session = requests.session()
        self.id = id
        if access_token is not None:
            self.access_token = access_token
        else:
            self.auth_params = {
                "scope": "all",
                "client_id": "2274003",
                "client_secret": "hHbZxrka2uZ6jB1inYsH",
                "fa_supported": 1,
                "lang": "ru",
                "device_id": "",
                "grant_type": "password",
                "username": login,
                "password": password,
                "libverify_support": "1",
                "v": "5.67"
            }
            self.session.headers['User-Agent'] = 'VKAndroidApp/4.9-1118 (Android 5.1; SDK 22; armeabi-v7a; UMI IRON; ru'
            answ = self.session.post(self.auth_url, data=self.auth_params).json()
            if 'error' in answ:
                print(answ['error'])
                if answ['error']['error_code'] == 14:
                    captcha = input('Enter captcha from here {}: '.format(answ['error']['captcha_img']))
                    params = self.auth_params
                    params['captcha_sid'] = answ['error']['captcha_sid']
                    params['captcha_key'] = captcha
                    answ = self.session.post(self.auth_url, data=params).json()

            if 'access_token' in answ:
                self.access_token = answ['access_token']
            else:
                raise AuthError(answ)

    def method(self, request):
        params = request._method_args
        params['access_token'] = self.access_token
        params['v'] = "5.67"
        resp = self.session.post(url=self.request_template_url + request._method_name, data=params).json()
        if 'error' in resp:
            if resp['error']['error_code'] == 14:
                captcha = input('Enter captcha from here {}: '.format(resp['error']['captcha_img']))
                params['captcha_sid'] = resp['error']['captcha_sid']
                params['captcha_key'] = captcha
                return self.method(requests)
            else:
                return resp
            print(resp)
        return resp['response']


class LongPool(object):
    def __init__(self, url, key, ts):
        self.url = url
        self.key = key
        self.ts = ts

    def getPoolURL(self):
        return ('https://{}?act=a_check&key={}&ts={}&wait=25&mode=2&version=1').format(self.url, self.key, self.ts)

    def pool(self):
        session = requests.session()
        answer = session.get(self.getPoolURL(), timeout=27.0)
        if answer.status_code == 200:
            if 'ts' in answer.json():
                self.ts = answer.json()['ts']
            return answer.json()
        else:
            raise Exception(
                'Error with get request {}. Answers contains code: {}'.format(answer.url, answer.status_code))


def getLongPoolServer(client):
    try:
        answ = client.messages.getLongPollServer()
        server = LongPool(answ['server'], answ['key'], answ['ts'])
    except Exception as ex:
        return getLongPoolServer(client)
    return server

class Errors(Enum):
    HISTORY_FAILED = 1
    KEY_IS_NOT_VALID = 2
    USER_INFO_LOST = 3
    VERSION_IS_NOT_VALID = 4

class Codes(Enum):
    FLAG_CHANGED = 1
    FLAG_SETUPED = 2
    FLAG_RESETED = 3
    FLAG_CHANGED_COMMUNITY = 11
    FLAG_SETUPED_COMMUNITY = 12
    FLAG_RESETED_COMMUNITY = 10
    NEW_MESSAGE = 4
    READ_INCOMING_MESSAGES = 6
    READ_OUTCOMING_MESSAGES = 7
    USER_ONLINE = 8
    USER_GONE_OFFLINE = 9
    CHAT_NAME_CHANGED = 51
    USER_TYPING_PRIVATE = 61
    USER_TYPING_CHAT = 62
    USER_CALLS = 70
    UNREAD_MESSAGES_COUNTER_UPDATE = 80
    NOTIFICATIONS_SETTINGS_UPDATE = 114



class VKPooler(object):


    def __init__(self):
        self.functions = {}

    def addHandler(self, code, function):
        if code.value in self.functions:
            self.functions[code.value].append(function)
        else:
            self.functions[code.value] = [function]

    errors = {Errors.HISTORY_FAILED: 'Error with history ot ts event',
              Errors.KEY_IS_NOT_VALID: 'Key is not valid. Relogin pls',
              Errors.USER_INFO_LOST: 'Restart it with new key',
              Errors.VERSION_IS_NOT_VALID: 'Minimal(ot maximal) version is wrong'}

    def startPooling(self, client):
        threading.Thread(target=self.Pooling, args=(client,)).start()

    def Pooling(self, client):
        server = getLongPoolServer(client)
        while True:
            try:
                answ = server.pool()
                if 'error' in answ:
                    for error in Errors:
                        if error.value == answ['error']:
                            logging.error(Errors[error.value])
                            time.sleep(1)
                            server = getLongPoolServer(client)
                else:
                    for update in answ['updates']:
                        for code in Codes:
                            if update[0] == code.value:
                                if code.value in self.functions:
                                    for function in self.functions[code.value]:
                                        function(client, update)
            except Exception as ex:
                print(ex)
                time.sleep(1)
                server = getLongPoolServer(client)
