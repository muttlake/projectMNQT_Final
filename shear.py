"""
Project MNQT
Shear class
"""

import math
import numpy as np

from Bicubic_Interpolation import Bicubic_Interpolation
from Interpolation import Interpolation
from Reflection import Reflection

class Shear:
    """ Shear class to displace image horizontally or vertically proportionally to its distance from the origin """
    
    def shear(self, image, m, direction, interpolation):
        """ Calls the appropriate function to shear the image based on the interpolation method """
        
        m = float(m)
        is_horizontal = direction == "Horizontal"
        is_m_negative = m < 0
        reflector = Reflection()
        
        # shears vertically by default, if horizontal just rotate by 90 then rotate back after
        if is_horizontal:
            image = reflector.reflectOnAxisY(image).T
            
        # if m is negative, flip image to set the origin properly then flip back after
        if is_m_negative:
            image = reflector.reflectOnAxisY(image)
            m = -m
            
        if interpolation == 'Bilinear':
            new_image = self.shear_bilinear(image, m)
            
        elif interpolation == 'Bicubic':
            new_image = self.shear_bicubic(image, m)
            
        else: # default to nearest neighbor
            new_image = self.shear_nearest_neighbor(image, m)
            
        # flip back if necessary
        if is_m_negative:
            new_image = reflector.reflectOnAxisY(new_image)
        
        # rotate back if necessary
        if is_horizontal:
            new_image = reflector.reflectOnAxisY(new_image.T)
        
        return new_image
        
    def shear_nearest_neighbor(self, image, m):
        
        rows, cols = image.shape
        new_rows = int(rows + abs(m)*cols)
        new_image = np.zeros((new_rows, cols))
        
        for i in range(new_rows):
            for j in range(cols):
                # y' = y + m*x -> y = y' - m*x 
                y = int(i - m*j)
                
                if y < 0 or y >= rows:
                    new_image[i,j] = 0
                else:
                    new_image[i,j] = image[y, j]
        
        return new_image
        
    def shear_bilinear(self, image, m):
        
        interpol = Interpolation()
        
        rows, cols = image.shape
        new_rows = int(rows + abs(m)*cols)
        new_image = np.zeros((new_rows, cols))
        
        for i in range(new_rows):
            for j in range(cols):
                # x' = x + m*y -> x = x' - m*y 
                y = i - m*j
                
                if int(y) < 0 or int(y) >= rows:
                    new_image[i,j] = 0
                else:
                    # find 4 nearest neighbors
                    # ex: x = 20.5, y = 33.3 -> x1 = 20, x2 = 21, y1 = 33, y2 = 34
                    y1 = math.floor(y)
                    y2 = math.ceil(y)
                    if y2 >= rows:
                        y2 = rows - 1
                    x = x1 = x2 = j
                
                    # interpolate

                                                #          _C O L S__
                                                #           x1     dX     x2
                    q11 = image[y1,x1]          #R      y1| q11    r1    q12
                    q12 = image[y1,x2]          #O      dY|        P
                    q21 = image[y2,x1]          #W        |
                    q22 = image[y2,x2]          #S      y2| q21    r2    q22

                    new_image[i, j] = np.round(interpol.bilinear_interpolation((x1, q11, q12), (x2, q21, q22), y2, y1, (x, y)))
        
        return new_image
        
    def shear_bicubic(self, image, m):
        
        interpol = Bicubic_Interpolation()
        derivativeX, derivativeY, derivativeXY = interpol.getDerivates(image)
        
        rows, cols = image.shape
        new_rows = int(rows + m*cols)
        new_image = np.zeros((new_rows, cols))
        
        for i in range(new_rows):
            for j in range(cols):
                # x' = x + m*y -> x = x' - m*y 
                y = i - m*j
                
                if int(y) < 0 or int(y) >= rows:
                    new_image[i,j] = 0
                else:
                    # find 4 nearest neighbors
                    # ex: x = 20.5, y = 33.3 -> x1 = 20, x2 = 21, y1 = 33, y2 = 34
                    y1 = math.floor(y)
                    y2 = math.ceil(y)
                    if y2 >= rows:
                        y2 = rows - 1
                    x = x1 = x2 = j
                
                    # interpolate

                                            #          _C O L S__
                                            #           x1     dX     x2
                    q11 = (y1,x1)           #R      y1| q11    r1    q12
                    q12 = (y1,x2)           #O      dY|        P
                    q21 = (y2,x1)           #W        |
                    q22 = (y2,x2)           #S      y2| q21    r2    q22
                        
                    h  = -((x - math.floor(x)) - 1)
                    w  = -((y - math.floor(y)) - 1)
                    
                    new_image[i, j] = np.round(interpol.perform_interpolation(w, h, image, derivativeX, derivativeY, derivativeXY, q11, q12, q21, q22))
        
        return new_image
