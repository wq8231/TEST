import requests
import hashlib
import re
import unittest
from common import CommonClass
import math


class MobileStuTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.stumd5psw = CommonClass()._md5('111111')  # 账号密码
        self.tchname = '27819'
        self.token = CommonClass().getpadtoken(self.tchname, self.stumd5psw)
        # self.token = '6cb42a26500049bc98d28689d5fc0137'
        self.headers = {
            'token': self.token,
            'userid': self.tchname,
            'Content-Type':'application/json;charset=UTF-8',
            'User-Agent': 'okhttp/3.6.0'}



    def test_01(self):  # 班级资源
        '''班级资源'''
        url = 'http://api.slothtek.com/api/v1/resource/class/query?classId=556&subjectId=-1&fileTypes=-1&pageIndex=0&pageSize=12'
        headers = self.headers
        result = requests.get(url=url, headers=headers)
        print(result.text)
        print(url)

        self.assertEqual(result.json()['code'],
                         200)

    def test_02(self):  # 学生资源
        '''我的资源'''
        url = 'http://api.slothtek.com/api/v1/resource/student/query?subjectId=-1&fileTypes=-1&pageIndex=0&pageSize=12'
        headers = self.headers
        result = requests.get(url=url, headers=headers)
        print(result.text)
        print(url)

        self.assertEqual(result.json()['code'],
                         200)

    def test_03(self):  # 班级微课
        '''班级微课'''
        url = 'http://api.slothtek.com/api/v1/resource/class/query?classId=556&fileTypes=.mp4,.flv&subjectId=-1&pageIndex=0&pageSize=12'
        headers = self.headers
        result = requests.get(url=url, headers=headers)
        print(result.text)
        print(url)

        self.assertEqual(result.json()['code'],
                         200)

    def test_04(self):  # 我的微课
        '''班级微课'''
        url = 'http://api.slothtek.com/api/v1/resource/student/query?subjectId=-1&fileTypes=.mp4,.flv&pageIndex=0&pageSize=12'
        headers = self.headers
        result = requests.get(url=url, headers=headers)
        print(result.text)
        print(url)

        self.assertEqual(result.json()['code'],
                         200)

    def test_05(self):  # 优秀作业
        '''优秀作业'''
        url = 'http://api.slothtek.com/api/v1/mission/class/excellent?classId=556&schoolId=40&pageIndex=0&pageSize=10'
        headers = self.headers
        result = requests.get(url=url, headers=headers)
        print(result.text)
        print(url)

        self.assertEqual(result.json()['code'],
                         200)

    def test_06(self):  # 成绩报告列表
        '''成绩报告列表'''
        url = 'http://api.slothtek.com/api/v1/mission/student/report?userId=27819&schoolId=40&courseId=0&pageIndex=0&pageSize=8'
        headers = self.headers
        result = requests.get(url=url, headers=headers)
        print(result.text)
        print(url)

        self.assertEqual(result.json()['code'],
                         200)

    def test_07(self):  # 成绩报告详情
        '''成绩报告详情'''
        url = 'http://api.slothtek.com/api/v1/mission/student/report/detail?userId=27819&missionId=7290'
        headers = self.headers
        result = requests.get(url=url, headers=headers)
        print(result.text)
        print(url)

        self.assertEqual(result.json()['code'],
                         200)

    def test_08(self):  # 已提交作业查看
        '''已提交作业查看'''
        url = 'http://api.slothtek.com/api/v1/mission/student/answer/detail2?commitId=27819&missionId=7290'
        headers = self.headers
        result = requests.get(url=url, headers=headers)
        print(result.text)
        print(url)

        self.assertEqual(result.json()['code'],
                         200)

    def test_09(self):  # 获取学生科目
        '''获取学生科目'''
        url = 'http://api.slothtek.com/api/v1/mission/student/subject?stageId=2'
        headers = self.headers
        result = requests.get(url=url, headers=headers)
        print(result.text)
        print(url)

        self.assertEqual(result.json()['code'],
                         200)

    def test_10(self):  # 获取互动消息
        '''获取互动消息'''
        url = 'http://bip.slothtek.com/api/v1/msg/query/list?userId=27819&type=2&pageIndex=0&pageSize=10'
        headers = self.headers
        result = requests.get(url=url, headers=headers)
        print(result.text)
        print(url)
        self.assertEqual(result.json()['code'],
                         200)

    def test_11(self):  # 发送消息
        '''发送消息'''
        url = 'http://bip.slothtek.com/api/v1/msg/send'
        headers = self.headers
        data='{"acceptor":[{"acceptId":27717,"acceptName":"回归测试用","acceptType":4}],"classify":0,"msg":"测试消息测试消息测试消息测试消息测试消息测试消息","title":"普通消息","type":2}'
        result = requests.post(url=url, headers=headers,data=data.encode())
        print(result.text)
        print(url)

        self.assertEqual(result.json()['code'],
                         200)



    def test_12(self):  # 错题收集
        '''错题收集'''
        url = 'http://api.slothtek.com/api/v1/mission/student/subject?stageId=2'
        headers = self.headers
        result = requests.get(url=url, headers=headers)
        print(result.text)
        print(url)


        self.assertEqual(result.json()['code'],
                         200)


    def test_13(self):  # 综合分析
        '''综合分析'''
        url = 'http://api.slothtek.com/api/v1/mission/common/student/subject/kpi?schoolId=40&studentId=27819&subjectId=24'
        headers = self.headers
        result = requests.get(url=url, headers=headers)
        print(result.text)
        print(url)

        self.assertEqual(result.json()['code'],
                         200)

    def test_14(self):  # 薄弱知识点
        '''薄弱知识点'''
        url = 'http://api.slothtek.com/api/v1/push/mission/weakness?subjectId=24&studentId=27819&schoolId=40'
        headers = self.headers
        result = requests.get(url=url, headers=headers)
        print(result.text)
        print(url)

        self.assertEqual(result.json()['code'],
                         200)
    def test_15(self):  # 空中课堂
        '''空中课堂'''
        url = 'http://api.slothtek.com/api/v1/live/living?studentId=27819'
        headers = self.headers
        result = requests.get(url=url, headers=headers)
        print(result.text)
        print(url)

        self.assertEqual(result.json()['code'],
                         200)
    def test_16(self):  #获取资源路径
        '''获取资源路径'''
        url='http://api.slothtek.com/api/v1/resource/download?resId=45371'
        headers = self.headers
        result = requests.post(url=url, headers=headers)
        print(result.text)
        print(url)

        globals()["filename"] =result.json()['data']['link']
        self.assertEqual(result.json()['data']['uuid'],
                         '8fcb34bd62e14337992fc80f995e5344')

    def test_17(self):  # 下载资源
        '''下载资源'''
        url=globals()["filename"]
        headers = self.headers
        result = requests.get(url=url, headers=headers)
        print(result.text)
        print(url)

        self.assertTrue(len(result.text)>3000)




