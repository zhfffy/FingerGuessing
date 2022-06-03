import numpy as np
import cv2 as cv
from keras.models import load_model
import matplotlib.pyplot as plt
from PIL import Image

model = load_model('my_model') # 调用所训练的模型

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
    cap = cv.VideoCapture(0) # 调用摄像头
    filename = '00.jpg'
    while True:
        success,frame = cap.read() # 读取每一帧
        new_img = cv.flip(frame, 1) # 翻转
        roi = new_img

        ## 肤色检测 (YCrCb之Cr分量 + OTSU二值化)
        # 把图像转换到YUV色域
        ycrcb = cv.cvtColor(roi, cv.COLOR_BGR2YCrCb)  
        # 图像分割, 分别获取y, cr, br通道图像
        (y, cr, cb) = cv.split(ycrcb)  

        ## 高斯滤波, cr 是待滤波的源图像数据, (5,5)是值窗口大小, 0 是指根据窗口大小来计算高斯函数标准差
        # 对cr通道分量进行高斯滤波
        cr1 = cv.GaussianBlur(cr, (5, 5), 0)  
        # 根据OTSU算法求图像阈值, 对图像进行二值化
        _, skin1 = cv.threshold(cr1, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
        # 展示处理后的图片skin1（黑白手势图片）
        cv.imshow('skin',skin1)  

        ## 轮廓查找
        # 对skin1进行轮廓查找
        image, contours, hierarchy = cv.findContours(skin1, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)  

        # 获取最大轮廓
        areas = []
        for c in range(len(contours)):
            areas.append(cv.contourArea(contours[c]))
        max_id = areas.index(max(areas))
        max_rect = cv.minAreaRect(contours[max_id])

        # 对捕获到的最大轮廓进行识别，并显示轮廓框架图
        # for item in contours:
        (x, y, w, h) = cv.boundingRect(contours[max_id]) # 获得最小矩形框架
        if w >= 50 and h >= 50: # 在较大的框架中查找
            # 获得、展示、保存矩形轮廓图(相当于裁剪skin1)
            img = skin1[y : y + h, x : x + w] 
            cv.imshow('img',img) 
            cv.imwrite(filename, img) 
            
            # 识别矩形轮廓图
            img = pre_pic(filename)
            img = img.reshape(1, 1, 100, 100).astype('float32')  # 修改数据格式
            img = img / 255  # 归一化
            predictions = model.predict_classes(img)  # 预测结果
            flag = model.predict(img) # 预测概率
            if max(flag[0]) > 0.5:  # 概率大于0.5才框出
                print(predictions)
                if predictions[0] == 0:
                    s = "jiandao"
                elif predictions[0] == 1:
                    s = "shitou"
                elif predictions[0] == 2:
                    s = "bu"
                elif predictions[0] == 3: # 预测为人脸则跳过
                    continue
                cv.rectangle(new_img, (x, y), (x + w, y + h), (255, 0, 0), 0) # 用矩形框出
                cv.putText(new_img, s, (x, y), cv.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 2, 8) # 在矩形上方显示文字

        # 展示添加框架后的摄像机图像
        cv.imshow('image', new_img)

        Key = cv.waitKey(1)
        if Key == ord(' '):  #按下空格键退出
            break

    cap.release() #释放占用资源
    cv.destroyAllWindows() #释放opencv创建的所有窗口