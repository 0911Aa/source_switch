# -*- coding: utf-8 -*-
"""
@ Description：Appium api 封装层
"""

import time
import allure
from appium import webdriver
# from appium.webdriver.common.touch_action import TouchAction
# from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import os
from settings import common_path
from sources.read_config import ReadIni

from logs.log import Log as L

read_ini = ReadIni()
def Ldict(element, type, name=None, text=None, time=5, index=0):
    """
    :param element: 查找元素的名称 例如：xxx:id/xx
    :param type: 元素类型 id,xpath,class name,accessibility id
    :param name: 测试步骤的名称
    :param : 需要输入文本的名称
    :param time: 查找该元素需要的时间，默认 5s
    :param index: 不为空则查找元素数组下标
    :return:
    """
    return {'element': element, 'type': type, 'name': name, 'text': text, 'time': time, 'index': index}


class NotFoundElementError(Exception):
    pass


class NotFoundTextError(Exception):
    pass


class ElementActions:
    def __init__(self, driver: webdriver.Remote, adb=None, Parameterdict=None):
        self.Parameterdict = Parameterdict
        self.driver = driver
        self.ADB = adb
        if Parameterdict:
            self.width = self.driver.get_window_size()['width']
            self.height = self.driver.get_window_size()['height']
            self.apppid = self.get_app_pid()

    def click(self, element, logtext):
        print("点击元素:%s" % (logtext))
        ele = read_ini.get_value(str(element))
        if ele.startswith("//"):
            self.driver.find_element_by_xpath(ele).click()
        else:
            self.driver.find_element_by_id(ele).click()

    def find_element(self,element,name):
        ele = read_ini.get_value(str(element))
        with allure.step("检查：'{0}'".format(name)):
                try:
                    if ele.startswith('//'):
                        return WebDriverWait(self.driver, 10).until(lambda driver: driver.find_element_by_xpath(ele), '失败了')
                    else:
                        return WebDriverWait(self.driver, 10).until(lambda driver: driver.find_element_by_id(ele),'失败')

                except Exception as e:
                    print(e)
                    L.e("页面中未能找到 %s 元素" % name)
                    raise Exception("页面中未能找到 [%s]" % name)


    def adb_shell(self, command, args, includeStderr=False):
        """
        appium --relaxed-security 方式启动
        adb_shell('ps',['|','grep','android'])

        :param command:命令
        :param args:参数
        :param includeStderr: 为 True 则抛异常
        :return:
        """
        result = self.driver.execute_script('mobile: shell', {
            'command': command,
            'args': args,
            'includeStderr': includeStderr,
            'timeout': 5000
            })
        return result['stdout']

    def get_app_pid(self):
        """ 获取包名PID 进程
        :return: int PID
        """
        result = self.ADB.shell('"ps | grep {0}"'.format(self.Parameterdict.get('appPackage')))

        # result = self.adb_shell('ps', ['|', 'grep', self.Parameterdict.get('appPackage')])
        if result:
            return result.split()[1]
        else:
            return False


    def clear(self):
        self.driver.quit()

    @staticmethod
    def sleep(s):
        if isinstance(s, dict):
            s = s['element']
        return time.sleep(s)


    def home(self):
        self.driver.keyevent(3)

    def valueup(self):
        self.driver.keyevent(24)

    def swipe_up(self,t=500):
        x1 = self.width * 0.8  # x坐标
        y1 = self.height * 0.65  # 起点y坐标
        y2 = self.height * 0.35  # 终点y坐标
        self.driver.swipe(x1, y1, x1, y2, t)

    # 向下滑动
    def swipe_down(self,t=500, n=1):
        x1 = self.width * 0.5  # x坐标
        y1 = self.height * 0.25  # 起点y坐标
        y2 = self.height * 0.75  # 终点y坐标
        for i in range(n):
            self.driver.swipe(x1, y1, x1, y2, t)

    def find_element_by_image(self, Tpl, value=0.85, swipe=False):
        """
        根据图片查找
        :param Tpl: 要查找的图片
        :param value: 相似度
        :param swipe: 是否要滑动查找
        :return:
        """
        import cv2 as cv
        import uuid

        # 导入屏幕截屏
        i = 0
        error_list = []
        while i < 5:
            try:
                i += 1
                target_path = str(uuid.uuid4()) + '.png'
                print("获得图片",target_path)
                self.driver.get_screenshot_as_file(target_path)
                target = cv.imread(target_path)
                # 导入匹配的图标
                Tpl_path = common_path.icons_path+str(Tpl)
                print("********",Tpl_path)
                tpl = cv.imread(Tpl_path)
                # 获取图标大小
                th, tw = tpl.shape[:2]
                # 匹配函数
                result = cv.matchTemplate(target, tpl, cv.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
                tl = max_loc  # 是矩形右下角的点的坐标
                print("相似度",max_val)
                cv.rectangle(target, tl, (tl[0] + tw, tl[1] + th), (7, 249, 151), 2)
                if max_val <= value:
                    raise TypeError("没有图标")
                point = [int(tl[0] + tw / 2), int(tl[1] + th / 2)]  # 是中间点的坐标
                print("point",point)
                cmd = "adb shell input tap " + str(str(point[0]) + " " + str(point[1]))
                # print("cmd",cmd)
                os.system(cmd)
                os.system("del /F /S /Q " + target_path)
                break

            except TypeError as e:
                print(e)
                error_list.append(e)
                os.system("del /F /S /Q " + target_path)
                if swipe:
                    self.swipe_up()
                    time.sleep(1)
                print(error_list,len(error_list))
                if len(error_list)>=5:
                    raise Exception("页面中没有对应图标%s"%Tpl)

    def find_elements_by_image(self, Tpls, value=0.85, swipe=False):
        """
        根据图片查找
        :param Tpl: 要查找的图片
        :param value: 相似度
        :param swipe: 是否要滑动查找
        :return:
        """
        import cv2 as cv
        import uuid

        # 导入屏幕截屏
        flag = False
        i = 0
        while i < 5:
            try:
                i += 1
                target_path = str(uuid.uuid4()) + '.png'
                print("获得图片", target_path)
                self.driver.get_screenshot_as_file(target_path)
                target = cv.imread(target_path)
                # 导入匹配的图标
                for Tpl in Tpls:
                    Tpl_path = common_path.icons_path + str(read_ini.get_value(Tpl))
                    print("********", Tpl_path)
                    tpl = cv.imread(Tpl_path)
                    # 获取图标大小
                    th, tw = tpl.shape[:2]
                    # 匹配函数
                    result = cv.matchTemplate(target, tpl, cv.TM_CCOEFF_NORMED)
                    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
                    tl = max_loc  # 是矩形右下角的点的坐标
                    print("相似度", max_val)
                    cv.rectangle(target, tl, (tl[0] + tw, tl[1] + th), (7, 249, 151), 2)
                    if max_val <= value:
                        continue
                        # raise TypeError("没有图标")
                    else:
                        flag = True
                        break
                if flag:

                    point = [int(tl[0] + tw / 2), int(tl[1] + th / 2)]  # 是中间点的坐标
                    print("point", point)
                    cmd = "adb shell input tap " + str(str(point[0]) + " " + str(point[1]))
                    # print("cmd",cmd)
                    os.system(cmd)
                    os.system("del /F /S /Q " + target_path)
                    break
                else:
                    raise TypeError("没有图标")
            except TypeError as e:
                print(e)
                os.system("del /F /S /Q " + target_path)
                if swipe:
                    self.swipe_up()
                    time.sleep(1)

        if not flag:
            raise Exception("页面中没有对应图标%s" % Tpl)


