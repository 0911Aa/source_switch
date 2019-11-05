# -*- coding: utf-8 -*-
from settings import common_path as cp
import chardet

def readfile(n):
    with open(cp.copy_file_path, 'r') as f:
        lines = f.readlines()
        if n > 1:
            a_str = "".join(lines[-n:-n + 1])
            # type = chardet.detect(a_str)
            # text1 = a_str.decode(type['encoding'])
            return '%s' % a_str
        else:
            a_str = "".join(lines[-n:])
            type = chardet.detect(a_str)
            text2 = a_str.decode(type['encoding'])
            return '%s' % text2

print(type(readfile(2)))