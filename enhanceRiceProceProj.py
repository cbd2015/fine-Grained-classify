#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018-8-10 15:44
# @Author  : chenbd
# @USER    : CHENBD
# @Site    : midea#2L4
# @File    : picProcessTest-1
# @Software: PyCharm
# @Desc     :
# @license : Copyright(C), Midea Company
# @Contact : 543447223@qq.com
import os
import cv2 as cv
import numpy as np

def rotate(image, angle, center=None, scale=1.0):
    """数据增强，图像翻转"""

    (h, w) = image.shape[:2]  ## 获取图像尺寸宽度和高度
    ## 若未指定旋转中心，则将图像中心设为旋转中心
    if center is None:
        center = (w / 2, h / 2)
    M = cv.getRotationMatrix2D (center, angle, scale)  ## 执行旋转
    rotated = cv.warpAffine (image, M, (w, h))
    ## 返回旋转后的图像
    return rotated

    # 构造参数解析器
    # ap = argparse.ArgumentParser()
    # ap.add_argument("-i", "--image", required=True, help="Path to the image")
    # args = vars(ap.parse_args())

def clahe_Photo(image):
    """局部直方图均衡化"""
    gray = cv.cvtColor (image, cv.COLOR_RGB2GRAY)
    # 指定区域的直方图均衡化    3:灰度级别      局部均衡化尺寸(5,5)
    clahe = cv.createCLAHE (4, (5, 5))
    dst = clahe.apply (gray)
    # cv.namedWindow("clahe_demo", cv.WINDOW_NORMAL)
    dst_RGB = cv.cvtColor (dst, cv.COLOR_GRAY2BGR)
    return dst_RGB

def contrast_brightness_image(src1, a, g):
    """ 对比度、亮度 """

    h, w, ch = src1.shape  # 获取shape的数值，height和width、通道
    # 新建全零图片数组src2,将height和width，类型设置为原图片的通道类型(色素全为零，输出为全黑图片)
    src2 = np.zeros ([h, w, ch], src1.dtype)
    dst = cv.addWeighted (src1, a, src2, 1 - a, g)  # addWeighted函数说明如下
    # cv.imshow ("con-bri-demo", dst)

    ##  对比度  & 亮度   ------方法1
    # enh_bri = ImageEnhance.Brightness (rice)
    # rice_brightened = enh_bri.enhance (brightness)

    return dst

def batch_Enhance(pathDir, destDir, dirlist):
    """ 批量图像数据增强处理 """
    # dirlist = os.walk(pathDir)
    count = 0
    # 光照强度系数
    brightness = 0.85

    ## 遍历文件列表
    iSolt = 0
    for folder in dirlist:
        # print(folder[0])# 头路径
        # os.listdir(folder)
        ##  分类文件夹
        print (folder)
        filesList = os.listdir (pathDir + "/" + folder + "/")
        destDirPathName = destDir + "/" + folder
        ##  判断文件夹是否已经存在
        if not os.path.exists (destDirPathName):
            os.mkdir (destDirPathName)
        # 遍历图像文件列表
        for files in filesList:
            ##  读取图像
            imageSource = cv.imread (pathDir + "/" + folder + "/" + files)
            # 每10张图像中有一张椒盐噪声
            if iSolt % 8 == 0:
                imageSource = saltpepper (imageSource, 0.0002)
            # 图像等比例缩放，增加视野中的特征数据
            Scale_image = Scale_zoon (imageSource)
            ##  转灰度图，直方图局部均衡处理
            image = clahe_Photo (Scale_image)

            for i in range (2):
                # 对每一张图像都进行处理：固定区/截取感兴趣区、旋转90  180  270
                # print(u"[0:256,%d:%d]" % (i*256,(i+1)*256))
                rice = image[0:256, 0:256]
                rice = contrast_brightness_image (rice, 1.2, 5)
                cv.imwrite (destDirPathName + "/" + files, rice)
                rotated90 = rotate (rice, 90)
                cv.imwrite (destDirPathName + "/" + "90" + str (i) + files, rotated90)
                rotated180 = rotate (rice, 180)
                cv.imwrite (destDirPathName + "/" + "180" + str (i) + files, rotated180)
                rotated270 = rotate (rice, 270)
                cv.imwrite (destDirPathName + "/" + "270" + str (i) + files, rotated270)

                # 第二行
                rice = image[0:256, 199:455]
                cv.imwrite (destDirPathName + "/" + "back" + str (i) + files, rice)
                rotated90_B = rotate (rice, 90)
                cv.imwrite (destDirPathName + "/" + "back" + str (i) + "90" + files, rotated90_B)
                rotated180_B = rotate (rice, 180)
                cv.imwrite (destDirPathName + "/" + "back" + str (i) + "180" + files, rotated180_B)
                rotated270_B = rotate (rice, 270)
                cv.imwrite (destDirPathName + "/" + "back" + str (i) + "270" + files, rotated270_B)
            iSolt += 1

def CropImage4File(filepath, destpath):
    """遍历指定目录，显示目录下的所有文件名"""

    pathDir = os.listdir (filepath)  # list all the path or file  in filepath
    for allDir in pathDir:
        child = os.path.join (filepath, allDir)
        dest = os.path.join (destpath, allDir)
        if os.path.isfile (child):
            image = cv.imread (child)
            sp = image.shape  # obtain the image shape
            sz1 = sp[0]  # height(rows) of image
            sz2 = sp[1]  # width(colums) of image
            # sz3 = sp[2]#the pixels value is made up of three primary colors, here we do not use
            a = int (sz1 / 2 - 200)  # x start
            b = int (sz1 / 2 + 200)  # x end
            c = int (sz2 / 2 - 200)  # y start
            d = int (sz2 / 2 + 200)  # y end
            cropImg = image[a:b, c:d]  # crop the image
            cv.imwrite (dest, cropImg)  # write in destination path
            cv.waitKey (0)


def Scale_zoon(image):
    """图像同比例缩放，大图到小图，特征更集中，可视化"""

    # 读取图像  原图像缩放为455*256
    # im = Image.open ("test.jpg")
    # 获取图片大小（长，宽，通道数）
    # size = im.shape

    temImg = cv.resize (image, (455, 256))
    # tempimg = cv.resize (im, (size[1]/2.8125, size[0]/2.8125), cv.INTER_LINEAR)
    # # im_resized = image.resize ((455, 256))

    return temImg


def saltpepper(img, n):
    """ @:function  椒盐随机噪声，增加系统的鲁棒性，提高识别的泛化能力
        @:parameter img is the img data
        @:parameter n is random rate product saltpepper data and insert to the img
    """
    m = int ((img.shape[0] * img.shape[1]) * n)

    for a in range (m):
        i = int (np.random.random () * img.shape[1])
        j = int (np.random.random () * img.shape[0])
        if img.ndim == 2:
            img[j, i] = 255
        elif img.ndim == 3:
            img[j, i, 0] = 255
            img[j, i, 1] = 255
            img[j, i, 2] = 255

    for b in range (m):
        i = int (np.random.random () * img.shape[1])
        j = int (np.random.random () * img.shape[0])
        if img.ndim == 2:
            img[j, i] = 0
        elif img.ndim == 3:
            img[j, i, 0] = 0
            img[j, i, 1] = 0
            img[j, i, 2] = 0

    return img


if __name__ == "__main__":
    """
        通过跟文件下的文件夹，需要有一个以上的文件夹存在
    """
    pathDir = "../RiceDataTest/helong/"  ## 图像文件夹: 原数据、处理结果
    destDir = "../RiceDataTest/phoneDest/"
    dirlist = os.listdir (pathDir)  ## 读取文件夹下的所有文件，返回list文件名列表
    batch_Enhance (pathDir, destDir, dirlist)

    # Scale_zoon()
    # img = cv.imread ('test.jpg')
    # saltImage = saltpepper (img, 0.0001)
    # cv.imshow ('saltImage', saltImage)
    # cv.waitKey (0)
    # cv.destroyAllWindows ()
