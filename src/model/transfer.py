'''
File name : transfer.py
Location : src.gui
Author : Imanpal Singh <imanpalsingh@gmail.com>
'''
'''
Change log:

28-12-20 :

    1) USed Xception for Feature extrction 

'''
from tensorflow import keras
from tensorflow.keras.applications import Xception
from src.data.generators import create
import datetime

INPUT_SHAPE = (256,256,3)

feature_extraction = Xception(input_shape=INPUT_SHAPE,include_top=False)

feature_extraction.trainable = False


Input = keras.Input(shape = INPUT_SHAPE)
x = feature_extraction(Input)
x = keras.layers.GlobalAveragePooling2D()(x)
x = keras.layers.Dropout(0.2)(x)
x = keras.layers.Dense(512,activation='relu')(x)
x = keras.layers.Dense(512,activation='relu')(x)
Output = keras.layers.Dense(1,activation='sigmoid')(x)

model = keras.Model(inputs = Input, outputs = Output)
model.compile(optimizer=keras.optimizers.Adam(lr=0.0001), loss=keras.losses.BinaryCrossentropy(from_logits=True)
, metrics=['accuracy','AUC'])

model.summary()
train,test = create()

log_dir = "logs/fitTransfer/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

early_Stopping = keras.callbacks.EarlyStopping(monitor='loss', patience=3)



history = model.fit(train,steps_per_epoch=train.samples//8,validation_data=test,validation_steps=test.samples//8,
epochs=10,callbacks=[tensorboard_callback,early_Stopping])

model.save('src/model/saved/Transfer19')