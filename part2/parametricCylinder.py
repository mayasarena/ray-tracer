#########################################################
##                CS3388 ASSIGNMENT 2                  ##
##                                                     ##
## Module Name: parametricCylinder.py                  ##
## Author: Maya Murad, inspired by provided classes    ##
## Date: Feb. 12 2020                                  ##
## Student Number: 250850926                           ##
##                                                     ##
## Purpose: Implement a parametric cylinder object     ##
## in order to display it as wiremesh with the help    ##
## of the cameraMatrix class.                          ##
#########################################################

from math import *
import numpy as np
from matrix import matrix
from parametricObject import parametricObject

class parametricCylinder(parametricObject):

    # Method __init__ initializes a parametric cylinder object with default parameters
    # Parameters:
    # radius: radius of the cylinder, defaulted to 1.0
    # height: height of the cylinder, defaulted to 2.0
    # color: color of the cylinder in rgb, defaulted to (0, 0, 0)
    # reflectance: reflectance of the cylinder, defaulted to (0.0, 0.0, 0.0)
    # uRange: range of u of the cylinder, defaulted to (0.0, 0.0)
    # vRange: range of v of the cylinder, defaulted to (0.0, 0.0)
    # uvDelta: uv delta, defaulted to (0.0, 0.0)
    def __init__(self, T = matrix(np.identity(4)), height = 1.0, radius = 1.0, color = (0, 0, 0), reflectance = (0.0, 0.0, 0.0), uRange = (0.0, 0.0), vRange = (0.0, 0.0), uvDelta = (0.0, 0.0)):
        super().__init__(T, color, reflectance, uRange, vRange, uvDelta)
        self.__radius = radius
        self.__height = height
    
    # Method getPoint gets the point of the cylinder on the viewing plane
    # Parameters:
    # u: the u coordinate
    # v : the v coordinate
    # Return value: __P, the point on the plane
    def getPoint(self, u, v):
        __P = matrix(np.ones((4,1)))
        __P.set(0, 0, (self.__radius * sin(v)))
        __P.set(1, 0, (self.__radius * cos(v)))
        __P.set(2, 0, self.__height * u)
        return __P

    # Method setRadius sets the radius of the cylinder
    # Parameter:
    # radius: the desired radius
    def setRadius(self, radius):
        self.__radius = radius

    # Method getRadius returns the radius of the cylinder
    # Return value: __radius, the radius of the cylinder
    def getRadius(self):
        return self.__radius
    
    # Method setHeight sets the height of the cylinder
    # Parameter:
    # height: the desired height
    def setHeight(self, height):
        self.__height = height

    # Method getHeight returns the height of the cylinder
    # Return value: __height, the height of the cylinder
    def getHeight(self):
        return self.__height

