"""
Project MNQT
Translate class
"""

import numpy as np

class Translate:
    """ Translate class to move an image off to the side in x or y """
    
    def translate(self, image, x_translation, y_translation):
        
        rows, cols = image.shape
        x_translation = int(x_translation)
        y_translation = int(y_translation)
        
        left_pad = 0
        right_pad = 0
        top_pad = 0
        bottom_pad = 0
        if x_translation > 0:
            left_pad = x_translation
        else:
            right_pad = -x_translation
        if y_translation > 0:
            top_pad = y_translation
        else:
            bottom_pad = -y_translation
        
        return np.pad(image, ((top_pad, bottom_pad),(left_pad, right_pad)), mode='constant')[bottom_pad:cols+bottom_pad, right_pad:rows+right_pad]
