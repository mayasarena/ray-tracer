#########################################################
##              CS3388 ASSIGNMENT 1                    ##
##                                                     ##
## Module Name: graphicsWindow.py                      ##
## Author of drawLine method: Maya Murad               ##
## Student Number: 250850926                           ##
## Date of creation of drawLine: January 20 2020       ##
##                                                     ##
## Purpose: The purpose of this assignment was to      ##
## implement Bresenham's Line Algorithm in order to    ##
## further understand how it works.                    ##   
#########################################################

from PIL import Image

class graphicsWindow:

    def __init__(self,width=640,height=480):
        self.__mode = 'RGB'
        self.__width = width
        self.__height = height
        self.__canvas = Image.new(self.__mode,(self.__width,self.__height))
        self.__image = self.__canvas.load()

    def getWidth(self):
        return self.__width

    def getHeight(self):
        return self.__height

    def drawPixel(self,pixel,color):
        self.__image[pixel[0],pixel[1]] = color

    ## drawLine draws a line from a first pixel to the second pixel 
    ## parameters:
    ## p1 is the starting pixel
    ## p2 is the ending pixel
    ## color is the desired color of the line in RGB values
    ## output: the resulting line from p1 to p2
    def drawLine(self,p1,p2,color):
        #getting x and y coordinates of p1 and p2
        x1, y1 = p1
        x2, y2 = p2
        #calculating delta y and delta x and their absolute values
        dx = x2 - x1
        dy = y2 - y1
        dx_abs = abs(x2 - x1)
        dy_abs = abs(y2 - y1)
        #calculating error intervals
        px = (2 * dy) - dx
        py = (2 + dx) - dy

        ### LINE IS X DOMINANT ###
        if dx_abs >= dy_abs:
            #setting the variables in the case that the line is drawn left to right
            if dx >= 0:
                x = x1
                y = y1
                z = x2
            #the line is drawn right to left
            else:
                x = x2
                y = y2
                z = x1
               
            self.drawPixel((x, y), color) #drawing the first pixel

            #iterating through the rest of the line in order to draw it
            for i in range(x, z + 1):
                if i == x: #for the first pixel, we set px 
                    px = (2 * dy_abs) - dx_abs

                else:
                    if px < 0: #in this case, y is unchanged 
                        px = px + (2 * dy_abs)

                    else: #otherwise, y+1 (or y-1) is closer to y(i)
                        px = px + (2 * dy_abs) - (2 * dx_abs) #set px
                        #dealing with the different cases
                        if dx > 0 and dy > 0 or dx < 0 and dy < 0:
                            y += 1
                        else:
                            y -= 1
                        
                    x += 1
                    self.drawPixel((x, y), color) 

        ### LINE IS Y DOMINANT ###
        else:
            #line is drawn left to right
            if dy >= 0:
                x = x1
                y = y1
                z = y2
            #line is drawn right to left
            else:
                x = x2
                y = y2
                z = y1
                
            self.drawPixel((x, y), color) 
            
            #iterating through rest of line
            for i in range(y, z + 1):
                if i == y: #setting py for the first pixel
                    py = (2 * dx_abs) - dy_abs

                else:
                    if py < 0: #in this case, x is unchanged
                        py = py + (2 * dx_abs)

                    else: #x+1 (or x-1) is closer to x(i)
                        py = py + (2 * dx_abs) - (2 * dy_abs)
                        #dealing with the different cases
                        if dx > 0 and dy > 0 or dx < 0 and dy < 0:
                            x += 1
                        else:
                            x -= 1
                        
                    y += 1
                    self.drawPixel((x, y), color)

    def saveImage(self,fileName):
        self.__canvas.save(fileName)
