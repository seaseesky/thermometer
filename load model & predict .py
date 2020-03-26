import os
import sys
import numpy as np
from cut_number import Vincent
import cv2
from keras.models import load_model
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
my_model = load_model(r'model_CNN_0326.h5')
"""
for test
img0 = cv2.imread('test/1912064/sep/39-3.png')
img0 = cv2.resize(img0,(128,128))
test_predict = my_model.predict(np.array([img0]))
print(test_predict)
"""
print('='*18)
print('Made in AUO_ML6A01')
print('='*18)



#讀取原始照片
ori = r"./test/"
folders = os.listdir(ori)
folders = sorted(folders)
#print('folders:',folders)
for folder in folders:
    vincent(ori + folder + '/')
    test_img = os.listdir(ori + folder + '/sep/')
    test_img = sorted(test_img)
    #print(test_img)

    temp_value = [0,0,0,0,0]
    pic_count = 0
    pic_no = test_img[0].split('-')[0]
    test_list=[]
    for i in range(len(test_img)):
        img0 = cv2.imread(ori+ folder + '/sep/' + test_img[i])
        img = cv2.resize(img0, (128,128))
        #test_list.append(img)
        #x_test = np.array(test_list).astype('float32')/255.
        test_predict = my_model.predict(np.array([img]))
        #if str(test_img[i]).split('.')[0] in  dict:
        test_predict_arg = test_predict.argmax(axis=1) # 取預測出來機率最大值
        if test_img[i].split('-')[0] != pic_no :
            pic_count+=1
            pic_no = test_img[i].split('-')[0]
        if test_predict_arg <10:
            temp_value[pic_count] = temp_value[pic_count]*10+test_predict_arg
    
    temp = max(list(map(int,temp_value)))
    if temp > 3000 and temp < 4200:
        temp = int(temp/10)
    elif temp >500:
        temp %=1000
    print(folder,':' ,temp)