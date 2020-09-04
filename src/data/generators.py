'''
Author: Imanpal Singh <imanpalsingh@gmail.com>
Location:  src.data
Date Created: 27-08-2020
Date Modified: 04-09-2020
'''

'''

Change Logs
===========

None

'''


from typing import Union
from tensorflow.keras.preprocessing.image import ImageDataGenerator

def create(train_dir : str, test_dir : str) -> Union[ImageDataGenerator,ImageDataGenerator] :

    '''

    Function that returns test and training keras image generators extracted from the `train_dir` and `test_dir` respectively

    Input
    =====

    `train_dir` : `str`
    
    The direcotry which contains the training images (seperated by class as folders)

    ---------------

    `test_dir` : `str`

    The directory which contains the test set images (seperated by class as folders)

    Example
    ========
    ```
    >>>from data.generators import create
    >>>train_gen,test_gen = create('dataset/training/','dataset/testing')

    ```
    '''
    train_gen = ImageDataGenerator(rescale=1./255,shear_range=0.2,zoom_range=0.25,horizontal_flip=True)
    test_gen = ImageDataGenerator(rescale=1./255)

    train_generator = train_gen.flow_from_directory(train_dir, target_size = (150,150), batch_size = 24, shuffle=True)
    test_generator = test_gen.flow_from_directory(test_dir, target_size = (150,150), batch_size = 24, shuffle=False)

    return train_generator,test_generator
        









        




