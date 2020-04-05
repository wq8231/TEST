import requests
import hashlib
import re

import yagmail
class CommonClass():
    def getueser(self):
        tchid=27717

    def getwebtoken(self, name, psw):  # 获取web端token
        url = 'http://yun.slothtek.com/base/api/out/v2/auth/login'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
        data = {'name': name, 'password': psw, 'platform': 'WEB'}
        result = requests.session().post(url=url, headers=headers, data=data)
        token=re.findall("token=(.*?);", str(result.headers))  # 在返回头里找到token)
        return token
    def getpadtoken(self,name,psw):  # 获取pad端token
        url = 'http://bip.slothtek.com/api/v1/auth/login'
        headers = {
            'User-Agent': 'okhttp/3.6.0'}
        data = {'name': name, 'password': psw}
        result = requests.session().post(url=url, headers=headers, data=data)
        token = result.json()['data']['token']
        return token

    def _md5(self, psw):
        md5 = hashlib.md5()
        # psw=bytes(psw.encode('utf-8'))
        md5.update(psw.encode('utf-8'))
        md5psw = md5.hexdigest()
        return md5psw
    def sendemail(self,file):

        sendSmpt = yagmail.SMTP(user="64439772@qq.com",
                                password="pcsxctftwxkobgcb", host='smtp.qq.com')  # 链接服务器，此处的password为邮箱的授权码，非邮箱登录密码
        content = [" test email"]
        sendSmpt.send(to=['64439772@qq.com','wangqian@slothtek.com','tangnian@slothtek.com'], subject='test-report',contents=['report', file])


