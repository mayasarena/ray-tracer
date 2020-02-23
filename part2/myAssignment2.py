#########################################################
##                CS3388 ASSIGNMENT 2                  ##
##                                                     ##
## Module Name: cameraMatrix.py                        ##
## Name: Maya Murad                                    ##
## Student Number: 250850926                           ##
##                                                     ##
## Purpose: Implement the camera transformation        ##
## matrix in order to display parametric objects       ##
## as wiremesh.                                        ##
#########################################################

from math import *
import numpy as np
from matrix import matrix

class cameraMatrix:

    def __init__(self,UP,E,G,nearPlane=10.0,farPlane=50.0,width=640,height=480,theta=90.0):
        __Mp = self.__setMp(nearPlane,farPlane)
        __T1 = self.__setT1(nearPlane,theta,width/height)
        __S1 = self.__setS1(nearPlane,theta,width/height)
        __T2 = self.__setT2()
        __S2 = self.__setS2(width,height)
        __W2 = self.__setW2(height)

        self.__UP = UP.normalize()
        self.__N = (E - G).removeRow(3).normalize()
        self.__U = self.__UP.removeRow(3).transpose().crossProduct(self.__N.transpose()).normalize().transpose()
        self.__V = self.__N.transpose().crossProduct(self.__U.transpose()).transpose()
        self.__Mv = self.__setMv(self.__U,self.__V,self.__N,E)
        self.__C = __W2*__S2*__T2*__S1*__T1*__Mp
        self.__M = self.__C*self.__Mv
    
    # Method __setMV sets a camera viewing matrix
    # Parameters:
    # U, V, N: unit vectors of the coordinate system of the camera
    # E: position of the origin of the camera coordinate system
    # Return value: __Mv, a matrix
    # Author: Maya Murad, Feb. 12 2020
    def __setMv(self,U,V,N,E):
        
        # Initialize a 4x4 matrix of zeros
        M = matrix(np.zeros((4, 4)))
        
        # Set the U values in the matrix
        M.set(0, 0, U.get(0, 0))
        M.set(1, 0, U.get(1, 0))
        M.set(2, 0, U.get(2, 0))
        
        # Set the V values in the matrix
        M.set(0, 1, V.get(0, 0))
        M.set(1, 1, V.get(1, 0))
        M.set(2, 1, V.get(2, 0))

        # Set the N values in the matrix
        M.set(0, 2, N.get(0, 0))
        M.set(1, 2, N.get(1, 0))
        M.set(2, 2, N.get(2, 0))
        
        # Set the E values in the matrix
        M.set(0, 3, E.get(0, 0))
        M.set(1, 3, E.get(1, 0))
        M.set(2, 3, E.get(2, 0))

        # Set the value to 1 in location matrix[3][3]
        M.set(3, 3, 1)

        # Mv = M^1 so we calculate the inverse to get Mv
        __Mv = M.inverse()

        return __Mv

    # Method __setMp sets a perspective transformation matrix
    # Parameters:
    # nearPlane: the distance from the origin of the camera coordinate
    # system to the near plane
    # farPlane: the distance from the origin of the camera coordinate
    # system to the farPlane
    # Return value: __Mp, the perspective matrix
    # Author: Maya Murad, Feb. 12 2020
    def __setMp(self,nearPlane,farPlane):
        
        # Calculating a and b values which are part of the matrix 
        b = (-2 * farPlane * nearPlane)/(farPlane - nearPlane)
        a = (nearPlane + b)/nearPlane
        
        # Initializing a 4x4 matrix of zeros
        __Mp = matrix(np.zeros((4, 4)))

        # Setting the non-zero values in the Mp matrix accordingly
        __Mp.set(0, 0, nearPlane)
        __Mp.set(1, 1, nearPlane)
        __Mp.set(2, 2, a)
        __Mp.set(2, 3, b)
        __Mp.set(3, 2, -1)

        return __Mp

    # Method __setT1 sets a translation matrix for the coordinates in the viewing volume
    # Parameters:
    # nearPlane: the distance from the origin of the camera coordinate
    # system to the near plane
    # theta: the viewing angle
    # aspect: the aspect ratio
    # Author: Maya Murad, Feb. 12 2020
    def __setT1(self,nearPlane,theta,aspect):

        # Calculating t, b, r, and l values 
        t = nearPlane * tan((pi/180)*(theta/2))
        b = -1 * t
        r = aspect * t
        l = -1 * r
        
        # Initializing a 4x4 matrix of zeros
        __T1 = matrix(np.zeros((4, 4)))

        # Setting the non-zero values in the T1 matrix accordingly
        __T1.set(0, 0, 1)
        __T1.set(0, 3, (-1*(r+l))/2)
        __T1.set(1, 1, 1)
        __T1.set(1, 3, (-1*(t+b))/2)
        __T1.set(2, 2, 1)
        __T1.set(3, 3, 1)

        return __T1

    # Method __setT1 sets a scaling matrix for the coordinates in the viewing volume
    # Parameters:
    # nearPlane: the distance from the origin of the camera coordinate
    # system to the near plane
    # theta: the viewing angle
    # aspect: the aspect ratio
    # Author: Maya Murad, Feb. 12 2020
    def __setS1(self,nearPlane,theta,aspect):
        
        # Calculating t, b, r, and l values
        t = nearPlane * tan((pi/180)*(theta/2))
        b = -1 * t
        r = aspect * t
        l = -1 * r

        # Initializing a 4x4 matrix of zeros
        __S1 = matrix(np.zeros((4,4)))

        # Setting the non-zero valyes in the S1 matrix accordingly
        __S1.set(0, 0, 2/(r-l))
        __S1.set(1, 1, 2/(t-b))
        __S1.set(2, 2, 1)
        __S1.set(3, 3, 1)

        return __S1

    # Method __setT2 sets a translation matrix for the coordinates from the warped
    # viewing volume
    # Author: Maya Murad, Feb. 12 2020
    def __setT2(self):

        # Initializing a 4x4 matrix of zeros
        __T2 = matrix(np.zeros((4,4)))

        # Setting the non-zero values in the T2 matrix
        __T2.set(0, 0, 1)
        __T2.set(0, 3, 1)
        __T2.set(1, 1, 1)
        __T2.set(1, 3, 1)
        __T2.set(2, 2, 1)
        __T2.set(3, 3, 1)

        return __T2

    # Method __setS2 sets a scaling matrix for the coordinates from the warped
    # viewing volume
    # Parameters:
    # width: width of the viewing space
    # height: height of the viewing space
    # Author: Maya Murad, Feb. 12 2020
    def __setS2(self,width,height):
        
        # Initializing a 4x4 matrix of zeros
        __S2 = matrix(np.zeros((4, 4)))

        # Setting the non-zero values in the S2 matrix
        __S2.set(0, 0, width/2)
        __S2.set(1, 1, height/2)
        __S2.set(2, 2, 1)
        __S2.set(3, 3, 1)

        return __S2
    
    # Method __setW2 sets a transformation matrix for the coordinates from the warped
    # viewing volume
    # Parameters:
    # height: height of the viewing space
    # Author: Maya Murad, Feb. 12 2020
    def __setW2(self,height):
        
        # Initializing a 4x4 matrix of zeros
        __W2 = matrix(np.zeros((4, 4)))

        # Setting the non-zero values in the W2 matrix
        __W2.set(0, 0, 1)
        __W2.set(1, 1, -1)
        __W2.set(1, 3, height)
        __W2.set(2, 2, 1)
        __W2.set(3, 3, 1)
 
        return __W2

    def worldToViewingCoordinates(self,P):
        return self.__Mv*P

    def viewingToImageCoordinates(self,P):
        return self.__C*P

    def imageToPixelCoordinates(self,P):
        return P.scalarMultiply(1.0/P.get(3,0))

    def worldToImageCoordinates(self,P):
        return self.__M*P

    def worldToPixelCoordinates(self,P):
        return self.__M*P.scalarMultiply(1.0/(self.__M*P).get(3,0))

    def getUP(self):
        return self.__UP

    def getU(self):
        return self.__U

    def getV(self):
        return self.__V

    def getN(self):
        return self.__N

    def getMv(self):
        return self.__Mv

    def getC(self):
        return self.__C

    def getM(self):
        return self.__M

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



