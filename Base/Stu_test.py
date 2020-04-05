import requests
import hashlib
import re
import os
import unittest
from common import CommonClass


class BaseStuTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):

        self.admd5psw = CommonClass()._md5('slothtekadmin')  # 管理员账号密码
        self.adname = '19221'
        self.token = CommonClass().getwebtoken(self.adname, self.admd5psw)[0]
        # self.token = '6f40815cd3104daa962f9864cc42fc28'
        self.adheaders = {
            'Content-Type': 'application/json;charset=UTF-8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
            'Cookie': 'userId=%s;token=%s' % (self.adname, self.token)}

    def test_01(self):  # 新增两个学生
        '''新增两个学生'''
        url = 'http://yun.slothtek.com/base/api/out/v2/base/stu/addStus'
        headers = self.adheaders
        data = '[{"stuName":"testaddstu","gradeVal":1,"classVal":480},{"stuName":"testaddstu","gradeVal":1,"classVal":480}]'
        result = requests.session().post(url=url, headers=headers, data=data)
        print(result.text)
        print(url)

        self.assertEqual(result.json()['msg'],
                         '增加学生成功')

    def test_02(self):  # 根据班级查学生,并且判断test_01新增的学生是否存在
        '''根据班级查学生,并且判断test_01新增的学生是否存在'''
        url = 'http://yun.slothtek.com/base/api/out/v2/base/stu/getStuInfosByClassVal?classVal=480'
        headers = self.adheaders
        result = requests.session().get(url=url, headers=headers)
        globals()["stuid"] = str(result.json()['data'][-1]['studentVal']) + ',' + str(
            result.json()['data'][-2]['studentVal'])
        print(result.text)
        print(url)

        self.assertEqual(result.json()['data'][-1]['studentName'], 'testaddstu')

    def test_03(self):  # 删除新增的两个学生
        '''删除新增的两个学生'''
        url = 'http://yun.slothtek.com/base/api/out/v2/base/stu/deleteStu?studentVals=%s&reason=&classVal=480' % \
              globals()["stuid"]
        headers = self.adheaders
        result = requests.delete(url=url, headers=headers)
        print(result.text)
        print(url)
        self.assertEqual(result.json()['msg'], '删除成功')

    def test_04(self):  # 根据账号查询学生
        '''根据账号查询学生'''
        url = 'http://yun.slothtek.com/base/api/out/v2/base/stu/getStusByKeyword?keyword=19224'
        headers = self.adheaders
        result = requests.get(url=url, headers=headers)
        print(result.text)
        print(url)

        self.assertEqual(result.json()['data'][0]['stuName'], '1号小学生')

    def test_05(self):  # 根据学生名字查询学生
        '''根据学生名字查询学生'''
        url = 'http://yun.slothtek.com/base/api/out/v2/base/stu/getStusByKeyword?keyword=1%E5%8F%B7%E5%B0%8F%E5%AD%A6%E7%94%9F'
        headers = self.adheaders
        result = requests.get(url=url, headers=headers)
        print(result.text)
        print(url)

        self.assertEqual(result.json()['data'][0]['stuName'], '1号小学生')

    def test_06(self): #修改学生姓名
        '''修改学生姓名'''
        url = 'http://yun.slothtek.com/base/api/out/v2/base/stu/modifyStu'
        headers = self.adheaders
        data = '{"enterScore":"666","patMobiles":"13122224444","studentId":19302,"studentName":"qwer","studentNo":"sls79a9d3m","tagVals":[],"cityInside":"true"}'
        result = requests.put(url=url, headers=headers, data=data)
        print(result.text)
        print(url)

        self.assertEqual(result.json()['msg'], "修改成功")

    def test_07(self):  # 验证导出一个班学生excle
        '''验证导出一个班学生excle'''
        url = 'http://yun.slothtek.com/base/api/out/v2/base/stu/validExportStuInfo?gradeVal=1&classVal=480'
        headers = self.adheaders
        result = requests.get(url=url, headers=headers)
        print(result.text)
        print(url)

        self.assertEqual(result.json()['msg'], "验证通过")

    def test_08(self):  # excel导入学生
        '''excel导入学生'''
        url = 'http://yun.slothtek.com/base/api/out/v2/base/stu/importStusExcel'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
            'Cookie': 'userId=%s;token=%s' % (self.adname, self.token)}
        path = os.path.join(os.getcwd(), r"addstu.xlsx")
        files = {'file': ('addstu.xlsx', open(path, 'rb'))}  #main文件的当前目录，所以只有一个点
        data = {'Content-Disposition': 'form-data; name="file"; filename*=utf-8''addstu.xlsx',
                'Content-Type': 'application/msword',
                }
        result = requests.post(url=url, headers=headers, data=data, files=files)
        print(result.text)
        print(url)

        self.assertEqual(result.json()['msg'], "导入学生成功")
    # 还差转班，excel修改学生信息
