'''
Author: Imanpal Singh <imanpalsingh@gmail.com>
Location:  src.utils
Date Created: 26-08-2020
Date Modified: 26-08-2020
'''

'''

Change Logs
===========

None

'''

def X_y_check(X,y):

    '''
    Function to check if Feature Matrix `X` and vector of prediction `y` are of correct shapes

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
    >>>from src.utils import checks
    >>>checks.X_y_check(X,y)

    ```
    '''

    if X.ndim == 1:

        raise AssertionError("The dimensions should be > 1 ")

    if X.shape[0] != y.shape[0] :

        raise AssertionError(f"The dimensions are not compatible  {X.shape[0]} != {y.shape[0]} ")


def X_XTest_check(X,XTest):

    '''
    Function to check if Feature Matrix `X` and Test set `XTest` are of correct shapes

    Inputs
    ======

    `X` : `numpy.ndarray`
    Numpy array as the Feature matrix

    -----------------

    `XTest` : `numpy.ndarray`
    Numpy array as the Test set

    
    Example
    =======

    ```
    >>>from src.utils import checks
    >>>checks.X_XTest_check(X,y)

    ```

    '''

    if XTest.shape[1:] != X.shape[1:] :
        raise AssertionError(f"The dimensions are not compatible {XTest.shape[1:]} != {X.shape[1:]} ")