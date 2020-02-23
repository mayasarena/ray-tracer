#########################################################
##                CS3388 ASSIGNMENT 2                  ##
##                                                     ##
## Module Name: parametricPlane.py                     ##
## Author: Maya Murad, inspired by provided classes    ##
## Date: Feb. 12 2020                                  ##
## Student Number: 250850926                           ##
##                                                     ##
## Purpose: Implement a parametric plane object        ##
## in order to display it as wiremesh with the help    ##
## of the cameraMatrix class.                          ##
#########################################################

from math import *
import numpy as np
from matrix import matrix
from parametricObject import parametricObject

class parametricPlane(parametricObject):
      
    # Method __init__ initializes a parametric plane object with default parameters
    # Parameters:
    # width: width of the plane, defaulted to 1.0
    # height: height of the plane, defaulted to 1.0
    # color: color of the plane in rgb, defaulted to (0, 0, 0)
    # reflectance: reflectance of the plane, defaulted to (0.0, 0.0, 0.0)
    # uRange: range of u of the plane, defaulted to (0.0, 0.0)
    # vRange: range of v of the plane, defaulted to (0.0, 0.0)
    # uvDelta: uv delta, defaulted to (0.0, 0.0)
    def __init__(self, T = matrix(np.identity(4)), width = 1.0, height = 1.0, color = (0, 0, 0), reflectance = (0.0, 0.0, 0.0), uRange = (0.0, 0.0), vRange = (0.0, 0.0), uvDelta = (0.0, 0.0)):
        super().__init__(T, color, reflectance, uRange, vRange, uvDelta)
        self.__width = width
        self.__height = height
    
    # Method getPoint gets the point of the plane on the viewing plane
    # Parameters:
    # u: the u coordinate
    # v : the v coordinate
    # Return value: __P, the point on the plane
    def getPoint(self, u, v):

        # Initializing a 4x1 matrix of one
        __P = matrix(np.ones((4,1)))

        # Setting all non-one values in the matrix
        __P.set(0, 0, self.__width * u)
        __P.set(1, 0, self.__height * v)
        __P.set(2, 0, 0)
        return __P
    
    # Method setWidth sets the width of the plane
    # Parameter:
    # width: the desired width
    def setWidth(self, width):
        self.__width = width

    # Method getWidth returns the width of the plane
    # Return value: __width, the width of the plane
    def getWidth(self):
        return self.__width
    
    # Method setHeight sets the height of the plane
    # Parameter:
    # height: the desired height
    def setHeight(self, height):
        self.__height = height

    # Method getHeight returns the height of the plane
    # Return value: __height, the height of the plane
    def getHeight(self):
        return self.__height

