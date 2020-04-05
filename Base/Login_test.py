import requests
import hashlib
import re
import unittest
from common import CommonClass
import HTMLTestRunner


class LoginTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.admd5psw = LoginTest()._md5('slothtekadmin')  # 管理员账号密码
        self.adname = '19221'
        self.tchname = '27717'
        self.tchmd5psw = LoginTest()._md5('123456')
        self.stuname = '28000'
        self.stumd5psw = LoginTest()._md5('111111')
        self.wpsw = LoginTest()._md5('oiuytrewq')  # 错误密码

    def test_01(self):  # web登录页面打开成功
        '''web登录页面打开成功'''
        url = 'http://yun.slothtek.com/'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
        result = requests.get(url=url, headers=headers)
        print(result.text)
        print(url)

        self.assertEqual('<Response [200]>', str(result))

    def test_02(self):  # web管理员登录成功
        '''web管理员登录成功'''
        globals()["token"] = ''

        url = 'http://yun.slothtek.com/base/api/out/v2/auth/login'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
        data = {'name': self.adname, 'password': self.admd5psw, 'platform': 'WEB'}
        result = requests.session().post(url=url, headers=headers, data=data)
        print(result.text)
        print(url)

        self.assertEqual(result.text,
                         '{"code":200,"msg":"登录成功","data":null,"params":null,"sysSign":null,"succeed":true}')
        # return token

    def test_03(self):  # web输入错误密码登录
        '''web输入错误密码登录'''
        url = 'http://yun.slothtek.com/base/api/out/v2/auth/login'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
        data = {'name': self.adname, 'password': self.wpsw, 'platform': 'WEB'}
        result = requests.session().post(url=url, headers=headers, data=data)
        print(result.text)
        print(url)

        self.assertEqual(result.text,
                         '{"code":500,"msg":"用户名或密码错误","data":null,"params":null,"sysSign":null,"succeed":false}')

    def test_04(self):  # web登录老师账号
        '''web登录老师账号'''
        url = 'http://yun.slothtek.com/base/api/out/v2/auth/login'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
        data = {'name': self.tchname, 'password': self.tchmd5psw, 'platform': 'WEB'}
        result = requests.session().post(url=url, headers=headers, data=data)
        print(result.text)
        print(url)

        globals()["token"] = re.findall("token=(.*?);", str(result.headers))  # 在返回头里找到token
        self.assertEqual(result.text,
                         '{"code":200,"msg":"登录成功","data":null,"params":null,"sysSign":null,"succeed":true}')

    def test_05(self):  # web登录学生账号
        '''web登录学生账号'''
        url = 'http://yun.slothtek.com/base/api/out/v2/auth/login'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
        data = {'name': self.stuname, 'password': self.stumd5psw, 'platform': 'WEB'}
        result = requests.session().post(url=url, headers=headers, data=data)
        print(result.text)
        print(url)

        self.assertEqual(result.text,
                         '{"code":200,"msg":"登录成功","data":null,"params":null,"sysSign":null,"succeed":true}')

    def test_06(self):  # pad登录老师账号
        '''pad登录老师账号'''
        url = 'http://bip.slothtek.com/api/v1/auth/login'
        headers = {
            'User-Agent': 'okhttp/3.6.0'}
        data = {'name': self.tchname, 'password': self.tchmd5psw}
        result = requests.session().post(url=url, headers=headers, data=data)
        print(result.text)
        print(url)

        self.assertEqual(result.json()['code'], 200)

    def test_07(self):  # pad登录学生账号
        '''pad登录学生账号'''
        url = 'http://bip.slothtek.com/api/v1/auth/login'
        headers = {
            'User-Agent': 'okhttp/3.6.0'}
        data = {'name': self.stuname, 'password': self.stumd5psw}
        result = requests.session().post(url=url, headers=headers, data=data)
        print(result.text)
        print(url)

        self.assertEqual(result.json()['code'], 200)

    def test_08(self):  # pad登录输入错误密码
        '''pad登录输入错误密码'''
        url = 'http://bip.slothtek.com/api/v1/auth/login'
        headers = {
            'User-Agent': 'okhttp/3.6.0'}
        data = {'name': self.stuname, 'password': self.wpsw, 'platform': 'WEB'}
        result = requests.session().post(url=url, headers=headers, data=data)
        print(result.text)
        print(url)

        self.assertEqual(result.json()['msg'],
                         "用户名或密码错误")

    def test_09(self):  # web退出登录
        '''web退出登录'''
        url = 'http://yun.slothtek.com/base/api/out/v2/auth/logout'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
            'Cookie': 'userId=%s;token=%s' % (self.tchname, globals()["token"][0]), 'token': globals()["token"][0]}

        result = requests.session().post(url=url, headers=headers)
        print(result.text)
        print(url)

        self.assertEqual(result.text,
                         '{"code":200,"msg":null,"data":null,"params":null,"sysSign":null,"succeed":true}')

    def test_10(self):  # v1/user/info  老师
        ''' v1/user/info  老师'''
        token = CommonClass().getpadtoken(self.tchname, self.tchmd5psw)
        url = 'http://bip.slothtek.com/api/v1/user/info'
        headers = {'userid': self.tchname, 'token': token, 'User-Agent': 'okhttp/3.6.0'}
        result = requests.session().get(url=url, headers=headers)
        print(result.text)
        print(url)

        self.assertEqual(result.json()['code'], 200)

    def test_11(self):  # v1/user/info  学生
        ''' v1/user/info  学生'''
        token = CommonClass().getpadtoken(self.stuname, self.stumd5psw)
        url = 'http://bip.slothtek.com/api/v1/user/info'
        headers = {'userid': self.stuname, 'token': token, 'User-Agent': 'okhttp/3.6.0'}
        result = requests.session().get(url=url, headers=headers)
        print(result.text)
        print(url)

        self.assertEqual(result.json()['code'], 200)

    def _md5(self, psw):
        md5 = hashlib.md5()
        # psw=bytes(psw.encode('utf-8'))
        md5.update(psw.encode('utf-8'))
        md5psw = md5.hexdigest()
        return md5psw

# if __name__ == '__main__':
#     filepath = 'G:\SL_Regression_Test(Release)/htmlreport.html'
#     ftp = open(filepath, 'wb')
#     suite = unittest.TestSuite()
#     suite.addTest(LoginTest('test_a'))
#     suite.addTest(LoginTest('test_b'))
#     runner = HTMLTestRunner.HTMLTestRunner(stream=ftp, title='welcome to this web')
#     runner.run(suite)
