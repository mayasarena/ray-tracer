#########################################################
##                CS3388 ASSIGNMENT 2                  ##
##                                                     ##
## Module Name: parametricCone.py                      ##
## Author: Maya Murad, inspired by provided classes    ##
## Date: Feb. 12 2020                                  ##
## Student Number: 250850926                           ##
##                                                     ##
## Purpose: Implement a parametric cone object         ##
## in order to display it as wiremesh with the help    ##
## of the cameraMatrix class.                          ##
#########################################################

from math import *
import numpy as np
from matrix import matrix
from parametricObject import parametricObject

class parametricCone(parametricObject):
    
    # Method __init__ initializes a parametric cone object with default parameters
    # Parameters:
    # radius: radius of the cone, defaulted to 1.0
    # height: height of the cone, defaulted to 2.0
    # color: color of the cone in rgb, defaulted to (0, 0, 0)
    # reflectance: reflectance of the cone, defaulted to (0.0, 0.0, 0.0)
    # uRange: range of u of the cone, defaulted to (0.0, 0.0)
    # vRange: range of v of the cone, defaulted to (0.0, 0.0)
    # uvDelta: uv delta, defaulted to (0.0, 0.0)
    def __init__(self, T = matrix(np.identity(4)), height = 2.0, radius = 1.0, color = (0, 0, 0), reflectance = (0.0, 0.0, 0.0), uRange = (0.0, 0.0), vRange = (0.0, 0.0), uvDelta = (0.0, 0.0)):
        super().__init__(T, color, reflectance, uRange, vRange, uvDelta)
        self.__radius = radius
        self.__height = height
    
    # Method getPoint gets the point of the cone on the viewing plane
    # Parameters:
    # u: the u coordinate
    # v : the v coordinate
    def getPoint(self, u, v):
        
        # Initializing a 4x1 matrix of ones
        __P = matrix(np.ones((4,1)))

        # Setting all non-one values in the matrix
        __P.set(0, 0, self.__radius * sin(v) * ((self.__height * (1 - u))/self.__height))
        __P.set(1, 0, self.__radius * cos(v) * ((self.__height * (1 - u))/self.__height))
        __P.set(2, 0, self.__height * u)
        return __P
    
    # Method setRadius sets the radius of the cone
    # Parameter:
    # radius: the desired radius
    def setRadius(self, radius):
        self.__radius = radius
    
    # Method getRadius returns the radius of the cone
    # Return value: __radius, the radius of the cone
    def getRadius(self):
        return self.__radius
        
    # Method setHeight sets the height of the cone
    # Parameter:
    # height: the desired height
    def setHeight(self, height):
        self.__height = height

    # Method getHeight returns the height of the cone
    # Return value: __height, the height of the cone
    def getHeight(self):
        return self.__height

