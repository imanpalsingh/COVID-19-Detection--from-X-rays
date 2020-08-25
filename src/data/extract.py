'''
Author: Imanpal Singh <imanpalsingh@gmail.com>
Location:  src.Data
Date Created: 25-08-2020
Date Modified: 25-08-2020
'''

'''

Change Logs
===========

None

'''

import pandas as pd 
from tqdm import tqdm
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

    `images_only` : `bool`

    Specifies whether to save the demographics given in `path/metadata.csv` along with the images if `False` or only images if `True`

    Example
    =======

    ```
    >>>from Data.extract import Organizer
    >>>obj = Organizer(path = "dataset/")

    ```

    '''

    def __init__(self,path: str, images_only : bool = True) -> None:

    
        if not os.path.isdir(path):

            raise FileNotFoundError(f"The Directory '{path}' does not exist.")

        if not images_only:

            raise NotImplementedError("'images_only = False' is not yet supported")

        self.path = path
        self.images_only = images_only


    def start(self,output_dir: str) -> None :

        '''

        Function to start the process of copying files to `output_dir`

        Input
        =====

        `output_dir` : `str`

        Sepcifies the path to the folder in which different folders will be created based on the `finding` column inside `self.path/metadata.csv`
        and inside those newly created folders, the images will be saved

        Example
        =======

        ```
        >>>from Data.extract import Organizer
        >>>obj = Organizer(path = "dataset/")
        >>>obj.start(output_dir="dataset/output/")
        ```

        '''

        if not os.path.isdir(output_dir):

            raise FileNotFoundError(f"The Directory '{output_dir}' does not exist.")

        metadata = pd.read_csv(self.path + 'metadata.csv')
        classes = metadata['finding'].unique()
        
        for folder in classes:
            
            path = os.path.join(output_dir,folder)
            try:
                os.mkdir(path)

            except FileExistsError:
                pass

            files = metadata[metadata['finding'] == folder]['filename']
            

            for _file in files:
                
                try:
                    copyfile(self.path + '/images/' + _file, output_dir + '/' + folder + '/' + _file)

                except FileNotFoundError:

                    print(f"Warning! : Skipping {_file} as it was not found")

