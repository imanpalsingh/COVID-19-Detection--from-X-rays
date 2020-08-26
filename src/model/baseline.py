'''
Author: Imanpal Singh <imanpalsingh@gmail.com>
Location:  src.model
Date Created: 26-08-2020
Date Modified: 26-08-2020
'''

'''

Change Logs
===========

None

'''

import numpy as np
from src.utils import checks
from tensorflow import keras


class Random:

    '''
    Random prediction generator

    Inputs
    ======

    `X` : `numpy.ndarray`
    Numpy array as the Feature matrix

    -----------------

    `y` : `numpy.ndarray`
    Numpy array as the Vector of prediction

    Example
    =======

    ```
    >>>from src.model.baseline import Random
    >>>clf = Random(X,y)

    ```
    '''

    def __init__(self, X, y) -> None :
        
        checks.X_y_check(X,y)

        self.X = X
        self.y = y


    def predict(self, XTest) -> list :

        '''
        Function to return a random prediction list, the list dimensions will be calculated using `XTest` and `y`

        Inputs
        ======

        `XTest` : `numpy.ndarray`
        Numpy array as the Test set

        Example
        =======

        ```
        >>>from src.model.baseline import Random
        >>>clf = Random(X,y)
        >>>clf.predict(XTest)

        ```

        '''

        checks.X_XTest_check(self.X,XTest)

        return np.random.rand(XTest[0].ndim,self.y.ndim)


class ClassicalML:

    '''
    Providing predictions from ML related algorithms. This class accepts only scikit-learn formatted algorithms
    having `fit` and `predict` functions

    Inputs
    ======
    
    `X` : `numpy.ndarray`
    Numpy array as the Feature matrix

    -----------------

    `y` : `numpy.ndarray`
    Numpy array as the Vector of prediction

    ---------------------

    `classifier` : sklearn's classifier
    Any valid scikit-learn's classifier containing `fit` and `predict` functions

    Example
    =======

    ```
    >>>from src.model.baseline import ClassicalML
    >>>from sklearn.linear_model import LogisticRegression
    >>>log_reg = LogisticRegression()
    >>>clf = ClassicalML(X,y,log)

    ```

    '''

    def __init__(self, X, y, classifier) -> None:

        checks.X_y_check(X,y)

        self.X = X
        self.y = y
        self.classifier = classifier
        self.classifier.fit(X,y)
    
    def predict(self,XTest) -> list:

        '''
        Function to return a predictions done by the `classifier` on `XTest`

        Inputs
        ======

        `XTest` : `numpy.ndarray`
        Numpy array as the Test set

        Example
        =======

        ```
        >>>from src.model.baseline import ClassicalML
        >>>from sklearn.linear_model import LogisticRegression
        >>>log_reg = LogisticRegression()
        >>>clf = ClassicalML(X,y,log)
        >>>clf.predict(XTest)

        ```
        '''


        checks.X_XTest_check(self.X,XTest)

        return self.classifier.predict(XTest)


class Convolutional(keras.Model):

    '''
    Simple Baseline Convolutional containing 1 convolutional layer and 1 Dense layer.

    Important : Model is not fit in this class, it is returned

    Inputs
    ======

    None

    Example
    =======

    ```

    >>>from src.model.baseline import Convolutional
    >>>model = Convolutional()
    >>>model.fit(generator)

    ```

    '''
    def __init__(self):

        super(Convolutional,self).__init__()
        self.input1 = keras.layers.InputLayer(input_shape=(13,13,3))
        self.conv = keras.layers.Conv2D(64,(4,4),activation='relu')
        self.maxpool = keras.layers.MaxPool2D((4,4))
        self.flatten = keras.layers.Flatten()
        self.dense = keras.layers.Dense(2,activation='sigmoid')
    
    def call(self,input):

        x = self.input1(input)
        x = self.conv(x)
        x = self.maxpool(x)
        x = self.flatten(x)
        return self.dense(x)
