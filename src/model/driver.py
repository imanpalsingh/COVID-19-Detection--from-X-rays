'''
Author: Imanpal Singh <imanpalsingh@gmail.com>
Location:  src.model
Date Created: 01-08-2020
Date Modified: 04-09-2020
'''

'''

Change Logs
===========

None
'''

from src.data import generators
from src.model.baseline import Convolutional

if __name__ == "__main__":

    model = Convolutional()
    model.compile(optimizer='adam',metrics=['accuracy'],loss='categorical_crossentropy')
    train_gen,test_gen = generators.create('dataset/final/training/','dataset/final/testing/')
    
    model.fit(train_gen,steps_per_epoch=14,epochs=30)

