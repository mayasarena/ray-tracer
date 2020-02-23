#########################################################
##                CS3388 ASSIGNMENT 2                  ##
##                                                     ##
## Module Name: parametricCircle.py                    ##
## Author: Maya Murad, inspired by provided classes    ##
## Date: Feb. 12 2020                                  ##
## Student Number: 250850926                           ##
##                                                     ##
## Purpose: Implement a parametric circle object       ##
## in order to display it as wiremesh with the help    ##
## of the cameraMatrix class.                          ##
#########################################################

from math import *
import numpy as np
from matrix import matrix
from parametricObject import parametricObject

class parametricCircle(parametricObject):
   
    # Method __init__ initializes a parametric circle object with default parameters
    # Parameters:
    # radius: radius of the circle, defaulted to 1.0
    # color: color of the circle in rgb, defaulted to (0, 0, 0)
    # reflectance: reflectance of the circle, defaulted to (0.0, 0.0, 0.0)
    # uRange: range of u of the circle, defaulted to (0.0, 0.0)
    # vRange: range of v of the circle, defaulted to (0.0, 0.0)
    # uvDelta: uv delta, defaulted to (0.0, 0.0)
    def __init__(self, T = matrix(np.identity(4)), radius = 1.0, color = (0, 0, 0), reflectance = (0.0, 0.0, 0.0), uRange = (0.0, 0.0), vRange = (0.0, 0.0), uvDelta = (0.0, 0.0)):
        super().__init__(T, color, reflectance, uRange, vRange, uvDelta)
        self.__radius = radius
    
    # Method getPoint gets the point of the circle on the viewing plane
    # Parameters:
    # u: the u coordinate
    # v : the v coordinate
    # Return value: __P, the point on the plane
    def getPoint(self, u, v):
        
        # Initializing a 4x1 matrix of ones
        __P = matrix(np.ones((4,1)))

        # Setting all non-one values in the matrix
        __P.set(0, 0, self.__radius * u * cos(v))
        __P.set(1, 0, self.__radius * u * sin(v))
        __P.set(2, 0, 0)
        return __P

    # Method setRadius sets the radius of the circle
    # Parameter:
    # radius: the desired radius
    def setRadius(self, radius):
        self.__radius = radius

    # Method getRadius returns the radius of the circle
    # Return value: __radius, the radius of the circle
    def getRadius(self):
        return self.__radius
    

