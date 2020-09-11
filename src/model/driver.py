'''
Author: Imanpal Singh <imanpalsingh@gmail.com>
Location:  src.model
Date Created: 01-08-2020
Date Modified: 12-09-2020
'''

'''

Change Logs
===========

1) 12-09-20
Added function for analysis of trained model

'''

from src.data import generators
from src.model.baseline import Convolutional
from matplotlib import pyplot as plt

def analysis(history, metrics : list =  ['loss', 'auc', 'precision', 'recall']) -> None:

    '''

    Function that plots the metrics of the model trained

    Input
    =====

    `history` : `Tensorflow trained model`

    Trained model to plot the analysis of

    ----------------------

    `metrics` : `list`

    List of metrics supported by the model and which are required to be displayed.


    Example
    ========
    ```
    >>>from model.driver import analysis
    >>>model.fit(X,y,epochs=100)
    >>>analysis(model)
    ```

    


    '''

    for n, metric in enumerate(metrics):
        name = metric.replace("_"," ").capitalize()
        plt.subplot(2,2,n+1)
        plt.plot(history.epoch,  history.history[metric], label='Train')
        plt.plot(history.epoch, history.history['val_'+metric],
                linestyle="--", label='Val')
        plt.xlabel('Epoch')
        plt.ylabel(name)
        if metric == 'loss':
            plt.ylim([0, plt.ylim()[1]])
        elif metric == 'auc':
            plt.ylim([0.8,1])
        else:
            plt.ylim([0,1])

    plt.legend()



if __name__ == "__main__":

    model = Convolutional()
    model.compile(optimizer='adam',metrics=['accuracy'],loss='categorical_crossentropy')
    train_gen,test_gen = generators.create('dataset/final/training/','dataset/final/testing/')
    
    model.fit(train_gen,steps_per_epoch=14,epochs=30)

