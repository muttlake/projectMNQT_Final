"""
Project MNQT
Interpolation class
"""

import numpy as np

class Interpolation:

    def linear_interpolation(self, pt1, pt2, unknown):
        """Computes the linear interpolation for the unknown values using pt1 and pt2
        take as input
        pt1: known point pt1 and f(pt1) or intensity value
        pt2: known point pt2 and f(pt2) or intensity value
        unknown: take and unknown location
        return the f(unknown) or intentity at unknown"""

        # Write your code for linear interpolation here
        #leftPix(30)----------unkownPix(?)---------------------rightPix(45)
        #leftX:2    ----------   dx:4     ---------------------rightX:8

        #(30*(8-4)) + (45*(4-2))  = 35
        #  (8-2)        (8-2)

        # pt1[leftX,pix]
        # pt2[rightX,pix]
        # unknown = dx

        leftX, leftPix = pt1
        rightX, rightPix = pt2

        if (leftX != rightX):
            fpart = leftPix * ((rightX - unknown) / (rightX - leftX))
            spart = rightPix * ((unknown - leftX) / (rightX - leftX))
            pix = fpart + spart
        else: #This usually occurs when you are at last column of matrix (because we dont have pix to the right)
            pix = leftPix #leftPix will equal rightPix so use any of the two

        return pix


    def bilinear_interpolation(self, pt1, pt2, pt3, pt4, unknown):
        """Computes the linear interpolation for the unknown values using pt1 and pt2
        take as input
        pt1: known point pt1 and f(pt1) or intensity value
        pt2: known point pt2 and f(pt2) or intensity value
        pt1: known point pt3 and f(pt3) or intensity value
        pt2: known point pt4 and f(pt4) or intensity value
        unknown: take and unknown location
        return the f(unknown) or intentity at unknown"""

        # Write your code for bilinear interpolation here
        # May be you can reuse or call linear interpolatio method to compute this task



        #                    _C O L S__
        #              leftX    dX    rightX
        # R      topY| q11      r1    q21
        # O        dY|          P
        # W          |
        # S   bottomY| q12      r2    q22

        #pt1[leftX, q11, q12]
        #pt2[rightX, q21, q22]
        #pt3[topY]
        #pt4[bottomY]
        #unknown[dy,dx]

        leftX, q11, q12 = pt1
        rightX, q21, q22 = pt2

        topY = pt3
        bottomY = pt4

        dy, dx = unknown

        if (rightX - leftX) != 0:
            r1 = self.linear_interpolation((leftX,q11),(rightX,q21), dx)
            r2 = self.linear_interpolation((leftX,q12),(rightX,q22), dx)
        else:
            r1 = q11
            r2 = q12

        if (bottomY - topY) != 0:
            avgPix = self.linear_interpolation((bottomY,r2), (topY,r1), dy)
        else:
            avgPix = (int(q11) + int(q12) + int(q21) + int(q22))/4

        return avgPix
