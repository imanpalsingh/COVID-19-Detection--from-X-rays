'''
Author: Imanpal Singh <imanpalsingh@gmail.com>
Location:  src.data
Date Created: 01-08-2020
Date Modified: 04-09-2020
'''

'''

Change Logs
===========

None
'''


from src.data.extract import Raw,TrainTest

if __name__ == "__main__":

    Raw("Dataset/").start(output_dir='dataset/output/')
    TrainTest('dataset/output/',train_perc=0.8).start('dataset/final/')

