#########################################
##         CS3388 ASSIGNMENT 4         ##
##                                     ##
## Module Name: cameraMatrix.py        ##
## Name: Maya Murad                    ##
## Student Number: 250850926           ##
##                                     ##
## Purpose: Implement                  ##
## minimumIntersection                 ##
#########################################

import operator
from math import *
import numpy as np
from matrix import matrix
from operator import itemgetter

class cameraMatrix:

    def __init__(self,window,UP,E,G,nearPlane=10.0,farPlane=50.0,theta=90.0):
        self.__UP = UP.normalize()
        self.__E = E
        self.__G = G
        self.__np = nearPlane
        self.__fp = farPlane
        self.__width = window.getWidth()
        self.__height = window.getHeight()
        self.__theta = theta
        self.__aspect = self.__width/self.__height
        self.__npHeight = self.__np*(pi/180.0*self.__theta/2.0)
        self.__npWidth = self.__npHeight*self.__aspect

        Mp = self.__setMp(self.__np,farPlane)
        T1 = self.__setT1(self.__np,self.__theta,self.__aspect)
        S1 = self.__setS1(self.__np,self.__theta,self.__aspect)
        T2 = self.__setT2()
        S2 = self.__setS2(self.__width,self.__height)
        W2 = self.__setW2(self.__height)

        self.__N = (self.__E - self.__G).removeRow(3).normalize()
        self.__U = self.__UP.removeRow(3).crossProduct(self.__N).normalize()
        self.__V = self.__N.crossProduct(self.__U)

        self.__Mv = self.__setMv(self.__U,self.__V,self.__N,self.__E)
        self.__C = W2*S2*T2*S1*T1*Mp
        self.__M = self.__C*self.__Mv

    def __setMv(self,U,V,N,E):
        Mv = matrix(np.identity(4))
        Mv.set(0,0,U.get(0,0))
        Mv.set(0,1,U.get(1,0))
        Mv.set(0,2,U.get(2,0))
        Mv.set(0,3,-E.removeRow(3).dotProduct(U))

        Mv.set(1,0,V.get(0,0))
        Mv.set(1,1,V.get(1,0))
        Mv.set(1,2,V.get(2,0))
        Mv.set(1,3,-E.removeRow(3).dotProduct(V))

        Mv.set(2,0,N.get(0,0))
        Mv.set(2,1,N.get(1,0))
        Mv.set(2,2,N.get(2,0))
        Mv.set(2,3,-E.removeRow(3).dotProduct(N))
        return Mv

    def __setMp(self,nearPlane,farPlane):
        Mp = matrix(np.identity(4))
        Mp.set(0,0,nearPlane)
        Mp.set(1,1,nearPlane)
        Mp.set(2,2,-(farPlane+nearPlane)/(farPlane-nearPlane))
        Mp.set(2,3,-2.0*(farPlane*nearPlane)/(farPlane-nearPlane))
        Mp.set(3,2,-1.0)
        Mp.set(3,3,0.0)
        return Mp

    def __setT1(self,nearPlane,theta,aspect):
        top = nearPlane*tan(pi/180.0*theta/2.0)
        right = aspect*top
        bottom = -top
        left = -right
        T1 = matrix(np.identity(4))
        T1.set(0,3,-(right+left)/2.0)
        T1.set(1,3,-(top+bottom)/2.0)
        return T1

    def __setS1(self,nearPlane,theta,aspect):
        top = nearPlane*tan(pi/180.0*theta/2.0)
        right = aspect*top
        bottom = -top
        left = -right
        S1 = matrix(np.identity(4))
        S1.set(0,0,2.0/(right-left))
        S1.set(1,1,2.0/(top-bottom))
        return S1

    def __setT2(self):
        T2 = matrix(np.identity(4))
        T2.set(0,3,1.0)
        T2.set(1,3,1.0)
        return T2

    def __setS2(self,width,height):
        S2 = matrix(np.identity(4))
        S2.set(0,0,width/2.0)
        S2.set(1,1,height/2.0)
        return S2

    def __setW2(self,height):
        W2 = matrix(np.identity(4))
        W2.set(1,1,-1.0)
        W2.set(1,3,height)
        return W2

    def getRay(self,window,i,j):
        a = -self.__np
        b = self.__npWidth*(2.0*i/window.getWidth() - 1.0)
        c = self.__npHeight*(2.0*(window.getHeight() - (j+1))/window.getHeight() - 1.0)
        return (self.__N.scalarMultiply(a) + self.__U.scalarMultiply(b) + self.__V.scalarMultiply(c)).insertRow(3,0.0)

    # Method minimumIntersection returns the minimum intersection point between ray and objects of the scene
    # Parameters:
    # direction: vector describing the direction of the ray
    # objectList: list of the objects composing the scene
    # Return value:
    # A list of tuples (k, t0) where k is the position in the list of an object
    # that the ray intersects, and t0 is the minimum t-value of the intersection
    # the ray makes with the object. This list is sorted in increasing order of
    # t-values
    # Author: Maya Murad, April 3 2020
    def minimumIntersection(self,direction,objectList):
        intersectionList = [] # Initialize empty intersection list
        cameraPosition = self.__E # Get the camera position
        for object in objectList: # Iterate through object list and find the intersections
            M = object.getT().inverse()
            Te = M*cameraPosition
            Td = M*direction
            t0 = object.intersection(Te, Td)
            if t0 != -1.0:
                intersectionList.append(tuple((object, t0)))
        return sorted(intersectionList, key = itemgetter(1)) # Sort the list and return

    def worldToViewingCoordinates(self,P):
        return self.__Mv*P

    def worldToImageCoordinates(self,P):
        return self.__M*P

    def worldToPixelCoordinates(self,P):
        return self.__M*P.scalarMultiply(1.0/(self.__M*P).get(3,0))

    def viewingToImageCoordinates(self,P):
        return self.__C*P

    def viewingToPixelCoordinates(self,P):
        return self.__C*P.scalarMultiply(1.0/(self.__C*P).get(3,0))

    def imageToPixelCoordinates(self,P):
        return P.scalarMultiply(1.0/P.get(3,0))

    def getUP(self):
        return self.__UP

    def getU(self):
        return self.__U

    def getV(self):
        return self.__V

    def getN(self):
        return self.__N

    def getE(self):
        return self.__E

    def getG(self):
        return self.__G

    def getMv(self):
        return self.__Mv

    def getC(self):
        return self.__C

    def getM(self):
        return self.__M

    def getNp(self):
        return self.__np

    def getFp(self):
        return self.__fp

    def getTheta(self):
        return self.__theta

    def getAspect(self):
        return self.__aspect

    def getWidth(self):
        return self.__width

    def getHeight(self):
        return self.__height

    def getNpHeight(self):
        return self.__npHeight

    def getNpWidth(self):
        return self.__npWidth

#########################################
##         CS3388 ASSIGNMENT 4         ##
##                                     ##
## Module Name: shader.py              ##
## Name: Maya Murad                    ##
## Student Number: 250850926           ##
##                                     ## 
## Purpose: Compute shadows generated  ##
## by objects.                         ##
#########################################

import numpy as np

class shader:

    # Method __shadowed determines if a particular pixel
    # is in the shadow of other objects or itself
    # Parameters:
    # object: the object in which there is an intersection with
    # I: intersection point 
    # S: vector from intersection point to light source
    # objectList: list of objects composing the scene
    # Return value:
    # True or False, whether the pixel is shaded or not
    # Author: Maya Murad, April 3 2020
    def __shadowed(self,object,I,S,objectList):
        
        e = 0.001
        M = object.getT()
        I = M*(I+(S.scalarMultiply(e))) # Detaching intersection point from its surface and transforming it to world coordinates
        S = M*S # Transforming S into world coordinates
        for other_object in objectList:
            M_inv = other_object.getT().inverse()
            other_I = M_inv*I # Transform intersection point into the generic coordinates of the object
            other_S = M_inv*S # Transform vector to the light source into generic coordinates of the object
            if other_object.intersection(other_I, other_S) != -1.0:
                return True

        return False

    # Constructor computes the shaded color for pixel (i, j) 
    # Parameters:
    # intersection: first (k, t0) tuple from the intersection list
    # direction: vector describing the direction of the ray
    # objectList: list of objects composing the scene
    # light: lightSource object
    # Author: Maya Murad, April 3 2020
    def __init__(self,intersection,direction,camera,objectList,light):

        object = intersection[0]
        t0 = intersection[1]
        M = object.getT().inverse() # Inverse of object matrix
        Ts = M*light.getPosition() # Light position transformed with M^-1
        Te = M*camera.getE() # Camera position (transforming the ray)
        Td = M*direction # Direction (transforming the ray)
        I = Te+(Td.scalarMultiply(t0)) # Intersection point calculation
        S = (Ts-I).normalize() # Vector from intersection point to light source
        N = object.normalVector(I) # Getting the normal vector
        R = -S + (N*S.scalarMultiply(2).transpose())*N # Specular reflection vector
        V = (Te-I).normalize() # Vector to center of projection
        Id = max(N.dotProduct(S), 0)
        Is = max(R.dotProduct(V), 0)
        r = object.getReflectance() # Reflectance
        c = object.getColor() # Color
        Li = light.getIntensity() # Light intensity
        
        if not self.__shadowed(object, I, S, objectList): # Check if shaded
            f = r[0] + (r[1]*Id) + (r[2]*(Is**r[3]))
        else:
            f = r[0]
        
        self.__color = (int(c[0]*Li[0]*f), int(c[1]*Li[1]*f), int(c[2]*Li[2]*f)) # Get color
        
    def getShade(self):
        return self.__color

