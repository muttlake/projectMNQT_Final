import numpy as np
import math

# this will return an array of interpolated values basically a scaled image
class Bicubic_Interpolation:
    M_inv = np.array([[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [-3, 3, 0, 0, -2, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [2, -2, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, -3, 3, 0, 0, -2, -1, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 2, -2, 0, 0, 1, 1, 0, 0],
                      [-3, 0, 3, 0, 0, 0, 0, 0, -2, 0, -1, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, -3, 0, 3, 0, 0, 0, 0, 0, -2, 0, -1, 0],
                      [9, -9, -9, 9, 6, 3, -6, -3, 6, -6, 3, -3, 4, 2, 2, 1],
                      [-6, 6, 6, -6, -3, -3, 3, 3, -4, 4, -2, 2, -2, -2, -1, -1],
                      [2, 0, -2, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 2, 0, -2, 0, 0, 0, 0, 0, 1, 0, 1, 0],
                      [-6, 6, 6, -6, -4, -2, 4, 2, -3, 3, -3, 3, -2, -1, -2, -1],
                      [4, -4, -4, 4, 2, 2, -2, -2, 2, -2, 2, -2, 1, 1, 1, 1]])

    def perform_scaling_interpolation(self, image, fx, fy):
        height_original = image.shape[0]
        width_original = image.shape[1]

        height_new = int(height_original * fy)
        width_new = int(width_original * fx)

        resampled_image = np.zeros((height_new, width_new), np.uint8)
        derivativeX, derivativeY, derivativeXY = self.getDerivates(image)

        for i in range(height_new):
            for j in range(width_new):
                pt1 = [int(i / fy), int(j / fx)]  # Left
                pt2, pt3, pt4 = self.getNeighbouringPoints(pt1, width_original, height_original)

                beta = self.getBeta(image, derivativeX, derivativeY, derivativeXY, pt1, pt2, pt3, pt4)
                alpha = self.getAlpha(beta)

                w = -(((j / fx) - math.floor(j / fx)) - 1)
                h = -(((i / fy) - math.floor(i / fy)) - 1)
                interpolated_intensity = self.getInterpolatedIntensity(w, h, alpha)
                resampled_image[i][j] = interpolated_intensity

        return resampled_image

    def perform_interpolation(self, w, h, image, derivativeX, derivativeY, derivativeXY, pt1, pt2, pt3, pt4):
        """ Perform Interpolation at one location"""
        # pt1 = [int(i / fy), int(j / fx)]  # Left
        # pt2, pt3, pt4 = self.getNeighbouringPoints(pt1, width_original, height_original)

        beta = self.getBetaCareful(image, derivativeX, derivativeY, derivativeXY, pt1, pt2, pt3, pt4)
        alpha = self.getAlpha(beta)

        # w = -(((j / fx) - math.floor(j / fx)) - 1)
        # h = -(((i / fy) - math.floor(i / fy)) - 1)

        interpolated_intensity = self.getInterpolatedIntensity(w, h, alpha)
        return interpolated_intensity

    def calculate_derivative_x(self, pt1, width_original, image):
        pt1_dx = 0.0
        if pt1[1] == width_original - 1 or pt1[1] == 0:
            pt1_dx = 0
        elif pt1[1] < width_original - 1 and pt1[1] > 0:
            pt1_dx = abs(image[pt1[0]][pt1[1] + 1] - image[pt1[0]][pt1[1] - 1])

        return pt1_dx

    def calculate_derivative_y(self, pt1, height_original, image):
        pt1_dy = 0.0
        if pt1[0] == height_original - 1 or pt1[0] == 0:
            pt1_dy = 0
        elif pt1[0] < height_original - 1 and pt1[0] > 0:
            pt1_dy = abs(image[pt1[0] - 1][pt1[1]] - image[pt1[0] + 1][pt1[1]])

        return pt1_dy

    def calculate_derivative_xy(self, pt1, height_original, width_original, image):
        pt1_dxdy = 0.0
        if pt1[0] == height_original - 1 or pt1[0] == 0 or pt1[1] == width_original - 1 or pt1[1] == 0:
            pt1_dxdy = 0
        elif pt1[0] < height_original - 1 and pt1[0] > 0 and pt1[1] < width_original - 1 and pt1[1] > 0:
            pt1_dxdy = abs((image[pt1[0] + 1][pt1[1] + 1] + image[pt1[0] - 1][pt1[1] - 1]) - (
                    image[pt1[0] + 1][pt1[1] - 1] + image[pt1[0] - 1][pt1[1] + 1]))

        return pt1_dxdy

    def getDerivates(self, image):
        height_original = image.shape[0]
        width_original = image.shape[1]

        derivativeX = np.zeros([height_original, width_original])
        derivativeY = np.zeros([height_original, width_original])
        derivativeXY = np.zeros([height_original, width_original])

        diminishing_factor = .01
        for i in range(height_original):
            for j in range(width_original):
                #print(i, j)
                derivativeX[i][j] = self.calculate_derivative_x([i, j], width_original, image) * diminishing_factor
                derivativeY[i][j] = self.calculate_derivative_y([i, j], height_original, image) * diminishing_factor
                derivativeXY[i][j] = self.calculate_derivative_xy([i, j], height_original, width_original, image) * diminishing_factor/2

        return derivativeX, derivativeY, derivativeXY

    def getNeighbouringPoints(self, pt1, width_original, height_original):
        pt2 = [0, 0]                                            #Interpolation Pt2
        pt3 = [0, 0]                                            #Interpolation Pt3
        pt4 = [0, 0]                                            #Interpolation Pt4

        if pt1[0] == 0 and pt1[1] == width_original - 1:  # TopRightPixel
            pt2[0] = pt1[0] + 1
            pt2[1] = pt1[1]
            pt3[0] = pt1[0]
            pt3[1] = pt1[1] - 1
            pt4[0] = pt1[0] + 1
            pt4[1] = pt1[1] - 1
        elif pt1[0] < height_original - 1 and pt1[1] == width_original - 1:  # RightMostColumn
            pt2[0] = pt1[0] + 1
            pt2[1] = pt1[1]
            pt3[0] = pt1[0]
            pt3[1] = pt1[1] - 1
            pt4[0] = pt1[0] + 1
            pt4[1] = pt1[1] - 1
        elif pt1[0] == height_original - 1 and pt1[1] < width_original - 1:  # BottomMostRow
            pt2[0] = pt1[0] - 1
            pt2[1] = pt1[1]
            pt3[0] = pt1[0]
            pt3[1] = pt1[1] + 1
            pt4[0] = pt1[0] - 1
            pt4[1] = pt1[1] + 1
        elif pt1[0] == height_original - 1 and pt1[1] == 0:  # BottomLeftPixel
            pt2[0] = pt1[0] - 1
            pt2[1] = pt1[1]
            pt3[0] = pt1[0]
            pt3[1] = pt1[1] + 1
            pt4[0] = pt1[0] - 1
            pt4[1] = pt1[1] + 1
        elif pt1[0] == height_original - 1 and pt1[1] == width_original - 1:  # BottomRightPixel
            pt2[0] = pt1[0] - 1
            pt2[1] = pt1[1]
            pt3[0] = pt1[0]
            pt3[1] = pt1[1] - 1
            pt4[0] = pt1[0] - 1
            pt4[1] = pt1[1] - 1
        elif (pt1[0] == 0 and pt1[1] == 0) or (
                pt1[0] < height_original - 1 and pt1[1] < width_original - 1):  # TopLeftPixel or any other pixel
            pt2[0] = pt1[0] + 1
            pt2[1] = pt1[1]
            pt3[0] = pt1[0]
            pt3[1] = pt1[1] + 1
            pt4[0] = pt1[0] + 1
            pt4[1] = pt1[1] + 1
        return pt2, pt3, pt4

    def getBeta(self, image, derivateX, derivateY, derivateXY, pt1, pt2, pt3, pt4):
        I11 = image[pt1[0]][pt1[1]]
        I12 = image[pt2[0]][pt2[1]]
        I21 = image[pt3[0]][pt3[1]]
        I22 = image[pt4[0]][pt4[1]]

        Ix11 = derivateX[pt1[0]][pt1[1]]
        Ix12 = derivateX[pt2[0]][pt2[1]]
        Ix21 = derivateX[pt3[0]][pt3[1]]
        Ix22 = derivateX[pt4[0]][pt4[1]]

        Iy11 = derivateY[pt1[0]][pt1[1]]
        Iy12 = derivateY[pt2[0]][pt2[1]]
        Iy21 = derivateY[pt3[0]][pt3[1]]
        Iy22 = derivateY[pt4[0]][pt4[1]]

        Ixy11 = derivateXY[pt1[0]][pt1[1]]
        Ixy12 = derivateXY[pt2[0]][pt2[1]]
        Ixy21 = derivateXY[pt3[0]][pt3[1]]
        Ixy22 = derivateXY[pt4[0]][pt4[1]]
        return np.array([I11, I12, I21, I22, Ix11, Ix21, Ix12, Ix22, Iy11, Iy21, Iy12, Iy22, Ixy11, Ixy21, Ixy12, Ixy22])

    def getBetaCareful(self, image, derivateX, derivateY, derivateXY, pt1, pt2, pt3, pt4):
        (N, M) = image.shape
        I11 = I12 = I21 = I22 = 0
        Ix11 = Ix12 = Ix21 = Ix22 = 0
        Iy11 = Iy12 = Iy21 = Iy22 = 0
        Ixy11 = Ixy12 = Ixy21 = Ixy22 = 0
        if pt1[0] < N and pt1[1] < M:
            I11 = image[pt1[0]][pt1[1]]
            Ix11 = derivateX[pt1[0]][pt1[1]]
            Iy11 = derivateY[pt1[0]][pt1[1]]
            Ixy11 = derivateXY[pt1[0]][pt1[1]]
        if pt2[0] < N and pt2[1] < M:
            I12 = image[pt2[0]][pt2[1]]
            Ix12 = derivateX[pt2[0]][pt2[1]]
            Iy12 = derivateY[pt2[0]][pt2[1]]
            Ixy12 = derivateXY[pt2[0]][pt2[1]]
        if pt3[0] < N and pt3[1] < M:
            I21 = image[pt3[0]][pt3[1]]
            Ix21 = derivateX[pt3[0]][pt3[1]]
            Iy21 = derivateY[pt3[0]][pt3[1]]
            Ixy21 = derivateXY[pt3[0]][pt3[1]]

        if pt4[0] < N and pt4[1] < M:
            I22 = image[pt4[0]][pt4[1]]
            Ix22 = derivateX[pt4[0]][pt4[1]]
            Iy22 = derivateY[pt4[0]][pt4[1]]
            Ixy22 = derivateXY[pt4[0]][pt4[1]]

        return np.array([I11, I12, I21, I22, Ix11, Ix21, Ix12, Ix22, Iy11, Iy21, Iy12, Iy22, Ixy11, Ixy21, Ixy12, Ixy22])

    def getInterpolatedIntensity(self, w, h, alpha):
        interpolated_intensity = 0
        for count in range(16):
            w_temp = math.floor(count / 4)
            h_temp = count % 4
            w_value = (1 - w) ** (w_temp)
            h_value = (1 - h) ** (h_temp)
            w_h_multiply = np.multiply(w_value, h_value)
            alpha_w_h = np.multiply(alpha[count], w_h_multiply)
            interpolated_intensity += alpha_w_h

        return interpolated_intensity

    def getAlpha(self, beta):
        return self.M_inv.dot(beta)