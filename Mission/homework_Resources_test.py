import requests
import re
import unittest
from common import CommonClass
import math
import os
import time


class HomeworkResources(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.tchmd5psw = CommonClass()._md5('123456')  #
        self.tchname = '27717'
        self.tchtoken = CommonClass().getpadtoken(self.tchname, self.tchmd5psw)
        self.stumd5psw = CommonClass()._md5('111111')
        self.stuname = '27819'
        # self.token = '6cb42a26500049bc98d28689d5fc0137'
        self.stutoken = CommonClass().getpadtoken(self.stuname, self.stumd5psw)
        self.stuheaders = {
            'token': self.stutoken,
            'userid': self.stuname,
            'Content-Type': 'application/json;charset=UTF-8',
            'User-Agent': 'okhttp/3.6.0'}
        self.tchheaders = {
            'token': self.tchtoken,
            'userid': self.tchname,
            'Content-Type': 'application/json;charset=UTF-8',
            'User-Agent': 'okhttp/3.6.0'}

    def test_01(self):  # 获取上传文件token
        '''获取上传文件token'''
        url = "http://api.slothtek.com/api/v1/file/uptoken?filename=Screenshot_20200225_212851_com.tencent.mm.jpg"
        headers = {
            'User-Agent': 'okhttp/3.2.0'
        }
        result = requests.get(url, headers=headers)
        globals()["fileKey"] = result.json()['data']['fileKey']
        globals()["filetoken"] = result.json()['data']['token']
        print(url)
        print(result.text)
        self.assertEqual(result.json()['code'], 200)

    def test_02(self):  # 上传文件到七牛
        '''上传文件到七牛'''
        url = "http://upload.qiniu.com/"
        path = os.path.join(os.getcwd(), r"timg.jpg")
        headers = {
            'User-Agent': 'QiniuAndroid/7.3.3 (9; HUAWEI-PCT-AL10; 1582685243370634; dawobP8ofeZsgaUR)'
        }
        data = {'key': globals()["fileKey"],
                'token': globals()['filetoken'],
                'Content-Type': 'application/octet-stream',
                'Content-Disposition': 'form-data; name="file"; filename="Screenshot_20200225_212851_com.tencent.mm.jpg"'}
        files = [
            ('file', open(path, 'rb'))
        ]
        result = requests.post(url=url, headers=headers, data=data, files=files)
        print(url)
        print(result.text)
        self.assertEqual(result.json()['key'], globals()["fileKey"])

    def test_03(self):  # 用刚刚的图片布置作业
        '''用刚刚的图片布置作业'''
        url = 'http://api.slothtek.com/api/v1/mission/teacher/publish'
        headers = self.tchheaders
        data = '{"acceptor":[{"acceptId":556,"acceptName":"3班","acceptType":1}],"mission":{"accepters":[],"answer":[],"answerTime":"2020-12-26 15:02","createId":0,"finishTime":"2020-12-26 15:02","fromSubjectId":0,"fromType":1,"id":0,"materials":[{"duration":0,"type":6,"url":"http://file.slothtek.com/%s","useType":0,"uuid":"c02a6cf5ad864c82bb6209b97bd2fad4"}],"microVideo":[],"missionStatus":0,"parts":[{"correctType":1,"id":0,"imgs":[],"itemDefaultScore":2.0,"items":[{"answer":[],"difficultId":0,"fromType":0,"id":0,"imgs":[],"kpis":[],"optionNumber":4,"options":["A","B","C","D"],"score":2.0,"selectOption":["A"],"subItems":[],"topicType":0}],"materials":[],"optionNumber":4,"partName":"单选题","score":2.0,"takeImgType":1,"type":1},{"correctType":1,"id":0,"imgs":[],"itemDefaultScore":10.0,"items":[{"answer":[],"difficultId":0,"fromType":0,"id":0,"imgs":[],"kpis":[],"optionNumber":4,"score":10.0,"selectOption":[],"subItems":[],"topicType":0}],"materials":[],"optionNumber":4,"partName":"简答题","score":10.0,"takeImgType":1,"type":5}],"remark":"","schoolId":40,"score":12.0,"sectionType":0,"sendTime":"2020-02-26 14:32","sendType":2,"title":"testhomework"}}' % \
               globals()["fileKey"]
        result = requests.post(url=url, headers=headers, data=data.encode())
        globals()['missionid'] = result.json()['data']
        print(result.text)
        print(url)
        self.assertEqual(result.json()['code'], 200)

    def test_04(self):  # 查看布置作业记录
        '''查看布置作业记录'''
        url = 'http://api.slothtek.com/api/v1/mission/teacher/query?teacherId=27717&pageIndex=0&schoolId=40&pageSize=5&status=2'
        headers = self.tchheaders
        result = requests.get(url=url, headers=headers)
        print(result.text)
        print(url)
        self.assertEqual(result.json()['code'], 200)

    def test_05(self):  # 查看刚刚布置的作业详情
        '''查看刚刚布置的作业详情'''
        url = 'http://api.slothtek.com/api/v1/mission/common/detail?missionId=%s' % globals()['missionid']
        headers = self.tchheaders
        result = requests.get(url=url, headers=headers)
        print(result.text)
        print(url)
        self.assertEqual(result.json()['code'], 200)

    def test_06(self):  # 检查题库
        '''检查题库是否正常返回'''
        url = 'http://yun.slothtek.com/mission/api/v1/core/question/by/kpi?stageId=3&subjectId=1&pressId=1&kpiStr=6631&questionType=-1&difficult=-1&clearData=true&pageIndex=1&pageSize=10'
        headers = self.tchheaders
        result = requests.get(url=url, headers=headers)
        print(result.text)
        print(url)
        self.assertEqual(result.json()['code'], 200)

    def test_07(self):  # 我的资源
        '''老师点击我的资源'''
        url = 'http://api.slothtek.com/api/v1/resource/teacher/query?preview=false&suffixs=-1&pageIndex=0&pageSize=10'
        headers = self.tchheaders
        result = requests.get(url=url, headers=headers)
        print(result.text)
        print(url)
        self.assertEqual(result.json()['code'], 200)

    def test_08(self):  # 发送动态
        '''老师查看资源发送动态'''
        url = 'http://api.slothtek.com/api/v1/resource/teacher/query/share?pageIndex=0&pageSize=10'
        headers = self.tchheaders
        result = requests.get(url=url, headers=headers)
        print(result.text)
        print(url)
        self.assertEqual(result.json()['code'], 200)

    def test_09(self):  # 我的微课
        '''老师点击我的微课'''
        url = 'http://api.slothtek.com/api/v1/resource/teacher/query?preview=false&suffixs=-1&pageIndex=0&resTypes=5&pageSize=20'
        headers = self.tchheaders
        result = requests.get(url=url, headers=headers)
        print(result.text)
        print(url)
        self.assertEqual(result.json()['code'], 200)

    def test_10(self):  # 微课发送动态
        '''老师查看微课发送动态'''
        url = 'http://api.slothtek.com/api/v1/resource/teacher/query/share?pageIndex=0&resTypes=5&pageSize=20'
        headers = self.tchheaders
        result = requests.get(url=url, headers=headers)
        print(result.text)
        print(url)
        self.assertEqual(result.json()['code'], 200)

    def test_11(self):  # 校本资源
        '''老师点击校本资源'''
        url = 'http://api.slothtek.com/api/v1/resource/school/query?pageIndex=0&schoolId=40&resTypes=5&pageSize=10&fileTypes=.mp4,.flv&stageId=3'
        headers = self.tchheaders
        result = requests.get(url=url, headers=headers)
        print(result.text)
        print(url)
        self.assertEqual(result.json()['code'], 200)

    def test_12(self):  # 学生查看刚刚布置的作业
        '''学生查看刚刚布置的作业'''
        url = 'http://api.slothtek.com/api/v1/mission/common/detail?missionId=%s' % globals()['missionid']
        headers = self.stuheaders
        result = requests.get(url=url, headers=headers)
        globals()['itemid1'] = result.json()['data']['parts'][0]['items'][0]['id']
        globals()['itemid2'] = result.json()['data']['parts'][1]['items'][0]['id']
        globals()['partsid1'] = result.json()['data']['parts'][0]['id']
        globals()['partsid2'] = result.json()['data']['parts'][1]['id']
        print(result.text)
        print(url)
        self.assertEqual(result.json()['code'], 200)

    def test_13(self):  # 学生提交刚刚布置作业
        '''学生提交刚刚布置作业'''
        url = 'http://api.slothtek.com/api/v1/mission/student/commit'
        data = '{"answer":[{"answer":["A"],"id":%s,"takeImgType":1,"topicType":1},{"id":%s,"imgs":["http://file.slothtek.com/72987e1606c245059d0a4dd9da29f9d9.jpg"],"takeImgType":1,"topicType":5}],"missionId":%s}' % (
            globals()['itemid1'], globals()['itemid2'], globals()['missionid'])
        headers = self.stuheaders
        result = requests.post(url=url, data=data, headers=headers)
        print(result.text)
        print(url)
        self.assertEqual(result.json()['data'], '答案提交成功')

    def test_14(self):  # 老师获取刚刚提交的作业
        '''老师获取test13学生提交的作业'''
        url = 'http://api.slothtek.com/api/v1/mission/teacher/query/correct/wait/student?allStudent=false&missionId=%s&commitId=%s' % (
            globals()['missionid'], self.stuname)
        headers = self.tchheaders
        result = requests.get(url=url, headers=headers)
        print(result.text)
        print(url)
        self.assertEqual(result.json()['code'], 200)

    def test_15(self):  # 批改列表
        '''上个用例布置作业的批改列表'''
        url = 'http://api.slothtek.com/api/v1/mission/teacher/query/correct/list?missionId=%s&status=1' % globals()[
            'missionid']
        headers = self.tchheaders
        result = requests.get(url=url, headers=headers)
        print(result.text)
        print(url)
        self.assertEqual(result.json()['code'], 200)

    def test_16(self):  # 批改学生作业
        '''批改学生作业并提交'''
        url = 'http://api.slothtek.com/api/v1/mission/teacher/correct'
        headers = self.tchheaders
        data = '{"answerId":%s,"missionId":%s,"parts":[{"correctImgs":[],"correctScore":10.0,"correctType":1,"id":%s,"items":[{"correctImgs":["http://file.slothtek.com/3027eb9af4234d4990d260d9bf965051.jpg"],"correctScore":10.0,"correctStatus":0,"itemId":%s,"score":10.0}],"takeImgType":1,"topicType":5}],"reviewIds":[]}' % (
            self.stuname, globals()['missionid'], globals()['partsid2'], globals()['itemid2'])
        result = requests.post(url=url, data=data, headers=headers)
        print(result.text)
        print(url)
        self.assertEqual(result.json()['data'], '作业批改成功')

    def test_17(self):  # 老师查看刚刚批改的情况，并验证总分
        '''老师查看刚刚批改的情况，并验证总分'''
        url = 'http://api.slothtek.com/api/v1/mission/teacher/correct/detail?missionId=%s&commitId=%s' % (
        globals()['missionid'], self.stuname)
        headers = self.tchheaders
        result = requests.get(url=url, headers=headers)
        print(result.text)
        print(url)
        self.assertEqual(result.json()['data']['correctScore'], 12)

    def test_18(self):  # 学生查看批改情况
        '''学生查看上调用例的批改情况'''
        url = 'http://api.slothtek.com/api/v1/mission/student/answer/detail2?commitId=%s&missionId=%s' % (
        self.stuname, globals()['missionid'])
        headers = self.stuheaders
        result = requests.get(url=url, headers=headers)
        print(result.text)
        print(url)
        self.assertEqual(result.json()['code'], 200)

    def test_19(self):  # 作业分析列表
        '''作业分析列表'''
        url = 'http://api.slothtek.com/api/v1/mission/teacher/query/report?pageIndex=0&createId=27717&schoolId=40&pageSize=8'
        headers = self.tchheaders
        result = requests.get(url=url, headers=headers)
        print(result.text)
        print(url)
        self.assertEqual(result.json()['code'], 200)

    def test_20(self):  # 作业分析详情,验证刚刚改的分数
        '''作业分析详情,验证上条用例批改的最高分在报告中是否正常'''
        url = 'http://api.slothtek.com/api/v1/mission/teacher/report/detail?missionId=%s' % globals()['missionid']
        headers = self.tchheaders
        result = requests.get(url=url, headers=headers)
        print(result.text)
        print(url)
        self.assertEqual(result.json()['data']['highestScore'], 12)

    def test_21(self):  # 小题答题详情报告
        '''小题答题详情报告'''
        url = 'http://api.slothtek.com/api/v1/mission/teacher/analyze/item?itemId=%s&itemType=1&missionId=%s&loadExtra=true' % (
        globals()['itemid1'], globals()['missionid'])
        headers = self.tchheaders
        result = requests.get(url=url, headers=headers)
        print(result.text)
        print(url)
        self.assertEqual(result.json()['code'], 200)

    def test_22(self):  # 错题
        '''teacher/error'''
        url = 'http://api.slothtek.com/api/v1/mission/teacher/error?missionId=7662'
        headers = self.tchheaders
        result = requests.get(url=url, headers=headers)
        print(result.text)
        print(url)
        self.assertEqual(result.json()['code'], 200)
<<<<<<< HEAD
=======

    def test_23(self):
        '''网盘资源分享图片到班和校本'''
        url='http://api.slothtek.com/api/v1/resource/share'
        headers = self.tchheaders
        data='{"acceptor":[{"acceptId":27819,"acceptName":"sssssx","acceptType":4},{"acceptId":27923,"acceptName":"wqqqa","acceptType":4},{"acceptId":40,"acceptType":8}],"resId":"49130"}'
        result = requests.post(url=url, data=data, headers=headers)
        print(result.text)
        print(url)
        self.assertEqual(result.json()['code'], 200)

    def test_24(self):
        '''查看原题'''
        url='http://api.slothtek.com/api/v1/mission/common/detail?missionId=%s'%globals()['missionid']
        headers = self.tchheaders
        result = requests.get(url=url,headers=headers)
        print(result.text)
        print(url)
        self.assertEqual(result.json()['code'], 200)

    def test_25(self):
        '''上传资源到我的资源'''
        url='http://api.slothtek.com/api/v1/resource/upload'
        headers=self.tchheaders
        data='{"acceptor":[{"acceptId":40,"acceptType":8}],"bookId":-1,"fileUUID":"c_5e4d08cdc545445fa49bdee1f8847112","kpis":[],"name":"微课_2020-02-21_21-06-32","nodes":[],"relevant":[],"schoolId":40,"stageId":3,"subjectId":70,"type":11,"versionId":457}'
        result = requests.post(url=url, data=data.encode(), headers=headers)
        print(result.text)
        print(url)
        self.assertEqual(result.json()['code'], 200)
>>>>>>> 1c3ea27b412717663ffc9266c868b15e4311daa3
