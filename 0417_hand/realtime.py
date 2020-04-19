import os
import cv2
from keras.models import load_model
import numpy as np
import time








def predict(pred_img,model):
	imgs= Separate(pred_img)
	test_predict = model.predict(imgs)
	test_predict_arg = test_predict.argmax(axis=1)
	value = "".join(str(x) for x in test_predict_arg)
	return(int(value))

def background(_ID,_model):
	loop_count = 0
	h_temp = -99
	while loop_count<5:	
		start = time.time()
		frame = cv2.imread(f'./test2/{_ID}/{6+loop_count}.png')	
		grayed = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		temp = predict(grayed,_model)
		print(temp)
		loop_count+=1
	print(f'ID : {_ID}  - temp : {temp}  - time_cost: {(time.time()-start):1.3f}s')


def main():
	my_model = load_model(r'model_CNN_32x32.h5')
	print('='*18)
	print('Made in AUO_ML6A01')
	print('='*18)
	
	while 1:
		#ID = input('Type or Touch:')
		ID = '1912375'
		if ID in ['q' , 'Q']:break
		print(f'{ID}---------------------')
		time.sleep(0.5)
		background(ID,my_model)
	
	

			

if __name__ == '__main__':
	os.environ["CUDA_VISIBLE_DEVICES"]="0"
	from tensorflow import Session
	from tensorflow import ConfigProto
	import keras.backend.tensorflow_backend as KTF
	cfg = ConfigProto()
	cfg.gpu_options.allow_growth = True
	sess = Session(config=cfg)
	KTF.set_session(sess)
	main()
	print('End')
