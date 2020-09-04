'''
Author: Imanpal Singh <imanpalsingh@gmail.com>
Location:  src.data
Date Created: 25-08-2020
Date Modified: 01-09-2020
'''

'''

Change Logs
===========

1) 01-09-20

Added Class to allow automated splitting of training and testing data for easier keras image integration  

2) 27-08-20

Changed class name Organizer to Raw
Added class TrainValTest to split the images into folders of training and test

2) 26-08-20

Added additional metadata saving and renaming of images

'''

import pandas as pd 
import os
from shutil import copyfile
import glob
from random import shuffle

class Raw:

    '''

    For extracting different types of images from `path/images/` folder and arranging them in folders
    based on their labels in `path/metadata.csv`

    Input
    =====

    `path` : `str`

    Specifies the path of the location of the dataset. The dataset should represent the same structure as of the repository 
    `https://github.com/ieee8023/covid-chestxray-dataset` of the original dataset.

    -----------------------------------

    `images_only` : `bool`

    Specifies whether to save the demographics given in `path/metadata.csv` along with the images if `False` or only images if `True`

    -----------------------------------

    `rename_files`  : `bool`

    Specifies if the files that are being copied (images) should be renamed.
    The images will be renamed for example as  `Covid191.png`


    Example
    =======

    ```
    >>>from data.extract import Organizer
    >>>obj = Organizer(path = "dataset/")

    ```

    '''

    def __init__(self,path: str, images_only : bool = True, rename_files : bool = True) -> None:

    
        if not os.path.isdir(path):

            raise FileNotFoundError(f"The Directory '{path}' does not exist.")


        self.path = path
        self.images_only = images_only
        self.rename_files = rename_files


    def start(self,output_dir: str) -> None :

        '''

        Function to start the process of copying files to `output_dir`

        Input
        =====

        `output_dir` : `str`

        Specifies the path to the folder in which different folders will be created based on the `finding` column inside `self.path/metadata.csv`
        and inside those newly created folders, the images will be saved

        Example
        =======

        ```
        >>>from data.extract import Raw
        >>>obj = Raw(path = "dataset/")
        >>>obj.start(output_dir="dataset/output/")
        ```

        '''

        if not os.path.isdir(output_dir):

            print(f"Warning! : The Directory '{output_dir}' does not exist and has been created.")
            os.mkdir(output_dir)

        metadata = pd.read_csv(self.path + 'metadata.csv')

        classes = metadata['finding'].unique()
        

        for folder in classes:

            '''
            For each unique class given in the metadata.csv create a folder for the class if it doesn't exist

            '''
            
            path = os.path.join(output_dir,folder)
            try:
                os.mkdir(path)

            except FileExistsError:
                pass

            data = metadata[metadata['finding'] == folder]
            files = data['filename']
            locations = data['folder']


            for index, (_file,location) in enumerate(zip(files,locations)):

                '''
                For each file that belongs to the class copy it from its current position to the newly created
                folder for that class

                '''
                if self.rename_files:
                        output_filename = folder + str(index) + os.path.splitext(_file)[1]
                    
                else:
                        output_filename = _file 
                
                try:
                    
                    copyfile(self.path + '/' + location + '/' + _file, output_dir + '/' + folder + '/' + output_filename)

                except FileNotFoundError:

                    print(f"Warning! : Skipping '{_file}' as it was not found at location '{location}'")

            
            if not self.images_only:

                data.to_csv(output_dir + '/' + folder + '/' + folder + '.csv', index = False)
             

class TrainTest:

    '''
    Class for automated splitting of training and testing data into two different folders so that keras's ImageDataGenerator
    can be easily applied.

    Inputs
    ======

    `path` : `str`

    Path were class separated images are stored. This is obtained by executing the `Raw` class first on the raw dataset. 

    ------------------

    `train_perc` : `float`

    A number between 0 and 1 defining the percentage of total images to be used for training and rest for testing.

    Note :  To avoid class left out problem percentage is calculated from each class separately so that every class 
    is present in both training and test. However, still a class can be left out if the percentage is high and data is low enough

    ---------------------

    `shuffle` : `bool`

    If to randomly select images for training and testing . If set to `False` first `total length x train_perc` images/data are selected


    Example
    =======

    ```
    >>>from data.extract import TrainTest
    >>>obj = Test(path = "dataset/output/",train_perc=0.9)

    ```
    '''

    def __init__(self, path, train_perc = 0.5, shuffle = False):

        self.path = path
        self.train_perc = train_perc
        self.shuffle = shuffle
    
    def start(self,output_dir):

        '''

        Function to start the process of splitting of data into training and test set

        Input
        =====

        `output_dir` : `str`

        Specifies the path to the folder in which two folders will be created `training` and `testing` 
        and files will be copied to these two folders

        Example
        =======

        ```
        >>>from data.extract import TrainTest
        >>>obj = Test(path = "dataset/output/",train_perc=0.9)
        >>>obj.start(output_dir="dataset/final/")
        ```

        '''


        folders = os.listdir(self.path)

        if not os.path.isdir(output_dir):

            print(f"Warning! : The Directory '{output_dir}' does not exist and has been created.")
            os.mkdir(output_dir)

        try:

            os.mkdir(output_dir + '/training/')

        except FileExistsError:

            pass
        
        try:

            os.mkdir(output_dir + '/testing/')
        
        except FileExistsError:

            pass


        
        for folder in folders:

            files = os.listdir(self.path+folder)

            if self.shuffle:

                shuffle(files)

            total_count = len(files)

            training_till = int(total_count*self.train_perc)

            train_files = files[:training_till]
            test_files = files[training_till:]

            try:

                os.mkdir(output_dir + '/testing/' + folder)
        
            except FileExistsError:

                pass

            try:

                os.mkdir(output_dir + '/training/' + folder)
        
            except FileExistsError:

                pass

            for train in train_files:

                try:
                    
                    copyfile(self.path + '/' + folder + '/' + train, output_dir + '/training/' + folder + '/' + train)
                
                except FileNotFoundError:

                    print(f"Warning! : Skipping '{train}' as it was not found at location '{output_dir + '/' + folder + '/'}'")

            for test in test_files:   

                try:
                    
                    copyfile(self.path + '/' + folder + '/' + test, output_dir + '/testing/' + folder + '/' + test)
                
                except FileNotFoundError:

                    print(f"Warning! : Skipping '{train}' as it was not found at location '{output_dir + '/' + folder + '/'}'")

            