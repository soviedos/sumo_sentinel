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
    def desenfoque_gaussiano(imagen, ksize=(5, 5)):
        return cv2.GaussianBlur(imagen, ksize, 0)

    @staticmethod
    def filtro_morfologico(imagen, operacion, kernel_size=3):
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        return cv2.morphologyEx(imagen, operacion, kernel)