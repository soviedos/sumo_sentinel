import cv2
import numpy as np
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config')))
import config as cfg

def detectar_dojo_canny(frame):
    """
    Detecta círculos en la imagen usando Canny y encuentra el segundo círculo más grande.
    Devuelve:
    - imagen de resultado (BGR) con los círculos dibujados
    - centro del dojo (x, y) o None
    - radio del dojo o None
    - contorno más grande
    - centro y radio del segundo círculo más grande (o None)
    """
    # Convertir a escala de grises si es necesario
    if len(frame.shape) == 3:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    else:
        gray = frame.copy()

    # 1. Aplicar Canny
    edges = cv2.Canny(gray, cfg.LOWER_THRESHOLD, cfg.UPPER_THRESHOLD)

    # 2. Encontrar contornos
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    mask_vis = cv2.cvtColor(edges.copy(), cv2.COLOR_GRAY2BGR)
    centro_segundo = None
    radio_segundo = None
    segundo_mayor = None

    if contours:
        # Ordena los contornos por área de mayor a menor
        contornos_ordenados = sorted(contours, key=cv2.contourArea, reverse=True)

        if len(contornos_ordenados) > 1:
            # Centro del segundo contorno más grande
            segundo_mayor = contornos_ordenados[1]
            M_segundo = cv2.moments(segundo_mayor)
            if M_segundo["m00"] != 0:
                cx_segundo = int(M_segundo["m10"] / M_segundo["m00"])
                cy_segundo = int(M_segundo["m01"] / M_segundo["m00"])
                centro_segundo = (cx_segundo, cy_segundo)

                # Calcular el radio como el del círculo mínimo que encierra el contorno
                (x, y), radio_segundo = cv2.minEnclosingCircle(segundo_mayor)
                radio_segundo = int(radio_segundo)

    return mask_vis, centro_segundo, radio_segundo, segundo_mayor