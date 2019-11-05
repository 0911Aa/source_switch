#coding:UTF-8
'''
@author: uidq1501
'''
import time
import logging
from settings import common_path

path =common_path.log_path

now = time.strftime('%Y-%m-%M-%H_%S',time.localtime(time.time()))
logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s %(levelname)s %(message)s',
                datefmt='%y%m%d_%H:%M:%S',
                filename= path+'\\test_log.txt',
                filemode='w')

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)