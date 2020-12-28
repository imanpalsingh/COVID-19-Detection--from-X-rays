'''
File name : cnn.py
Location : src.model
Author : Imanpal Singh <imanpalsingh@gmail.com>
'''
'''
Change log:

28-12-20 :

    1) Hyper parameterized

'''
from tensorflow.keras.layers import Dense,Dropout,Conv2D,MaxPooling2D,Flatten,Activation,AvgPool2D,MaxPool2D,GlobalAvgPool2D
from tensorflow.keras import models
from src.data.generators import create
from tensorflow import keras
import datetime
from matplotlib import pyplot as plt

train, test = create()

## Model ##

model = keras.Sequential()
model.add(Conv2D(filters=32,kernel_size=4,input_shape=(256,256,3)))
model.add(Activation('relu'))
model.add(MaxPool2D(2,2))
model.add(Flatten())
model.add(Dense(15,activation='relu'))
model.add(Dense(1,activation='sigmoid'))
model.summary()

## Callbacks##
log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)
early_Stopping = keras.callbacks.EarlyStopping(monitor='loss', patience=3)

opt = keras.optimizers.Adam(learning_rate=0.0001)
model.compile(optimizer=opt,loss='binary_crossentropy',metrics=['accuracy','AUC',keras.metrics.Recall(), keras.metrics.Precision()])

history = model.fit(train,steps_per_epoch=train.samples//8,validation_data=test,validation_steps=test.samples//8,
epochs=10,callbacks=[tensorboard_callback,early_Stopping])


model.save('src/model/saved/covid-19')