#!/usr/bin/env python
# -*- coding: utf-8 -*-
# --------------------------------------------
# @Time    : 2019/3/6 21:42
# @Author  : chenbd
# @File    : post
# @Software: PyCharm Community Edition
# @license : Copyright(C), Your Company
# @Contact : 543447223@qq.com
# @Version : V1.1.0
# --------------------------------------------
# 中文显示乱码
# matplotlib.rcParams['font.sans-serif'] = ['SimHei']
# matplotlib.rcParams['font.family']='sans-serif'
# 功能     ：
#
# 算法链接：
#
# 实验结果：
## POST请求：
# post请求提交用户信息到服务器
# 执行时间：
# --------------------------------------------
import os
import requests
import base64

import time


def jpg2base64(picName):

    with open(picName, 'rb') as f:
        base64_data = base64.b64encode(f.read())
        getbase64 = base64_data.decode()
        print('%s' % type(getbase64))
        return getbase64

def write2Txt(result):
    """
    :a+ 往文件末尾追写数据，原来的数据不覆盖
    :param result:
    :return:
    """
    with open ('rice.txt', 'a+') as f:
        f.writelines(result)


def postImage(strBase64):
    """
       CGI(Common Gateway Interface)是HTTP服务器运行的程序
       通过Internet把用户请求送到服务器
       服务器接收用户请求并交给CGI程序处理
       CGI程序把处理结果传送给服务器
     """
    url = "https://xxxxxxxxxx"    # 大米识别服务器地址
    # url = "https://ce2.midea.com/food-imgreg-test/as/"    # 杂粮识别服务器地址

    # Post请求携带参数
    body = {'data':strBase64, 'SN':"1111100000", 'UserTag':""}
    # https安全校验头headers
    headers = {'content-type': "application/x-www-form-urlencoded; charset=utf-8",
               'Authorization': "Basic xxxxxxxxxxxxxxxxxxxxxxx="}

    # url服务器地址、data携带参数、https校验头
    response = requests.post(url, data=body, headers = headers)
    # 暴露请求状态
    response.raise_for_status ()
    # 请求不成功不是200，则引发HTTPError异常
    response.encoding = response.apparent_encoding
    # 返回报文信息

    return response.text


def recogImages(pathDir, destDir, dirlist):
    for folder in dirlist:
        print (folder)
        filesList = os.listdir (pathDir + "/" + folder + "/")
        destDirPathName = destDir + "/" + folder
        # 判断文件夹是否已经存在
        if not os.path.exists (destDirPathName):
            os.mkdir (destDirPathName)
        # 遍历图像文件列表
        time1 = time.time()
        for files in filesList:
            picbase64 = jpg2base64 (pathDir + "/" + folder + "/"+files)
            responseText = postImage (picbase64)
            print(files) # 图片名字
            write2Txt(files+"\n")
            write2Txt (responseText+"\n\n")
        detlatime = (time.time() - time1)

if __name__ == "__main__":

    pathDir = "sourceImages/"  ## 图像文件夹: 原数据、处理结果
    destDir = "imagesEnhance/"
    dirlist = os.listdir (pathDir)  ## 读取文件夹下的所有文件，返回list文件名列表

    recogImages(pathDir, destDir, dirlist )

