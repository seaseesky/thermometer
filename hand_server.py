import cv2
cap = cv2.VideoCapture(0)
import time
import numpy as np
from opcua import ua,Server
show_mode = False

def main():
    count = 0
    while running:
        frame = cap.read()[1]
        frame = frame[40:470,120:450]
        frame = cv2.resize(frame,(33*2,43*2))#,interpolation=cv2.INTER_NEAREST)
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray,50,255,cv2.THRESH_BINARY_INV)[1]
        #thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU )[1]

        if show_mode:
            cv2.imshow('gray',gray)
            cv2.imshow('thr',thresh)
            if cv2.waitKey(1) and 0xFF == ord('q'):break
        else:
            if np.mean(thresh)<=30:
                #print('idle')
                pass
            else:
                #print('temp')
                Temp.set_value(thresh.tolist())
        time.sleep(0.1)


if __name__ == '__main__':
    server = Server()
    server.set_endpoint("opc.tcp://192.168.0.101:4840")
    obj    = server.get_objects_node()
    uri    = server.register_namespace("ML6A01")
    Thermo = obj.add_object(uri,"Thermometer")
    Temp   = Thermo.add_variable(uri,"Temperature",[''])
    running = True
    
    server.start()
    main()
    server.stop()
    cap.release()
    if show_mode:cv2.destroyAllWindows()
