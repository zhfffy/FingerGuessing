import cv2 as cv

import cv2 as cv

if __name__ == "__main__":
    m_0 = 0  #剪刀
    m_1 = 0  #石头
    m_2 = 0  #布
    m_3 = 0  #人脸（加个人脸标签用于避免将人脸错误识别）
    flag = 0
    cap = cv.VideoCapture(0) # 调用摄像头
    while True:
        success, frame = cap.read() # 读取每一帧
        new_img = cv.flip(frame, 1) # 翻转
        roi = new_img

        # YCrCb之Cr分量 + OTSU二值化（肤色检测）
        ycrcb = cv.cvtColor(roi, cv.COLOR_BGR2YCrCb)  # 把图像转换到YUV色域
        (y, cr, cb) = cv.split(ycrcb)  # 图像分割, 分别获取y, cr, br通道图像

        # 高斯滤波, cr 是待滤波的源图像数据, (5,5)是值窗口大小, 0 是指根据窗口大小来计算高斯函数标准差
        cr1 = cv.GaussianBlur(cr, (5, 5), 0)  # 对cr通道分量进行高斯滤波
        # 根据OTSU算法求图像阈值, 对图像进行二值化
        _, skin1 = cv.threshold(cr1, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
        cv.imshow('skin1', skin1)  # 展示处理后的图片

        # 轮廓查找
        image, contours, hierarchy = cv.findContours(skin1, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        for item in contours:  # 遍历所有轮廓
            (x, y, w, h) = cv.boundingRect(item) # 获得最小矩形框架
            if w >= 50 and h >= 50: # 在较大的框架中查找
                img = skin1[y : y + h, x : x + w]  # 获得矩形轮廓图
                cv.imshow('img', img)  # 展示矩形轮廓图
                cv.rectangle(new_img, (x, y), (x + w, y + h), (255, 0, 0), 0) # 在new_img中用矩形框出
                k = cv.waitKey(1) # 等待键盘促发
                if k == ord(' '):  # 按下空格退出
                    flag = 1
                    break
                elif k == ord('a'): # 按A收集剪刀图片
                    # 按下后将图片保存到指定路径（imencode函数可以有中文路径）
                    cv.imencode('.jpg', img)[1].tofile("D:\\Users\\Owner\\Desktop\\project\\FingerGuessing\\extra_data\\0\\{}.png".format(m_0))
                    m_0 += 1
                    print('正在保存0-roi图片,本次图片数量:', m_0)
                elif k == ord('p'): # 按S收集石头图片
                    cv.imencode('.jpg', img)[1].tofile("D:\\Users\\Owner\\Desktop\\project\\FingerGuessing\\extra_data\\1\\{}.png".format(m_1))
                    m_1 += 1
                    print('正在保存1-roi图片,本次图片数量:', m_1)
                elif k == ord('d'): # 按D收集布图片
                    cv.imencode('.jpg', img)[1].tofile("D:\\Users\\Owner\\Desktop\\project\\FingerGuessing\\extra_data\\2\\{}.png".format(m_2))
                    m_2 += 1
                    print('正在保存2-roi图片,本次图片数量:', m_2)
                elif k == ord('f'): # 按F收集人脸图片
                    cv.imencode('.jpg', img)[1].tofile("D:\\Users\\Owner\\Desktop\\project\\FingerGuessing\\extra_data\\3\\{}.png".format(m_3))
                    m_3 += 1
                    print('正在保存3-roi图片,本次图片数量:', m_3)

        cv.imshow("frame", new_img) # 展示new_img图像
        if flag == 1:
            break

    cap.release() #释放占用资源
    cv.destroyAllWindows() #释放opencv创建的所有窗口