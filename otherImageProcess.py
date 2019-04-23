"""
	图片融合
"""
# coding=utf-8

# 底板图案
bottom_pic = 'elegent.jpg'
# 上层图案
top_pic = 'lena.jpg'

import cv2
bottom = cv2.imread(bottom_pic)
top = cv2.imread(top_pic)
# 权重越大，透明度越低
overlapping = cv2.addWeighted(bottom, 0.8, top, 0.2, 0)
# 保存叠加后的图片
cv2.imwrite('overlap(8:2).jpg', overlapping)
