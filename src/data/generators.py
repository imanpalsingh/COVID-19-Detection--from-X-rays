'''
File name : generators.py
Location : src.data
Author : Imanpal Singh <imanpalsingh@gmail.com>
'''

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import models
import os

IMG_SHAPE = (256,256)
BATCH_SIZE = 8

def create(dir : str = "src/Dataset/traintest/") :

    '''
    Function returns train,val and test generators created on train test separated dataset

    Input
    =====

    `dir` : the direcotry containing training and testing data 

    '''
    train = ImageDataGenerator(rescale = 1.0/255,samplewise_center=True,
        samplewise_std_normalization= True,
        rotation_range = 40,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,)
        
    test = ImageDataGenerator(rescale = 1.0/255)

    tr_gen = train.flow_from_directory(os.path.join(dir,'Train'),target_size=IMG_SHAPE,batch_size=BATCH_SIZE,shuffle=True,class_mode="binary")
    #va_gen = train.flow_from_directory(os.path.join(dir,'train'),target_size=IMG_SHAPE,batch_size=64,shuffle=False,subset="validation")
    te_gen = test.flow_from_directory(os.path.join(dir,'Test'),target_size=IMG_SHAPE,batch_size=BATCH_SIZE,shuffle=False,class_mode="binary")

    return tr_gen,te_gen


def create_new(dir : str, model_save_dir : str = "src/model/saved/Transfer19"):

    '''
    Function returns a generator for the new dataset to apply prediction on. Then applies prediction using the saved model and 
    returns the result and filenames associated with the result

    Input
    =====

    `dir` : the direcotry containing Images
    `model_save_dir`  the direcotry containing saved trained model

    '''
    
    test = ImageDataGenerator(rescale = 1.0/255)
    data = test.flow_from_directory(dir,target_size=IMG_SHAPE,batch_size=1, shuffle=False, class_mode=None)
    print("Success")
    steps = len(data.filenames)
    model = models.load_model(model_save_dir)

    predictions = model.predict(data,steps=steps)

    return data.filenames, predictions