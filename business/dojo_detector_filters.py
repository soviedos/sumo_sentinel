import cv2
import numpy as np

class DojoFilters:
    @staticmethod
    def ajustar_brillo_contraste(imagen, brillo, contraste):
        return cv2.convertScaleAbs(imagen, alpha=contraste, beta=brillo)

    @staticmethod
    def filtro_hsv(imagen, lower, upper):
        hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        return cv2.bitwise_and(imagen, imagen, mask=mask)

    @staticmethod
    def a_grises(imagen):
        return cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    @staticmethod
    def binarizar(imagen, thresh):
        _, binary = cv2.threshold(imagen, thresh, 255, cv2.THRESH_BINARY)
        return binary

    @staticmethod
    def desenfoque_gaussiano(imagen, ksize):
        return cv2.GaussianBlur(imagen, ksize, 0)

    @staticmethod
    def filtro_morfologico(imagen, operacion, kernel_size):
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        return cv2.morphologyEx(imagen, operacion, kernel)

    @staticmethod
    def filtro_min_max_blancos(imagen, min_val, max_val):
        # Devuelve una máscara donde los píxeles en el rango [min_val, max_val] son blancos
        mask = cv2.inRange(imagen, min_val, max_val)
        return mask

    @staticmethod
    def ecualizacion_histograma(imagen):
        # Si la imagen es a color, convertir a YUV y ecualizar solo el canal Y
        if len(imagen.shape) == 3 and imagen.shape[2] == 3:
            yuv = cv2.cvtColor(imagen, cv2.COLOR_BGR2YUV)
            yuv[:, :, 0] = cv2.equalizeHist(yuv[:, :, 0])
            return cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)
        else:
            return cv2.equalizeHist(imagen)

    @staticmethod
    def filtro_bilateral(imagen, d=9, sigmaColor=75, sigmaSpace=75):
        return cv2.bilateralFilter(imagen, d, sigmaColor, sigmaSpace)