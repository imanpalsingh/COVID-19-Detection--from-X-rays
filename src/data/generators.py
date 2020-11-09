from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import models
import os

def create(dir : str = "src/Dataset/traintest/") :

    '''
    Function returns train,val and test generators created on train test separated dataset

    Input
    =====

    `dir` : the direcotry containing training and testing data 

    '''
    train = ImageDataGenerator(rescale = 1.0/255,samplewise_center=True,
        samplewise_std_normalization= True,
        rotation_range = 15,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        fill_mode="nearest",
        vertical_flip=True,
        cval=0.0)
        
    test = ImageDataGenerator(rescale = 1.0/255)

    tr_gen = train.flow_from_directory(os.path.join(dir,'Train'),target_size=(512,512),batch_size=8,shuffle=True)
    #va_gen = train.flow_from_directory(os.path.join(dir,'train'),target_size=(256,256),batch_size=64,shuffle=False,subset="validation")
    te_gen = test.flow_from_directory(os.path.join(dir,'Test'),target_size=(512,512),batch_size=8,shuffle=False)

    return tr_gen,te_gen


def create_new(dir : str, model_save_dir : str = "src/model/saved/covid-19"):

    test = ImageDataGenerator()
    data = test.flow_from_directory(dir,target_size=(512,512),batch_size=1, shuffle=False, class_mode=None)
    print("Success")
    steps = len(data.filenames)
    model = models.load_model(model_save_dir)

    predictions = model.predict(data,steps=steps)

    return data.filenames, predictions