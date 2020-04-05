# -*- coding: utf-8 -*-
import time
import unittest
import HTMLTestRunner
import HTMLTestRunnerCN
from common import CommonClass
import os

def suite():
    start_dir = os.getcwd()
    print(start_dir)
    suite = unittest.defaultTestLoader.discover(start_dir=start_dir, pattern='*test.py', top_level_dir=None)
    return suite


if __name__ == '__main__':
    localtime = time.localtime(time.time())
    now = str(localtime.tm_year) + '.' + str(localtime.tm_mon) + '.' + str(localtime.tm_mday) + '.' + str(
        localtime.tm_hour) + '.' + str(localtime.tm_min)
    reportpath=os.path.join(os.getcwd(),r"report")
    reportname = os.path.join(reportpath, now + "Regression-test-report.html")
    fp = open(reportname, 'wb')
    fpp = open(reportname, 'rb').read()

    runner = HTMLTestRunnerCN.HTMLTestReportCN(
        stream=fp,
        title='{ SL_Test_Report }',
        # description='',
        description="wq"
    )
    suite = suite()
    runner.run(suite)
    fp.close()
    time.sleep(1)
    CommonClass().sendemail(reportname)

