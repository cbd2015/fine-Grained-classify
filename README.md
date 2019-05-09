# fine-Grained-classify
fine-Grained classify 细颗粒度图像分类
## 总体框架
参考文献
参考开源代码
研发代码同步
总结
### 1. 论文参考
    > Bilinear CNNs for Fine-grainedVisual Recognition.pdf（双线性卷积细颗粒度图像识别方法）；
    > bcnn_iccv15.pdf (作者源码使用的是matlab语言)；
结合目标检测、人工标注、图像分割等方法提取关键的细粒度图像，在进行softmax分类；
### 2. 参考开源代码
    > Bilinear-CNN-TensorFlow.
    > Fine_Grained_Classification.
    > tensorflow_compact_bilinear_pooling.
    > VGG-or-MobileNet-SSD.

### 3. 代码功能说明
    > enhanceImagePy 是图像预处理的，数据增强的方案； 包括：图像翻转、裁剪、局部均衡化、灰度化、压缩、椒盐噪声处理等
    > test.py 是用于测试的python入口文件
    > post.py 是一种用于测试上线系统实际效果测试的post批量自动化请求并获取识别结果的一个python脚本；
    > othersImageProcess.py 其他处理图像的封装函数，包括：图像镜像、图像融合
