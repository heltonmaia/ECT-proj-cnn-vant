

import cv2 
from sklearn.model_selection import train_test_split

# Function to extract frames 
def FrameCapture(path): 
        vidObj = cv2.VideoCapture(path) 
        fps = vidObj.get(cv2.CAP_PROP_FPS)
        
        # checks whether frames were extracted 
        success = True
        aux = count = 0
        print('fps: {}'.format(fps))
        df = []
        while success:
                success, image = vidObj.read() 
                if aux%7==0:
                        df.append(image)
                        count +=1
                aux +=1
        print('{} frames salvos'.format(count))
        t_size = float(input('digite a porcentagem de teste: '))
        t_size = t_size/100.0
        X_train, X_test = train_test_split(df, test_size=t_size)
        print('tamanho do train: {}'.format(len(X_train)))
        print('tamanho do test: {}'.format(len(X_test)))
        flag='vitor'
        for i in range(len(X_train)):
                if flag=='vitor':
                        cv2.imwrite('train/vitor/frame{}.jpg'.format(i), X_train[i])
                        flag = 'mateus'
                else:
                        if flag=='mateus':
                                cv2.imwrite('train/mateus/frame{}.jpg'.format(i), X_train[i])
                                flag='lucas'
                        else:
                                cv2.imwrite('train/lucas/frame{}.jpg'.format(i), X_train[i])
                                flag='vitor'




        for i in range(len(X_test)):
                cv2.imwrite('test/frame{}.jpg'.format(i+79), X_test[i])
        

FrameCapture("DJI_0055.MP4") 
