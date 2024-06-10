import requests, random, threading, json, sys
from string import ascii_letters, digits
from datetime import datetime
from uuid import uuid4
import time as sleper
from fake_useragent import UserAgent

requests.packages.urllib3.disable_warnings()

class Fidra:
    def __init__(self):
        with open("username.txt", "r") as file:
            self.names = [line.strip() for line in file] 
        self.start_time = sleper.time()
        self.time = int(datetime.now().timestamp())
        self.numbers = '123456789'
        self.chars = 'qwertyuiopasdfghjklzxcvbnm1234567890'
        self.length = random.randint(6, 8)
        self.created = 0
        self.status = None
        self.password = ''.join(random.choice(ascii_letters + digits) for _ in range(random.randint(8, 15)))
        self.app_id = str("".join(random.choice(self.numbers) for i in range(15)))
        self.year = random.randint(1990, 1999)
        self.month = random.randint(1, 12)
        self.day = random.randint(1, 29)
        self.ig_did = str(uuid4()).upper()
        self.ua = UserAgent()

    def send_to_bot(self, message):
        try:
            with open('bot.json', 'r') as f:
                data = json.load(f)
                self.id = data['id']
                self.token = data['token']
                requests.post(f'https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.id}&text={message}')
        except:
            pass

    def set_cookies(self):
        url = 'https://i.instagram.com/api/v1/public/landing_info/'
        headers = {
            'User-Agent': self.ua.random
        }
        response = requests.get(url, headers=headers).cookies
        try:
            self.mid = response['mid']
            self.csrftoken = response['csrftoken']
            return True
        except:
            return False

    def check_username(self):
        if self.set_cookies():
            url = 'https://www.instagram.com/api/v1/web/accounts/web_create_ajax/attempt/'
            headers = {
                'User-Agent': self.ua.random,
                'X-IG-App-ID': f'{self.app_id}',
                'referer': 'https://www.instagram.com/',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Cookie': f'csrftoken={self.csrftoken}; ig_did={self.ig_did}; ig_nrcb=1; mid={self.mid}',
                'X-CSRFToken': f'{self.csrftoken}'
            }
            while True:
                self.username = ''.join(random.choice(self.chars) for i in range(self.length))
                data = f'email=&username={self.username}&first_name=&opt_into_one_tap=false'
                response = requests.post(url, headers=headers, data=data)
                if 'username_is_taken' not in response.text and response.status_code == 200:
                    print('[1] Checking username')
                    return True
                else:
                    print(f"Searching for available username")

    def create_email(self):
        if self.check_username():
            url = 'https://luxusmail.org/livewire/message/frontend.app'
            headers = {
                'User-Agent': self.ua.random,
                'Content-Type': 'application/json'
            }
            
            domains = ['luxusmail.my.id', 'miramail.my.id', 'ish.my.id', 'highmail.my.id', 'whatisakillowatt.com', 'amik.pro']
            random_domain = random.choice(domains)
            
            data = {
                "fingerprint": {
                    "id": "Sm8UsTrXynqAadXZL9mT",
                    "name": "frontend.app",
                    "locale": "en",
                    "path": "/",
                    "method": "GET",
                    "v": "acj"
                },
                "serverMemo": {
                    "children": {
                        "l1910240968-0": {
                            "id": "ntdfebb7ERKaOGY5oSvW",
                            "tag": "main"
                        }
                    },
                    "errors": [],
                    "htmlHash": "df09fec3",
                    "data": {
                        "messages": [],
                        "deleted": [],
                        "error": "",
                        "email": None,
                        "initial": False,
                        "overflow": False
                    },
                    "dataMeta": [],
                    "checksum": "7dfec930cd7f2f3915105222914b903895ce1d0a1a28fe85271a5356a37fddc7"
                },
                "updates": [
                    {
                        "type": "fireEvent",
                        "payload": {
                            "id": "2yhx",
                            "event": "syncEmail",
                            "params": [f"{self.username}@{random_domain}"]
                        }
                    },
                    {
                        "type": "fireEvent",
                        "payload": {
                            "id": "w0e1l",
                            "event": "fetchMessages",
                            "params": []
                        }
                    }
                ]
            }
            try:
                response = requests.post(url, headers=headers, json=data, verify=True)
                if 'email' in response.json():
                    self.email = response.json()['email']
                    print('[2] Creating Email')
                    return True
                else:
                    return False
            except Exception as e:
                print(e)
                return False
        else:
            print('Missing Cookies')

    def retry_send_code(self, email):
        url = 'https://i.instagram.com/api/v1/accounts/send_verify_email/'
        data = f'device_id=&email={email}'
        headers = {
            'User-Agent': self.ua.random,
            'X-IG-App-ID': f'{self.app_id}',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': f'csrftoken={self.csrftoken}; ig_did={self.ig_did}; ig_nrcb=1; mid={self.mid}',
            'X-CSRFToken': f'{self.csrftoken}',
            'User-Agent': self.ua.random,
            'referer': 'https://www.instagram.com/'
        }
        requests.post(url, headers=headers, data=data)

    def account_status(self, username):
        url = f'https://i.instagram.com/api/v1/users/web_profile_info/?username={username}'
        headers = {
            'User-Agent': self.ua.random,
            'X-IG-App-ID': f'{self.app_id}',
            'referer': 'https://www.instagram.com/'
        }
        response = requests.get(url, headers=headers)
        if 'id' in response.text:
            return 'Active'
        else:
            return 'Suspend'

    def save_info(self, account, session):
        with open('fidra-accounts.txt', 'a') as f:
            f.write(f'{account}\n')
        with open('fidra-sessions.txt', 'a') as s:
            s.write(f'session:{session}\n')

    def send_code(self):
        if self.check_birthday():
            url = 'https://i.instagram.com/api/v1/accounts/send_verify_email/'
            data = f'device_id=&email={self.email}'
            headers = {
                'User-Agent': self.ua.random,
                'X-IG-App-ID': f'{self.app_id}',
                'x-requested-with': 'XMLHttpRequest',
                'referer': 'https://www.instagram.com/',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Cookie': f'csrftoken={self.csrftoken}; ig_did={self.ig_did}; ig_nrcb=1; mid={self.mid}',
                'X-CSRFToken': f'{self.csrftoken}'
            }
            send = requests.post(url, headers=headers, data=data)
            if '"email_sent":true' in send.text:
                print('[3] Sending Verification code')
                sleper.sleep(4)
                return True
            else:
                return False
        else:
            print('Error In Check Birthday')

    def get_code(self):
        if self.send_code():
            url = f'https://api.internal.temp-mail.io/api/v3/email/{self.email}/messages'
            headers = {
                'User-Agent': self.ua.random,
                'Content-Type': 'application/json'
            }
            while True:
                for _ in range(5):
                    response = requests.get(url, headers=headers, verify=False)
                    if 'Instagram' in response.text:
                        for messages in response.json():
                            subject = messages['subject']
                            self.code = subject.split(' is your Instagram code')[0]
                            return True
                    else:
                        print(f'\r[4] Waiting Verification code', end='')
                        sleper.sleep(5)
                print('\rResend', end='')
                self.retry_send_code(self.email)
        else:
            print('Email Not sent')

    def check_code(self):
        if self.get_code():
            print('\n[5] Verifying The Code')
            url = 'https://i.instagram.com/api/v1/accounts/check_confirmation_code/'
            data = f'code={self.code}&device_id=&email={self.email}'
            headers = {
                'User-Agent': self.ua.random,
                'X-IG-App-ID': f'{self.app_id}',
                'Content-Type': 'application/x-www-form-urlencoded',
                'referer': 'https://www.instagram.com/',
                'Cookie': f'csrftoken={self.csrftoken}; ig_did={self.ig_did}; ig_nrcb=1; mid={self.mid}',
                'X-CSRFToken': f'{self.csrftoken}',

            }
            response = requests.post(url, headers=headers, data=data)
            if 'signup_code' in response.text:
                self.signup_code = response.json()['signup_code']
                return True
            else:
                print(response.text)
                return False

    def create_account(self):
        if self.check_code():
            print('[6] Creating Account')
            url = 'https://www.instagram.com/accounts/web_create_ajax/'
            time = int(datetime.now().timestamp())
            data = f'enc_password=#PWD_INSTAGRAM_BROWSER:0:{time}:{self.password}&email={self.email}&username={self.username}&first_name=Created By Fidra\n&month={self.month}&day={self.day}&year={self.year}&client_id=&seamless_login_enabled=1&tos_version=row&force_sign_up_code={self.signup_code}'
            headers = {
                'User-Agent': self.ua.random,
                'X-IG-App-ID': f'{self.app_id}',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Cookie': f'csrftoken={self.csrftoken}; ig_did={self.ig_did}; ig_nrcb=1; mid={self.mid}',
                'X-CSRFToken': f'{self.csrftoken}',
                'referer': 'https://www.instagram.com/'
            }
            response = requests.post(url, headers=headers, data=data)
            if 'user_id' in response.text:
                self.end_time = sleper.time()
                self.elapsed_time = int(self.end_time - self.start_time)
                print('-' * 40)
                print('Successfully Created')
                print(f'username : {self.username}')
                print(f'password : {self.password}')
                print(f'email : {self.email}')
                print(f'Account Status : {self.account_status(self.username)}')
                print(f'The process took {self.elapsed_time} seconds')
                print('Account saved in "fidra-accounts.txt"')
                print('-' * 40)
                session = response.cookies['sessionid']
                account = f'{self.username}:{self.password}'
                message = f'New IG Account Created\nusername: {self.username}\npassword: {self.password}\nemail: {self.email}\nAccount Status : {self.account_status(self.username)}\nDeveloper : https://www.instagram.com/f09l/'
                self.save_info(account, session)
                self.send_to_bot(message)
            else:
                if '"The IP address you are using has been flagged as an open proxy."' in response.text:
                    response = '{"account_created": true, "status": "ok"}'
                print('-' * 40)
                print(response.text)
                print('-' * 40)
        else:
            print('Failed To Create Account')


print("""
  __ _     _           
 / _(_)   | |          
| |_ _  __| |_ __ __ _ 
|  _| |/ _` | '__/ _` |
| | | | (_| | | | (_| |
|_| |_|\__,_|_|  \__,_|
                       
Instagram Accounts Creator v1.0
Powered By @f09l
""")

fidra = Fidra()
try:
    count = int(input('accounts count : '))
except:
    count = 0
for _ in range(count):
    fidra.create_account()
