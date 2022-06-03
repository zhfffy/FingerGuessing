import sys
import os
import inspect
import numpy as np
import cv2 as cv
from keras.models import load_model
import matplotlib.pyplot as plt
from PIL import Image

# 读取图片，调整大小(100*100)，转为numpy数组
def pre_pic(picName):
    # 先打开传入的原始图片
    img = Image.open(picName)
    # 使用消除锯齿的方法resize图片
    reIm = img.resize((100,100),Image.ANTIALIAS)
    # 变成灰度图，转换成矩阵
    im_arr = np.array(reIm.convert("L"))
    return im_arr

if __name__ == '__main__':
    # path = inspect.getfile(inspect.currentframe())
    abspath = os.getcwd()  # unity调用时，此处会返回unity项目的根目录FingerGuessing，而不是py文件所在的子目录FingerGuessingModel
    modelpath = abspath + "\\FingerGuessingModel\\my_model"
    picpath = abspath + "\\Assets\\Results\\gesture.jpg"

    #modelpath = "D:\\Program Files\\unityproject\\FingerGuessing\\FingerGuessingModel\\my_model"
    #picpath = "D:\\Program Files\\unityproject\\FingerGuessing\\Assets\\Results\\gesture.jpg"
    ## sys.argv 是将shell命令中除去‘python’后以空格分割的数组，index=0是python脚本的路径，index=1之后的是对应为的参数
    
    model = load_model(modelpath) # 调用所训练的模型

    ## 读取图片 存储为三维数组new_img
    new_img = cv.imread(picpath)
    temp = new_img
    ## cv.imshow("ori_image", temp)

    ## 肤色检测 (YCrCb之Cr分量 + OTSU二值化)
    # 把图像转换到YUV色域
    ycrcb = cv.cvtColor(temp, cv.COLOR_BGR2YCrCb)
    # 图像分割, 分别获取y, cr, br通道图像
    (y, cr, cb) = cv.split(ycrcb)  

    ## 高斯滤波, cr 是待滤波的源图像数据, (5,5)是值窗口大小, 0 是指根据窗口大小来计算高斯函数标准差
    # 对cr通道分量进行高斯滤波
    cr1 = cv.GaussianBlur(cr, (5, 5), 0) 
    # 根据OTSU算法求图像阈值, 对图像进行二值化
    _, skin1 = cv.threshold(cr1, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    # 展示处理后的图片skin1（黑白手势图片）
    # cv.imshow('skin',skin1)

    ## 轮廓查找
    filename = "contour.jpg" # 保存轮廓图片名
    predict_flag = 0.5
    predict_class = -1      
    
    # 对skin1进行轮廓查找
    image, contours, hierarchy = cv.findContours(skin1, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)  # 轮廓查找

    # 获取最大轮廓
    areas = []
    for c in range(len(contours)):
        areas.append(cv.contourArea(contours[c]))
    max_id = areas.index(max(areas))

    # 对捕获到的最大轮廓进行识别，并显示轮廓框架图
    # for item in contours:
    #    (x, y, w, h) = cv.boundingRect(item) # 获得最小矩形框架
    (x, y, w, h) = cv.boundingRect(contours[max_id]) # 获得最小矩形框架
    if w >= 50 and h >= 50: # 在较大的框架中查找
        # 获得、展示、保存矩形轮廓图(相当于裁剪skin1)
        img = skin1[y : y + h, x : x + w] 
        ## cv.imshow('img',img) 
        cv.imwrite(filename, img) 

        # 识别矩形轮廓图
        img = pre_pic(filename)
        img = img.reshape(1, 1, 100, 100).astype('float32')  # 修改数据格式
        img = img / 255  # 归一化
        predictions = model.predict_classes(img)  # 预测结果
        flag = model.predict(img) # 预测概率
        print(flag[0])
        if max(flag[0]) > predict_flag:  # 概率大于0.5才框出
            #predict_flag = max(flag[0])
            if predictions[0] == 0:
                s = "jiandao"
                predict_class = 0
            elif predictions[0] == 1:
                s = "shitou"
                predict_class = 1
            elif predictions[0] == 2:
                s = "bu"
                predict_class = 2 
            ## cv.rectangle(new_img, (x, y), (x + w, y + h), (255, 0, 0), 0) # 用矩形框出
            ## cv.putText(new_img, s, (x, y), cv.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 2, 8) # 在矩形上方显示文字

    # 展示添加框架后的摄像机图像
    # cv.imshow('image', new_img)  

    # key = cv.waitKey(0) 
    
    print(predict_class) 