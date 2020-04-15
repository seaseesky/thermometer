import time
import numpy as np
import cv2
from opcua import Client
from opcua import ua

def announcement(word):
    print('='*10,time.ctime(),'='*10)
    print(word)
    print('-'*10)
class SubHandler(object):
    def datachange_notification(self, node, val, data):
        # Record condition
        try:
            announcement("New data change")
            img = np.array(val)
            img = np.rot90(img,3)
            cv2.imwrite("0.png",img)
            
        except:
            print('ex   ')
            #cv2.destroyAllWindows()

def main():
    try:
        client.connect()
        announcement('Connected')
        temp = client.get_node("ns=2;i=2")

    # Check data change
        handler = SubHandler()
        sub = client.create_subscription(500, handler)
        handle = sub.subscribe_data_change(temp)
        if input('type q to leave') == 'q':pass
        #if input("type q to leave")=='q':pass
    except:
        pass
        

if __name__ == "__main__":
    running = True
    client = Client("opc.tcp://192.168.0.101:4840/")
    try:
        main()
    except:
        pass
    client.disconnect()
    cv2.destroyAllWindows()
    announcement('End')
    
    
    
            
