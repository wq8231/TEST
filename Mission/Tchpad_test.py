import requests
import hashlib
import re
import unittest
from common import CommonClass
import math


class MobileTchTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.tchmd5psw = CommonClass()._md5('123456')  # 管理员账号密码
        self.tchname = '27717'
        self.token = CommonClass().getpadtoken(self.tchname, self.tchmd5psw)
        # self.token = '6cb42a26500049bc98d28689d5fc0137'
        self.headers = {
            'token': self.token,
            'userid': self.tchname,
            'User-Agent': 'okhttp/3.6.0'}

    def test_01(self):  # mission/teacher/info
        '''mission/teacher/info'''
        url = 'http://api.slothtek.com/api/v1/mission/teacher/info'
        headers = self.headers
        result = requests.get(url=url, headers=headers)
        print(result.text)
        print(url)

        self.assertEqual(result.json()['code'], 200)

    def test_02(self):  # 获取普通作业类型
        '''获取普通作业类型'''
        url = 'http://api.slothtek.com/api/v1/mission/common/topic'
        headers = self.headers
        result = requests.get(url=url, headers=headers)
        print(result.text)
        print(url)

        self.assertEqual(result.json()['code'], 200)

    def test_03(self):  # 获取知识点
        '''获取知识点'''
        url = 'http://api.slothtek.com/api/v1/core/kpi?subjectId=19&stageId=2'
        headers = self.headers
        result = requests.get(url=url, headers=headers)
        print(result.text)
        print(url)

        self.assertEqual(result.json()['code'], 200)

    def test_04(self):  # 获取册别信息
        '''获取册别信息'''
        url = 'http://api.slothtek.com/api/v1/core/book?versionId=75'
        headers = self.headers
        result = requests.get(url=url, headers=headers)
        print(result.text)
        print(url)

        self.assertEqual(result.json()['code'], 200)

    def test_05(self):  # 获取难度和类型
        '''获取难度和类型'''
        url = 'http://api.slothtek.com/api/v1/core/questiontype?subjectId=19&stageId=2'
        headers = self.headers
        result = requests.get(url=url, headers=headers)
        print(result.text)
        print(url)

        self.assertEqual(result.json()['code'], 200)

    def test_06(self):  # 获取册别信息
        '''获取册别信息'''
        url = 'http://api.slothtek.com/api/v1/core/kpi?subjectId=19&stageId=2'
        headers = self.headers
        result = requests.get(url=url, headers=headers)
        print(result.text)
        print(url)

        self.assertEqual(result.json()['code'], 200)

    def test_07(self):  # 根据知识点查题库题
        '''根据知识点查题库题'''
        url = 'http://yun.slothtek.com/mission/api/v1/core/question/by/kpi?stageId=2&subjectId=19&pressId=75&kpiStr=2071&questionType=-1&difficult=-1&clearData=true&pageIndex=1&pageSize=10'
        headers = self.headers
        result = requests.get(url=url, headers=headers)
        print(result.text)
        print(url)

        self.assertTrue(len(result.text) > 10000)

    def test_08(self):  # 获取章节信息
        '''获取章节信息'''
        url = 'http://api.slothtek.com/api/v1/core/book/node?textbookId=13410'
        headers = self.headers
        result = requests.get(url=url, headers=headers)
        print(result.text)
        print(url)

        self.assertEqual(result.json()['code'], 200)

    def test_09(self):  # 获取题库作业图片
        '''获取题库作业图片'''
        url = 'http://item.slothtek.com/imgs/bcbe2b8ae42d4f7cba8a5ce0bcd75670.png'
        headers = self.headers
        result = requests.get(url=url, headers=headers)
        print(result.text)
        print(url)

        self.assertTrue(len(result.text) > 9000)

    def test_10(self):  # 获取老师班级学生信息
        '''获取老师班级学生信息'''
        url = 'http://bip.slothtek.com/api/v1/teacher/query/myclass?teacherId=%s&schoolId=40' % self.tchname
        headers = self.headers
        result = requests.get(url=url, headers=headers)
        print(result.text)
        print(url)

        self.assertEqual(result.json()['code'], 200)

    def test_11(self):  # 获取老师分组信息
        '''获取老师分组信息'''
        url = 'http://bip.slothtek.com/api/v1/group/query/mygroups?createId=27717'
        headers = self.headers
        result = requests.get(url=url, headers=headers)
        print(result.text)
        print(url)

        self.assertEqual(result.json()['code'], 200)

    def test_12(self):  # 答疑中心
        '''答疑中心'''
        url = 'http://api.slothtek.com/api/v1/issue/assign/list?issueStatus=2&pageIndex=0&pageSize=20'
        headers = self.headers
        result = requests.get(url=url, headers=headers)
        print(result.text)
        print(url)

        self.assertEqual(result.json()['code'], 200)

    def test_13(self): #成绩报告
        '''成绩报告'''
        url='http://api.slothtek.com/api/v1/mission/class/report/score?classId=543&schoolId=40&startTime=1582010407626&endTime=1582615207626'
        headers = self.headers
        result = requests.get(url=url, headers=headers)
        print(result.text)
        print(url)

        self.assertEqual(result.json()['code'], 200)

    def test_14(self): #作业提交报告
        '''老师作业提交报告'''
        url='http://api.slothtek.com/api/v1/mission/class/report/commit?classId=543&schoolId=40&startTime=1582010407626&endTime=1582615207626'
        headers = self.headers
        result = requests.get(url=url, headers=headers)
        print(result.text)
        print(url)

        self.assertEqual(result.json()['code'], 200)

    def test_15(self): #班级错题本
        '''老师班级错题本'''
        url='http://yun.slothtek.com/mission/api/v1/mission/class/error/set?teacherId=27717&schoolId=40&classId=-1&startTime=2020-02-18&endTime=2020-02-25&errorRate=-1.0&topicType=-1&pageIndex=0&pageSize=10'
        headers = self.headers
        result = requests.get(url=url, headers=headers)
        print(result.text)
        print(url)

        self.assertEqual(result.json()['code'], 200)

    def test_16(self):#作业报告列表
        '''老师作业报告列表'''
        url='http://api.slothtek.com/api/v1/mission/teacher/report/detail?missionId=7293'
        headers = self.headers
        result = requests.get(url=url, headers=headers)
        print(result.text)
        print(url)

        self.assertEqual(result.json()['code'], 200)

    def test_17(self):#作业报告详情
        '''老师作业报告详情'''
        url='http://api.slothtek.com/api/v1/mission/teacher/query/report?pageIndex=0&createId=27717&schoolId=40&pageSize=8'
        headers = self.headers
        result = requests.get(url=url, headers=headers)
        print(result.text)
        print(url)

        self.assertEqual(result.json()['code'], 200)
    def test_18(self):#空中课堂
        '''老师空中课堂'''
        url='http://api.slothtek.com/api/v1/live/push/server?teacherId=27717'
        headers = self.headers
        result = requests.get(url=url, headers=headers)
        print(result.text)
        print(url)

        self.assertEqual(result.json()['code'], 200)