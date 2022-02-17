import tensorflow as tf
import PIL.Image as Image
import numpy as np

def train():
    
    import os
    import matplotlib.pyplot as plt
    
    import keras
    from keras.models import Sequential
    from keras.layers import Dense, Dropout, Flatten
    from keras.layers.convolutional import Conv2D, MaxPooling2D
    from keras.utils import np_utils
    from sklearn.model_selection import train_test_split


    img_rows, img_cols = 56, 28*3  # 신경망에 입력할 이미지의 사이즈입니다.         
    datas_x, datas_y = [], []
    
    
    
    # 데이터를 불러옵니다.
    file_list = os.listdir("records")
    for i in range(len(file_list)):
        
        img = Image.open("records/"+file_list[i])               #이미지를 읽어옵니다.
        img = img.resize((img_rows, int(img_cols/3)))           #이미지를 축소시킵니다.
        img = np.asarray(img).astype(float)/255                 #이미지를 0~255 -> 0.0~1.0으로 정규화
        img = np.vstack((img[:,:,0],img[:,:,1],img[:,:,2]))     #RGB -> R,G,B 이미지로 분리합니다.
        datas_x.append(img) 
        
        motorRL = list(map(int,file_list[i].split("d")[1].replace(".png","")))  # 이름에서 모터 데이터를 가져옵니다.
        throttle = (int(file_list[i].split("s")[1].split("d")[0]))//50         # 스로틀은 50단위로 그루핑합니다.
        data_y = sum(motorRL[i]*(2**i) for i in range(len(motorRL)))            # 라벨에서 모터는 1의 자리입니다.
        data_y = data_y + throttle*5                                            # 라벨에서 스로틀은 5의 자리입니다.
        datas_y.append(data_y)
        
            
    datas_x = np.array(datas_x)
    datas_y = np.array(datas_y)
    
    
    # 학습 성능 평가를 위하여 train과 test용 데이터를 분리합니다.
    
    # 10장 이하의 라벨은 측정이 불가하므로 필터링합니다.
    data = np.unique(datas_y, return_counts=True)
    print(data)
    data_y_c = datas_y.copy()
    dataU10 = data[0][data[1]>10]
    datas_y = datas_y[np.isin(data_y_c, dataU10)]
    datas_x = datas_x[np.isin(data_y_c, dataU10)]
    
    x_train, x_test, y_train, y_test = train_test_split(
        datas_x, datas_y, 
        test_size=0.3, 
        shuffle=True, 
        stratify=datas_y, 
        random_state=34)
    print('x_train shape:', x_train.shape)
    print(x_train.shape[0], 'train samples')
    print(x_test.shape[0], 'test samples')



    
    print(np.unique(y_train, return_counts=True))
    output_shape = y_train.max()+1   # 출력단의 개수입니다.
    
    # 라벨링 작업을 수행합니다.
    y_train = keras.utils.np_utils.to_categorical(y_train, output_shape)
    y_test = keras.utils.np_utils.to_categorical(y_test, output_shape)

    # 학습을 시작합니다.
    batch_size  = 100        # 한 학습연산에 계산될 데이터 개수입니다.
    epochs      = 10         # 학습횟수 입니다. 많다면 정확해집니다.
    input_shape = (img_cols, img_rows, 1)     # 입력될 이미지의 사이즈입니다.
    
    

    # cnn 학습모델입니다. 
    model = Sequential()
    filterCnt = 32  # 1차 특징의 개수입니다.
    denseCnt = 500  # 히든레이어의 개수입니다.
    
    # 특징 이미지를 형성합니다.
    model.add(Conv2D(filterCnt, kernel_size=(5, 5), strides=(1, 1), padding='same', activation='relu', input_shape=input_shape))
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
    model.add(Conv2D(filterCnt*2, (2, 2), activation='relu', padding='same'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25)) # 과적합 방지를 위한 드롭아웃
    model.add(Flatten())     # 입력단 형성
    # 신경망을 형성합니다.
    model.add(Dense(denseCnt, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(output_shape, activation='softmax'))
    model.summary()

    model.compile(
        loss='categorical_crossentropy', 
        optimizer='adam', 
        metrics=['accuracy'])

    hist = model.fit(
        x_train, y_train, 
        batch_size=batch_size, 
        epochs=epochs, 
        verbose=1, 
        validation_data=(x_test, y_test))



    # 학습 진행
    score = model.evaluate(x_test, y_test, verbose=0)
    print('Test loss:', score[0])
    print('Test accuracy:', score[1])
    
    return model

if __name__ == "__main__":
    train()
