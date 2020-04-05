import requests
import hashlib
import re
import unittest
from common import CommonClass
import math
import os


class BaseTchTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.admd5psw = CommonClass()._md5('slothtekadmin')  # 管理员账号密码
        self.adname = '19221'
        self.token = CommonClass().getwebtoken(self.adname, self.admd5psw)[0]
        self.adheaders = {
            'Content-Type': 'application/json;charset=UTF-8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
            'Cookie': 'userId=%s;token=%s' % (self.adname, self.token)}

    def test_01(self):  # 添加老师
        '''添加老师'''
        url = 'http://yun.slothtek.com/base/api/out/v2/base/teacher/addTeachers'
        headers = self.adheaders
        data = '[{"label":"testaddtch"},{"label":"testaddtch"}]'
        result = requests.post(url=url, headers=headers, data=data)
        print(result.text)
        print(url)
        self.assertEqual(result.json()['msg'], "添加老师成功")

    def test_02(self):  # 查出整个学校老师数量
        '''查出整个学校老师数量'''
        url = 'http://yun.slothtek.com/base/api/out/v2/base/teacher/getTeachersCount?keyword='
        headers = self.adheaders
        result = requests.get(url=url, headers=headers)
        globals()["page"] = math.ceil((result.json()['data']) / 10)
        print(result.text)
        print(url)

        self.assertEqual(result.json()['code'], 200)

    def test_03(self):  # 查询整个学校老师，判断刚刚添加上没有
        '''查询整个学校老师，顺便判断刚刚添加上没有'''
        url = 'http://yun.slothtek.com/base/api/out/v2/base/teacher/getTeachers?keyword=&page=%s&pageSize=10' % \
              globals()["page"]
        headers = self.adheaders
        result = requests.get(url=url, headers=headers)
        globals()["tchid"] = str(result.json()["data"][-1]["id"]) + ',' + str(result.json()["data"][-2]["id"])
        globals()["onetchid"] = str(result.json()["data"][-1]["id"])
        print(result.text)
        print(url)

        self.assertEqual(result.json()['data'][-1]['teacherName'], "testaddtch")

    def test_04(self):  # 给刚刚添加上的老师分配班级
        '''给刚刚添加上的老师分配班级'''
        url = 'http://yun.slothtek.com/base/api/out/v2/base/teacher/allocationTeachers'
        headers = self.adheaders
        data = '[{"classVal":"480","gradeVal":"1","courseVal":"10","roleVal":"1500","teacherVal":%s}]' % globals()[
            "onetchid"]
        result = requests.post(url=url, headers=headers, data=data)
        print(result.text)
        print(url)

        self.assertEqual(result.json()['msg'], "关联 成功")

    def test_05(self):  # 根据班级-学科查出刚刚分配的老师，解除分配
        '''根据班级-学科查出刚刚分配的老师，解除分配'''
        url = 'http://yun.slothtek.com/base/api/out/v2/base/teacher/getTeacherByRole?roleVal=1500&gradeVal=1&classVal=480&courseVal=10'
        headers = self.adheaders
        result = requests.session()
        value = result.get(url=url, headers=headers).json()["data"][-1]["value"]
        url = 'http://yun.slothtek.com/base/api/out/v2/base/teacher/deleteAllote?alloteVal=%s' % value
        result = result.delete(url=url, headers=headers)
        print(result.text)
        print(url)

        self.assertEqual(result.json()['msg'], "删除成功")

    def test_06(self):  # 根据关键字查老师
        '''根据关键字查老师'''
        url = 'http://yun.slothtek.com/base/api/out/v2/base/teacher/getTeachers?keyword=test'
        headers = self.adheaders
        result = requests.get(url=url, headers=headers)
        print(result.text)
        print(url)

        self.assertEqual(result.json()['data'][-1]['teacherName'], "testaddtch")

    def test_07(self):  # 修改老师名字
        '''修改老师名字'''
        url = 'http://yun.slothtek.com/base/api/out/v2/base/teacher/updateName?teacherVal=%s&teacherName=dkaj' % \
              globals()["tchid"][0:5]
        headers = self.adheaders
        result = requests.put(url=url, headers=headers)
        print(result.text)
        print(url)

        self.assertEqual(result.json()['msg'], "更新名字成功")

    def test_08(self):  # 删除刚刚添加的两个老师
        '''删除刚刚添加的两个老师'''
        url = 'http://yun.slothtek.com/base/api/out/v2/base/teacher/delete?teacherVals=%s' % globals()["tchid"]
        headers = self.adheaders
        result = requests.delete(url=url, headers=headers)
        print(result.text)
        print(url)

        self.assertEqual(result.json()['msg'], '删除成功')

    def test_09(self):  # 下载老师名单
        '''下载老师名单'''
        url = 'http://yun.slothtek.com/base/api/out/v2/base/teacher/exportTeacherNames'
        headers = self.adheaders
        result = requests.get(url=url, headers=headers)
        print(result.headers)
        print(url)

        exlen = len(result.text)

        self.assertTrue(exlen > 40000)

    def test_10(self):  # excel导入老师
        '''excel导入老师'''
        url = 'http://yun.slothtek.com/base/api/out/v2/base/teacher/importTeacherExcel'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
            'Cookie': 'userId=%s;token=%s' % (self.adname, self.token)}
        path = os.path.join(os.getcwd(), r"addtch.xlsx")

        files = {'file': ('addtch.xlsx', open(path, 'rb'))}  # main文件的当前目录，所以只有一个点
        data = {'Content-Disposition': 'form-data; name="file"; filename*=utf-8''addtch.xlsx',
                'Content-Type': 'application/msword',
                }
        result = requests.post(url=url, headers=headers, data=data, files=files)
        print(result.text)
        print(url)

        self.assertEqual(result.json()['msg'], "导入成功")
