def Vincent(read_dir):
	import os
	import sys
	import numpy as np
	import cv2

	#讀取影像資料夾
	target_path = read_dir
	#切割後字元存放處
	try:
		os.mkdir(target_path+'/sep')
	except:
		pass
	
	path = target_path+'/sep/'
	files = os.listdir(target_path)

	for file in files:
		try:
			img0 = cv2.imread(target_path + file)
			img_g = cv2.cvtColor(img0, cv2.COLOR_BGR2GRAY)
			img_g[img_g[:,:] < 230] = 0 
			ret, binary = cv2.threshold(img_g, 110, 255, cv2.THRESH_BINARY)
			rawimg = binary - binary[0,1]

			row_nz = []
			for row in rawimg.tolist():
				row_nz.append(len(row) - row.count(0))
			idx=np.array(row_nz)>(max(row_nz)/4) #截出上下的範圍
			np.where(idx==1)[0][0],np.where(idx==1)[0][-1]
			up_y=np.where(idx==1)[0][-1] #上界
			down_y=np.where(idx==1)[0][0] #下界
			rawimg1=rawimg[down_y:up_y,]
			

			# counting non-zero value by column, x axis
			col_nz = []
			for col in rawimg1.T.tolist():
				col_nz.append(len(col) - col.count(0))

			idy=np.not_equal(col_nz,0)
			record_y=[] #如果有八個數字，裡面應該要有九個格子(一開始找出七個，前後插入變九個)
			for i in range(0,(len(np.where(idy==1)[0])-1)):
				# 如果下一個數是0就略過，直到找到下一個數不是0的位置
				if(np.where(idy==1)[0][i+1]-np.where(idy==1)[0][i]==1):
					pass
				else:
					record_y.append(np.where(idy==1)[0][i])

			# 插入第一個非0位置跟最後一個非0的位置
			record_y.insert(0,np.where(idy==1)[0][0])
			record_y.append(np.where(idy==1)[0][-1])

			# 檢查數字
			rm_id=[]
			if len(record_y)>9:
				for j in range(0,len(record_y)-1):
					temp=np.array(col_nz[record_y[j]:record_y[j+1]])
					#如果只是雜訊，就刪掉
					if sum(temp>(max(col_nz)/4))==0:
						rm_id.append(record_y[j+1])

			for x in rm_id:
					record_y.remove(x)

			for i in range(0,len(record_y)-1):
				a=binary[down_y:up_y,record_y[i]:record_y[i+1]]
				a=cv2.resize(a, (56, 56), interpolation=cv2.INTER_CUBIC)
				save_name= file.split('.')[0]+ '-'+str(i)+'.png' 
				cv2.imwrite(os.path.join(path, save_name), a)	
		except:
			pass
