import requests, random, threading, json, sys, os
from string import ascii_letters, digits
from datetime import datetime
from uuid import uuid4
import time as sleper
from fake_useragent import UserAgent

requests.packages.urllib3.disable_warnings()

def proxy():
    try:
        proxies = requests.get('https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks4&timeout=100000&country=all&ssl=all&anonymity=all').text
        os.makedirs('Data', exist_ok=True)  # Create the Data directory if it doesn't exist
        with open('Data/proxy.txt', 'w') as f:
            f.write(proxies)
    except Exception as e:
        print(f"Error fetching proxies: {e}")
        proxies = requests.get('https://raw.githubusercontent.com/MN4WN1-777/ignew/master/Data/proxy.txt').text
        os.makedirs('Data', exist_ok=True)  # Create the Data directory if it doesn't exist
        with open('Data/proxy.txt', 'w') as f:
            f.write(proxies)

class Fidra:
    def _init_(self):
        with open("username.txt", "r") as file:
            self.names = [line.strip() for line in file] 
        self.start_time = sleper.time()
        self.time = int(datetime.now().timestamp())
        self.numbers = '123456789'
        self.chars = 'qwertyuiopasdfghjklzxcvbnm1234567890'
        self.length = random.randint(6, 8)
        self.created = 0
        self.status = None
        self.password = ''.join(random.choice(ascii_letters + digits) for _ in range(random.randint(8, 14)))
        self.app_id = str("".join(random.choice(self.numbers) for i in range(15)))
        self.year = random.randint(1990, 1999)
        self.month = random.randint(1, 12)
        self.day = random.randint(1, 20)
        self.ig_did = str(uuid4()).upper()
        self.ua = UserAgent()
        self.proxy_list = self.load_proxies()
        self.proxy_index = 0

    def load_proxies(self):
        try:
            with open('Data/proxy.txt', 'r') as f:
                proxies = f.read().splitlines()
            return proxies
        except Exception as e:
            print(f"Error loading proxies: {e}")
            return []

    def get_next_proxy(self):
        if self.proxy_list:
            proxy = self.proxy_list[self.proxy_index]
            self.proxy_index = (self.proxy_index + 1) % len(self.proxy_list)
            return {"http": f"socks4://{proxy}", "https": f"socks4://{proxy}"}
        return None

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
        proxy = self.get_next_proxy()
        response = requests.get(url, headers=headers, proxies=proxy, verify=False).cookies
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
            proxy = self.get_next_proxy()
            while True:
                self.username = ''.join(random.choice(self.chars) for i in range(self.length))
                data = f'email=&username={self.username}&first_name=&opt_into_one_tap=false'
                response = requests.post(url, headers=headers, data=data, proxies=proxy, verify=False)
                if 'username_is_taken' not in response.text and response.status_code == 200:
                    print('[1] Checking username')
                    return True
                else:
                    print(f"Searching for available username")

    def create_email(self):
        if self.check_username():
            url = 'https://api.internal.temp-mail.io/api/v3/email/new'
            headers = {
                'User-Agent': self.ua.random,
                'Content-Type': 'application/json'
            }
            data = {
                "min_name_length": 5,
                "max_name_length": 7
            }
            proxy = self.get_next_proxy()
            try:
                response = requests.post(url, headers=headers, json=data, proxies=proxy, verify=False)
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

    def check_birthday(self):
        if self.create_email():
            url = 'https://www.instagram.com/web/consent/check_age_eligibility/'
            data = f'day={self.day}&month={self.month}&year={self.year}'
            headers = {
                'User-Agent': self.ua.random,
                'X-IG-App-ID': f'{self.app_id}',
                'Content-Type': 'application/x-www-form-urlencoded',
                'referer': 'https://www.instagram.com/',
                'Cookie': f'csrftoken={self.csrftoken}; ig_did={self.ig_did}; ig_nrcb=1; mid={self.mid}',
                'X-CSRFToken': f'{self.csrftoken}'
            }
            proxy = self.get_next_proxy()
            check = requests.post(url, headers=headers, data=data, proxies=proxy, verify=False)
            if '"status":"ok"' in check.text:
                return True
            else:
                return False
        else:
            print('Email Not Created')

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
        proxy = self.get_next_proxy()
        requests.post(url, headers=headers, data=data, proxies=proxy, verify=False)

    def account_status(self, username):
        url = f'https://i.instagram.com/api/v1/users/web_profile_info/?username={username}'
        headers = {
            'User-Agent': self.ua.random,
            'X-IG-App-ID': f'{self.app_id}',
            'referer': 'https://www.instagram.com/'
        }
        proxy = self.get_next_proxy()
        response = requests.get(url, headers=headers, proxies=proxy, verify=False)
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
            proxy = self.get_next_proxy()
            send = requests.post(url, headers=headers, data=data, proxies=proxy, verify=False)
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
            proxy = self.get_next_proxy()
            while True:
                for _ in range(5):
                    response = requests.get(url, headers=headers, proxies=proxy, verify=False)
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
                'X-CSRFToken': f'{self.csrftoken}'
            }
            proxy = self.get_next_proxy()
            response = requests.post(url, headers=headers, data=data, proxies=proxy, verify=False)
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
            proxy = self.get_next_proxy()
            response = requests.post(url, headers=headers, data=data, proxies=proxy, verify=False)
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
                print('-' * 40)
                print(response.text)
                print('-' * 40)
        else:
            print('Failed To Create Account')


print("""

                       
Instagram Accounts Creator v1.0
Powered 
""")

proxy()  # Fetch and save proxies
fidra = Fidra()
try:
    count = int(input('accounts count : '))
except:
    count = 0
for _ in range(count):
    fidra.create_account()
