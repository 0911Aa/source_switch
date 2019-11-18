# -*- coding: utf-8 -*-

import pytest,time,allure,os,subprocess
from sources.get_driver import DriverClient
from logs import logging_save
from sources.read_config import ReadIni
import chardet
from settings import common_path as cp
from config import test_times

read_ini = ReadIni()

def setup_module(module):
    print("开始测试")

def teardown_module(module):
    print("测试结束")


@pytest.mark.P1
@pytest.mark.run(order=1)
@allure.feature('source切换测试')
@pytest.mark.repeat(test_times)
class Test_G6SA_source_switch:

    def setup_class(cls):
        print('设置初始化')
        cls.Action = DriverClient().Action
        for i in range(20):
            cls.Action.valueup()

    def teardown(self):
        print("this case finishd")
        time.sleep(2)

    def BT_switch(self):
        self.Action.home()
        time.sleep(2)
        os.system('adb -s 0000 shell input tap 404 648')
        logging_save.logging.info('正在切换到BT source...')
        self.Action.find_element('music_hall',"音乐栏").click()
        self.Action.find_element('BT',"蓝牙按钮").click()

    def USB_audio_switch(self):
        self.Action.home()
        time.sleep(2)
        os.system('adb -s 0000 shell input tap 404 648')
        logging_save.logging.info('正在切换到USB audio source...')
        self.Action.find_element('music_hall', "音乐栏").click()
        self.Action.find_element('USB_audio', "USB音乐按钮").click()

    def USB_vedio_switch(self):
        logging_save.logging.info('正在切换到USB vedio source...')
        self.Action.find_element('vedio_hall', "视频栏").click()
        self.Action.find_element('USB_vedio', "音乐栏").click()

    def FM_switch(self):
        logging_save.logging.info('正在切换到FM source...')
        os.system('adb -s 0000 shell input tap 235 654')

    def track_check(self,play_status, play_times):
        creat_filename = open(cp.python_side_path, 'w')
        creat_filename.write(play_status)
        creat_filename.write(play_times)
        creat_filename.flush()
        time.sleep(3)
        creat_filename.close()
        p = subprocess.Popen(cp.exe_path)
        p.wait()

    def clearBlankLine(self):
        file1 = open(cp.labview_result_path, 'r')  # 要去掉空行的文件
        with open(cp.copy_file_path, 'w') as file2:  # 生成没有空行的文件
            try:
                for line in file1.readlines():
                    if line == '\n':
                        line = line.strip("\n")
                    file2.write(line)
            finally:
                file1.close()

    def readfile(self,n):
        with open(cp.copy_file_path, 'r') as f:
            lines = f.readlines()
            if n > 1:
                a_str = "".join(lines[-n:-n + 1])
                # type = chardet.detect(a_str)
                # text1 = a_str.decode(type['encoding'])
                return '%s' % a_str
            else:
                a_str = "".join(lines[-n:])
                # type = chardet.detect(a_str)
                # text2 = a_str.decode(type['encoding'])
                return '%s' % a_str

    def test_case1(self):
        # BT--->USB_audio--->USB_vedio--->FM
        self.BT_switch()
        logging_save.logging.info('检查车机输出...')
        self.track_check('BT ', '7')
        self.clearBlankLine()
        if 'OK' in self.readfile(2):
            pass
        else:
            logging_save.logging.info(self.readfile(1))
            print("case fail...")
            raise Exception("蓝牙声音输出异常")
        # self.Action.find_element('USB_vedio', "音乐栏").click()
        self.Action.find_element("BT_next","蓝牙下一曲").click()
        logging_save.logging.info('检查车机输出...')
        self.track_check('BT ', '10')
        self.clearBlankLine()
        if 'OK' in self.readfile(2):
            pass
        else:
            logging_save.logging.info(self.readfile(1))
            print("case fail...")
            raise Exception("切换下一曲后，蓝牙声音输出异常")


        self.USB_audio_switch()
        logging_save.logging.info('检查车机输出...')
        self.track_check('USB_AUDIO ', '11')
        self.clearBlankLine()
        if 'OK' in self.readfile(2):
            pass
        else:
            logging_save.logging.info(self.readfile(1))
            print("case fail...")
            raise Exception("USB音乐声音输出异常")
        logging_save.logging.info('检查车机输出...')
        self.Action.find_element("USB_next", "USB下一曲").click()
        self.track_check('USB_AUDIO ', '20')
        self.clearBlankLine()
        if 'OK' in self.readfile(2):
            pass
        else:
            logging_save.logging.info(self.readfile(1))
            print("case fail...")
            raise Exception("切换下一曲后，USB音乐声音输出异常")

        self.USB_vedio_switch()
        logging_save.logging.info('检查车机输出...')
        self.track_check('USB_VEDIO ', '15')
        self.clearBlankLine()
        if 'OK' in self.readfile(2):
            pass
        else:
            logging_save.logging.info(self.readfile(1))
            print("case fail...")
            raise Exception("USB视频声音输出异常")
        logging_save.logging.info('检查车机输出...')
        self.Action.find_element("vedio_name_2", "第二个视频").click()
        self.track_check('USB_VEDIO ', '23')
        self.clearBlankLine()
        if 'OK' in self.readfile(2):
            pass
        else:
            logging_save.logging.info(self.readfile(1))
            print("case fail...")
            raise Exception("切换曲目后，USB视频声音输出异常")
        logging_save.logging.info('检查车机输出...')
        self.Action.find_element("vedio_name_1", "第一个视频").click()
        self.track_check('USB_VEDIO ', '23')
        self.clearBlankLine()
        if 'OK' in self.readfile(2):
            pass
        else:
            logging_save.logging.info(self.readfile(1))
            print("case fail...")
            raise Exception("切换曲目后，USB视频声音输出异常")
        # os.system('adb -s 0000 shell input tap 77 153')
        # self.driver.tap([(77, 153)], 1)
        # time.sleep(2)

        self.FM_switch()
        logging_save.logging.info('检查车机输出...')
        self.track_check('FM ', '8')
        self.clearBlankLine()
        if 'OK' in self.readfile(2):
            pass
        else:
            logging_save.logging.info(self.readfile(1))
            # raise Exception("声音输出异常")

    def test_case2(self):
    # USB_audio--->BT--->USB_vedio--->FM
        self.USB_audio_switch()
        logging_save.logging.info('检查车机输出...')
        self.track_check('USB_AUDIO ', '13')
        self.clearBlankLine()
        if 'OK' in self.readfile(2):
            pass
        else:
            logging_save.logging.info(self.readfile(1))
            print("case fail...")
            raise Exception("USB音乐声音输出异常")
        self.Action.find_element("USB_next", "USB下一曲").click()
        logging_save.logging.info('检查车机输出...')
        self.track_check('USB_AUDIO ', '20')
        self.clearBlankLine()
        if 'OK' in self.readfile(2):
            pass
        else:
            logging_save.logging.info(self.readfile(1))
            print("case fail...")
            raise Exception("切换下一曲后，USB音乐声音输出异常")

        self.BT_switch()
        logging_save.logging.info('检查车机输出...')
        self.track_check('BT ', '11')
        self.clearBlankLine()
        if 'OK' in self.readfile(2):
            pass
        else:
            logging_save.logging.info(self.readfile(1))
            print("case fail...")
            raise Exception("蓝牙声音输出异常")
        self.Action.find_element("BT_next","蓝牙下一曲").click()
        logging_save.logging.info('检查车机输出...')
        self.track_check('BT ', '10')
        self.clearBlankLine()
        if 'OK' in self.readfile(2):
            pass
        else:
            logging_save.logging.info(self.readfile(1))
            print("case fail...")
            raise Exception("切换下一曲后，蓝牙声音输出异常")

        self.USB_vedio_switch()
        logging_save.logging.info('检查车机输出...')
        self.track_check('USB_VEDIO ', '15')
        self.clearBlankLine()
        if 'OK' in self.readfile(2):
            pass
        else:
            logging_save.logging.info(self.readfile(1))
            print("case fail...")
            raise Exception("USB视频声音输出异常")
        self.Action.find_element("vedio_name_2", "第二个视频").click()
        logging_save.logging.info('检查车机输出...')
        self.track_check('USB_VEDIO ', '23')
        self.clearBlankLine()
        if 'OK' in self.readfile(2):
            pass
        else:
            logging_save.logging.info(self.readfile(1))
            print("case fail...")
            raise Exception("切换曲目后，USB视频声音输出异常")
        self.Action.find_element("vedio_name_1", "第一个视频").click()
        logging_save.logging.info('检查车机输出...')
        self.track_check('USB_VEDIO ', '23')
        self.clearBlankLine()
        if 'OK' in self.readfile(2):
            pass
        else:
            logging_save.logging.info(self.readfile(1))
            print("case fail...")
            raise Exception("切换曲目后，USB视频声音输出异常")
        # os.system('adb -s 0000 shell input tap 77 153')
        # # self.driver.tap([(77, 153)], 1)
        # time.sleep(2)

        self.FM_switch()
        logging_save.logging.info('检查车机输出...')
        self.track_check('FM ', '8')
        self.clearBlankLine()
        if 'OK' in self.readfile(2):
            pass
        else:
            logging_save.logging.info(self.readfile(1))
            # raise Exception("声音输出异常")

    def test_case3(self):
    #USB_audio--->FM--->BT--->USB_video
        self.USB_audio_switch()
        logging_save.logging.info('检查车机输出...')
        self.track_check('USB_AUDIO ', '13')
        self.clearBlankLine()
        if 'OK' in self.readfile(2):
            pass
        else:
            logging_save.logging.info(self.readfile(1))
            print("case fail...")
            raise Exception("USB音乐声音输出异常")
        self.Action.find_element("USB_next", "USB下一曲").click()
        logging_save.logging.info('检查车机输出...')
        self.track_check('USB_AUDIO ', '20')
        self.clearBlankLine()
        if 'OK' in self.readfile(2):
            pass
        else:
            logging_save.logging.info(self.readfile(1))
            print("case fail...")
            raise Exception("切换下一曲后，USB音乐声音输出异常")

        self.FM_switch()
        logging_save.logging.info('检查车机输出...')
        self.track_check('FM ', '8')
        self.clearBlankLine()
        if 'OK' in self.readfile(2):
            pass
        else:
            logging_save.logging.info(self.readfile(1))
            # raise Exception("声音输出异常")

        self.BT_switch()
        logging_save.logging.info('检查车机输出...')
        self.track_check('BT ', '11')
        self.clearBlankLine()
        if 'OK' in self.readfile(2):
            pass
        else:
            logging_save.logging.info(self.readfile(1))
            print("case fail...")
            raise Exception("蓝牙声音输出异常")
        self.Action.find_element("BT_next","蓝牙下一曲").click()
        logging_save.logging.info('检查车机输出...')
        self.track_check('BT ', '10')
        self.clearBlankLine()
        if 'OK' in self.readfile(2):
            pass
        else:
            logging_save.logging.info(self.readfile(1))
            print("case fail...")
            raise Exception("切换下一曲后，蓝牙声音输出异常")

        self.USB_vedio_switch()
        logging_save.logging.info('检查车机输出...')
        self.track_check('USB_VEDIO ', '15')
        self.clearBlankLine()
        if 'OK' in self.readfile(2):
            pass
        else:
            logging_save.logging.info(self.readfile(1))
            print("case fail...")
            raise Exception("USB视频声音输出异常")
        self.Action.find_element("vedio_name_2", "第二个视频").click()
        logging_save.logging.info('检查车机输出...')
        self.track_check('USB_VEDIO ', '23')
        self.clearBlankLine()
        if 'OK' in self.readfile(2):
            pass
        else:
            logging_save.logging.info(self.readfile(1))
            print("case fail...")
            raise Exception("切换曲目后，USB视频声音输出异常")
        self.Action.find_element("vedio_name_1", "第一个视频").click()
        logging_save.logging.info('检查车机输出...')
        self.track_check('USB_VEDIO ', '23')
        self.clearBlankLine()
        if 'OK' in self.readfile(2):
            pass
        else:
            logging_save.logging.info(self.readfile(1))
            print("case fail...")
            raise Exception("切换曲目后，USB视频声音输出异常")
        # os.system('adb -s 0000 shell input tap 77 153')
        # # self.driver.tap([(77, 153)], 1)
        # time.sleep(2)