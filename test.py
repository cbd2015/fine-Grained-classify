# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
# @Time     : 2019-4-17 19:47
# @USER     : chenbd
# @Site     : midea#2L4
# @File     : test
# @Software : PyCharm
# @license  : Copyright(C), Midea Company
# @Author   : chenbd
# @Email    : 543447223@qq.com
# @Version  : V1.1.0
------------------------------------------------- 
# @Attantion：
#    1、
#    2、
#    3、
# @Tag      : 
#
# @Referne  :
#    1、
#    2、
-------------------------------------------------
"""
import numpy as np
import pylab as pl
import scipy.spatial.distance as dist
def plotSamples(x, y, z=None):
    stars = np.matrix([[3., -2., 0.], [3., 2., 0.]])
    if z is not None:
        x, y = z * np.matrix([x, y])
        stars = z * stars
    pl.scatter(x, y, s=10)    # 画 gaussian 随机点
    pl.scatter(np.array(stars[0]), np.array(stars[1]), s=200, marker='*', color='r')  # 画三个指定点
    pl.axhline(linewidth=2, color='g') # 画 x 轴
    pl.axvline(linewidth=2, color='g')  # 画 y 轴
    pl.axis('equal')
    pl.axis([-5, 5, -5, 5])
    pl.show()
# 产生高斯分布的随机点
mean = [0, 0]      # 平均值
cov = [[2, 1], [1, 2]]   # 协方差
x, y = np.random.multivariate_normal(mean, cov, 1000).T
plotSamples(x, y)
covMat = np.matrix(np.cov(x, y))    # 求 x 与 y 的协方差矩阵
Z = np.linalg.cholesky(covMat).I  # 仿射矩阵
plotSamples(x, y, Z)
# 求马氏距离
print( '\n到原点的马氏距离分别是：')
print( dist.mahalanobis([0,0], [3,3], covMat.I), dist.mahalanobis([0,0], [-2,2], covMat.I))
# 求变换后的欧几里得距离
dots = (Z * np.matrix([[3, -2, 0], [3, 2, 0]])).T
print ('\n变换后到原点的欧几里得距离分别是：')
print (dist.minkowski([0, 0], np.array(dots[0]), 2), dist.minkowski([0, 0], np.array(dots[1]), 2))
