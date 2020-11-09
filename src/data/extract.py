'''
File name : extract.py
Location : src.data
Author : Imanpal Singh <imanpalsingh@gmail.com>
'''

'''
Change log:

04-11-20 :

        1) Converted into binary classification task, only two folders will be created
        Covid-19 and Safe


03-11-20 : 

        1) Removed classes and organized into functions

'''

import pandas as pd 
import pathlib
import os
from shutil import copyfile
from random import shuffle


def class_wise(input_dir : str = 'src/dataset/input/' , output_dir : str = 'src/dataset/classwise/', warnings : str = False) -> None :

    '''

    Function to extract raw images from the covid-19 dataset and organize them on the basis of class they belong to.
    The dataset used is https://github.com/ieee8023/covid-chestxray-dataset and should be used without any modification to the
    file organization

    Input
    =====

    `input_dir` : directory to the repository of dataset

    `output_dir` : directory where the organized and extracted images will be saved 

    `warnings` : wether to display warning on file copy error or file doesn't exists as specified in output_dir/metadata.csv

    '''

    metadata = pd.read_csv(input_dir + 'metadata.csv')
    X_ray_data = metadata[(metadata['modality'] == 'X-ray') & (metadata['view'] != 'L')]

    pathlib.Path(output_dir).mkdir(parents=True,exist_ok=True)
    pathlib.Path(os.path.join(output_dir,'Covid-19')).mkdir(exist_ok=True)
    pathlib.Path(os.path.join(output_dir,'Safe')).mkdir(exist_ok=True)
    
    for row in X_ray_data.itertuples():

        try :
            
            if 'COVID-19' in row.finding:
                
                copyfile(os.path.join(input_dir,row.folder,row.filename), os.path.join(output_dir,'Covid-19',row.filename))

            elif 'No Finding' in row.finding :
                
                copyfile(os.path.join(input_dir,row.folder,row.filename), os.path.join(output_dir,'Safe',row.filename))

        except FileNotFoundError:

            if warnings:

                print(f"Warning! '{row.filename}' was not available locally.")
        except:

            if warnings:

                print("Error : Unknown error occurred while trying to copy file. Aborting")     


def train_test_wise(input_dir : str = "src/dataset/classwise/", output_dir : str = "src/dataset/traintest/" , train_perc = 0.5, shuffle_files = True):
    
    '''
    Function to split the classwise organized data into train and test

    Input
    =====

    `input_dir` : direcotry containing class wise organized dataset

    `output_dir` : directory to contain the train and test split of dataset

    `train_perc` : the percentage of dataset to copy into the training folder. Rest will be copied to testing folder

    `shuffle_file` : if to shuffle files while selecting them for training or testing folder. If set to `False`, always the 
    first `train_perc`% of images will be selected for training

    '''
    folders = os.listdir(input_dir)
    
    pathlib.Path(output_dir).mkdir(parents=True,exist_ok=True)
    pathlib.Path(os.path.join(output_dir,'Train')).mkdir(exist_ok=True)
    pathlib.Path(os.path.join(output_dir,'Test')).mkdir(exist_ok=True)
   
    for folder in folders:

        files = os.listdir(os.path.join(input_dir,folder))

        if shuffle_files:

            shuffle(files)

        total_count = len(files)

        training_till = int(total_count*train_perc)

        train_files = files[:training_till]
        test_files = files[training_till:]

        pathlib.Path(os.path.join(output_dir,'train',folder)).mkdir(exist_ok=True)
        pathlib.Path(os.path.join(output_dir,'test',folder)).mkdir(exist_ok=True)
        
        for train in train_files:

            try:
                
                copyfile(os.path.join(input_dir, folder, train), os.path.join(output_dir, 'train', folder, train))
            
            except FileNotFoundError:

                print(f"Warning! : Skipping '{train}' as it was not found at location '{output_dir + '/' + folder + '/'}'")

        for test in test_files:   

            try:
                
                copyfile(os.path.join(input_dir, folder, test), os.path.join(output_dir, 'test', folder, test))
            
            except FileNotFoundError:

                print(f"Warning! : Skipping '{train}' as it was not found at location '{output_dir + '/' + folder + '/'}'")



if __name__ == "__main__":

    #class_wise()
    train_test_wise(train_perc=0.5)