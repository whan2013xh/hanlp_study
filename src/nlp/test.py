# -*- coding: utf-8 -*-
"""
    CreatedDate: 2021-07-22
    FileName   : test.py
    Author     : Honghe
    Descreption: 
"""
from pyhanlp import JClass
char = '入门自然语言'
for str in char:
    code = JClass('java.lang.Character')(str).hashCode()
    print(f"{str} : {code}")


# import jpype
# print(jpype.__version__)
#
# if __name__=="__main__":
#     # 获取系统的jvm路径
#     jvm_path = jpype.getDefaultJVMPath()
#     print(jvm_path)
#     # 设置jvm路径，以启动java虚拟机
#     jpype.startJVM(jvm_path,convertStrings=False)
#     # 执行java代码
#     jpype.java.lang.System.out.println('hello world')
#     # 关闭jvm虚拟机，当使用完 JVM 后，可以通过 jpype.shutdownJVM() 来关闭 JVM，该函数没有输入参数。当 python 程序退出时，JVM 会自动关闭。
#     jpype.shutdownJVM()