from tensorflow.keras.layers import Dense,Dropout,Conv2D,MaxPooling2D,Flatten,Activation,AvgPool2D,MaxPool2D,GlobalAvgPool2D
from tensorflow.keras import models
from src.visualize import cnnlayer
from src.data.generators import create
from tensorflow import keras


train, test = create()

model = keras.Sequential()
model.add(Conv2D(filters=32,kernel_size=4,input_shape=(512,512,3)))
model.add(Activation('relu'))
model.add(MaxPool2D(2,2))
model.add(Conv2D(filters=64,strides=2,kernel_size=4))
model.add(Activation('relu'))
model.add(MaxPool2D(4,4))
model.add(Flatten())
model.add(Dense(25,activation='relu'))
model.add(Dense(2,activation='softmax'))
model.summary()
opt = keras.optimizers.RMSprop()
model.compile(optimizer=opt,loss='categorical_crossentropy',metrics=['accuracy','AUC'])
history = model.fit(train,steps_per_epoch=train.samples//8,validation_data=test,validation_steps=test.samples//8,epochs=20)

model.save('src/model/saved/covid-19')