'''
Author: Imanpal Singh <imanpalsingh@gmail.com>
Location:  src.data
Date Created: 25-08-2020
Date Modified: 26-08-2020
'''

'''

Change Logs
===========

1) 26-08-20

Added additional metadata saving and renaming of images

'''

import pandas as pd 
import os
from shutil import copyfile

class Organizer:

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
        >>>from data.extract import Organizer
        >>>obj = Organizer(path = "dataset/")
        >>>obj.start(output_dir="dataset/output/")
        ```

        '''

        if not os.path.isdir(output_dir):

            raise FileNotFoundError(f"The Directory '{output_dir}' does not exist.")

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
             
