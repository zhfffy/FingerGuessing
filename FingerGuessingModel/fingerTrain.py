import numpy as np
import os
import cv2 as cv
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.utils import np_utils
from keras import backend
from PIL import Image
backend.set_image_data_format('channels_first')

# 更改动态分配内存
import tensorflow as tf
import keras
config = tf.ConfigProto()
config.gpu_options.allow_growth = True
keras.backend.tensorflow_backend.set_session(tf.Session(config=config))

# 设定随机种子
seed = 7
np.random.seed(seed)

# 读取图片，调整大小(100*100)，转为numpy数组
def pre_pic(picName):
    # 先打开传入的原始图片
    img = Image.open(picName)
    # 使用消除锯齿的方法resize图片
    reIm = img.resize((100,100),Image.ANTIALIAS)
    # 变成灰度图，转换成矩阵
    im_arr = np.array(reIm.convert("L"))
    return im_arr

# 用pre_pic函数将图片转为numpy数组，并将所有图片的数组合并为一个数组
def get_files(file_dir):
    flag = 0
    for file in os.listdir(file_dir):
        image_file_path = os.path.join(file_dir,file)
        if file == '0':  # 文件名为‘0’表示剪刀
            temp = 0  # 设置标签temp=0
        elif file == '1':  # 文件名为‘1’表示石头
            temp = 1  # 设置标签temp=1
        elif file == '2':  # 文件名为‘2’表示布
            temp = 2  # 设置标签temp=2
        elif file == '3':  # 文件名为‘3’表示人脸
            temp = 3  # 设置标签temp=3
        for image_name in os.listdir(image_file_path):
            image_name_path = os.path.join(image_file_path,image_name)
            img = pre_pic(image_name_path)  # 将图片通过pre_pic函数转为numpy数组，例如img.shape=(100，100)
            if flag == 0:  # 第一次处理
                X_image = img[np.newaxis,:]  # X_image.shape=(1,100,100)
                Y_image = np.array([temp])  # Y_image.shape=(1,)
                flag = 1
            else:  # 第n次处理(n!=1)
            	#将(n-1,100,100)与(1,100,100)合并为(n,100,100)
                X_image = np.vstack((X_image,img[np.newaxis,:]))
                #将(n-1,)与(1,)合并为(n,)
                Y_image = np.hstack((Y_image,np.array([temp])))

    return X_image,Y_image  # X_image为图片数据，Y_image为标签

# 创建、编译模型
def create_model():
    model = Sequential()
    # 100 * 100 * 1
    model.add(Conv2D(filters=8, kernel_size=(3,3),strides=(1,1),padding='same',input_shape=(1,100,100),activation='relu'))
    # 100 * 100 * 8
    model.add(MaxPooling2D(pool_size=(2,2)))
    print("111")
    print(model)
    # 50 * 50 * 8
    model.add(Conv2D(filters=16, kernel_size=(3,3),strides=(1,1),padding='same',activation='relu'))
    # 50 * 50 * 16
    
    # 只使用keep_prob*cell_size的神经元进行训练，其余神经元不进行迭代
    model.add(Dropout(0.5))
    model.add(MaxPooling2D(pool_size=(4,4)))
    
    model.add(Dense(16,activation='relu'))
    
    model.add(Flatten())
    ## model.add(Dense(4,activation='softmax'))
    model.add(Dense(3,activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model


if __name__ == "__main__":
    filetrain = "D:\\Users\\Owner\\Desktop\\project\\FingerGuessing\\gesture_data"
    filetest = "D:\\Users\\Owner\\Desktop\\project\\FingerGuessing\\gesture_test"
    print('start')
    X_train,Y_train = get_files(filetrain)
    X_test,Y_test = get_files(filetrain)
    print(X_train.shape)
    print(Y_train.shape)
    
    # 修改数据格式
    X_train = X_train.reshape(X_train.shape[0], 1, 100, 100).astype('float32')
    X_test = X_test.reshape(X_test.shape[0], 1, 100, 100).astype('float32')

    # 格式化数据到0-1之前
    X_train = X_train / 255
    X_test = X_test / 255

    # one-hot编码
    Y_train = np_utils.to_categorical(Y_train)
    Y_test = np_utils.to_categorical(Y_test)

    #  创建、编译模型
    model = create_model()

    #  训练模型
    model.fit(X_train, Y_train, epochs=40, batch_size=300, verbose=2)

    #  评估模型
    score = model.evaluate(X_test, Y_test, verbose=0)
    print('acc: %.2f%%' % (score[1] * 100))

    #  保存模型
    model.save('my_model')
