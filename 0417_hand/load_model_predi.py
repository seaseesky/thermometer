import os
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
"""
def test(model):
    img0 = cv2.imread('test/1912064/sep/39-3.png')
    img0 = cv2.resize(img0,(128,128))
    test_predict = model.predict(np.array([img0]))
    print(test_predict)
"""


def main(model):
    import sys
    import numpy as np
    from cut_number import Vincent
    import cv2
    #讀取原始照片
    ori = r"./test/"
    folders = os.listdir(ori)
    folders = sorted(folders)

    ID_temp = []
    for folder in folders:
        Vincent(ori + folder + '/')
        test_img = os.listdir(ori + folder + '/sep/')
        test_img = sorted(test_img)
        #print(test_img)

        temp_value = [0,0,0,0,0,0,0,0,0,0,0,0,0]
        pic_count = 0
        pic_no = test_img[0].split('-')[0]

        for i in range(len(test_img)):
            img0 = cv2.imread(ori+ folder + '/sep/' + test_img[i])
            img = cv2.resize(img0, (128,128))
            test_predict = model.predict(np.array([img]))
            test_predict_arg = test_predict.argmax(axis=1) # 取預測出來機率最大值
            if test_img[i].split('-')[0] != pic_no :
                pic_count+=1
                pic_no = test_img[i].split('-')[0]
            if test_predict_arg <10:
                temp_value[pic_count] = temp_value[pic_count]*10+test_predict_arg
        print(temp_value)
        
        temp = max(list(map(int,temp_value)))

        if temp > 3000 and temp < 4200:
            temp = temp//10
        elif temp >500:
            temp %=1000
        print(folder,':' ,temp/10,'\n',temp_value)
        ID_temp.append([folder,temp/10])
    return ID_temp


if  __name__ == '__main__':
    os.environ["CUDA_VISIBLE_DEVICES"]="0"
    from tensorflow import ConfigProto,Session
    import keras.backend.tensorflow_backend as KTF
    cfg = ConfigProto()
    cfg.gpu_options.per_process_gpu_memory_fraction=0.2
    sess = Session(config=cfg)
    KTF.set_session(sess)


    from keras.models import load_model
    yasin = load_model(r'model_CNN_JY.h5')
    print('='*18)
    print('Made in AUO_ML6A01')
    print('='*18)    
    data = main(yasin)
    """
    import csv
    with open('output.csv','w',newline='') as csvfile:
        field_name = ['ID','temperature']
        writer = csv.writer(csvfile)
        writer.writerow(field_name)
        writer.writerows(data)
    """
    print('Done')