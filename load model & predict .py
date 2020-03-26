import os
import sys
import pandas as pd
import numpy as np
from pandas.core.frame import DataFrame
from cut_number import vincent
import cv2
import matplotlib.pyplot as plt
from pylab import rcParams

#讀取原始照片



test_img=[]
test_list=[]
for i in range(len(test_img)):
    img0 = cv2.imread(test_img[i][0])
    img = cv2.resize(img0, (128,128))
    test_list.append(img)
    
x_test = np.array(test_list).astype('float32')/255.


from keras.models import load_model
my_model = load_model(r'model_CNN_0326.h5')
test_predict = my_model.predict(x_test)
test_predict_arg = test_predict.argmax(axis=1) # 取預測出來機率最大值