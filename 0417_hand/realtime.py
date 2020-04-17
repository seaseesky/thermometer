import os
import numpy as np
import cv2
from keras.models import load_model
import numpy as np
import time


def Separate(img_g):
	img_list = []
	try:
		#img_g[img_g[:,:] < 230] = 0 
		#_, binary = cv2.threshold(img_g, 110, 255, cv2.THRESH_BINARY)
		binary = img_g
		rawimg = binary - binary[0,1]

		row_nz = []
		for row in rawimg.tolist():
			row_nz.append(len(row) - row.count(0))
		idx=np.array(row_nz)>(max(row_nz)/4) 
		np.where(idx==1)[0][0],np.where(idx==1)[0][-1]
		up_y=np.where(idx==1)[0][-1] 
		down_y=np.where(idx==1)[0][0] 
		rawimg1=rawimg[down_y:up_y,]

		col_nz = []
		for col in rawimg1.T.tolist():
			col_nz.append(len(col) - col.count(0))

		idy=np.not_equal(col_nz,0)
		record_y=[]
		for i in range(0,(len(np.where(idy==1)[0])-1)):
			if(np.where(idy==1)[0][i+1]-np.where(idy==1)[0][i]==1):
				pass
			else:
				record_y.append(np.where(idy==1)[0][i])

		record_y.insert(0,np.where(idy==1)[0][0])
		record_y.append(np.where(idy==1)[0][-1])

		rm_id=[]
		if len(record_y)>9:
			for j in range(0,len(record_y)-1):
				temp=np.array(col_nz[record_y[j]:record_y[j+1]])
				if sum(temp>(max(col_nz)/4))==0:
					rm_id.append(record_y[j+1])
		
		for x in rm_id:
				record_y.remove(x)
		
		for i in range(0,len(record_y)-1):
			a = binary[down_y:up_y,record_y[i]:record_y[i+1]]
			if min(a.shape)<10:continue
			a = cv2.resize(a, (32,32), interpolation=cv2.INTER_CUBIC)
			a = np.reshape(a,(32,32,1))
			#a = cv2.cvtColor(a,cv2.COLOR_GRAY2BGR)
			img_list .append(a)
	except:
		pass
	return np.array(img_list).astype('float32')/255.





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
