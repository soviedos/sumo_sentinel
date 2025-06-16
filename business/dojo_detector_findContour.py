import cv2
import numpy as np

def procesar_dojo_findContours(mask):
    """
    Procesa la máscara binaria para encontrar los dos contornos más grandes,
    calcula sus centros y la distancia entre ellos.
    Devuelve:
        - imagen de resultado (BGR)
        - centro del mayor (o None)
        - centro del segundo mayor (o None)
        - distancia euclidiana (o None)
    """
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    mask_vis = cv2.cvtColor(mask.copy(), cv2.COLOR_GRAY2BGR)
    centro_mayor = None
    centro_segundo = None
    distancia = None

    if contours:
        # Ordena los contornos por área de mayor a menor
        contornos_ordenados = sorted(contours, key=cv2.contourArea, reverse=True)

        if len(contornos_ordenados) > 1:
            # Centro del círculo (contorno más grande)
            mayor = contornos_ordenados[0]
            M_mayor = cv2.moments(mayor)
            if M_mayor["m00"] != 0:
                cx_mayor = int(M_mayor["m10"] / M_mayor["m00"])
                cy_mayor = int(M_mayor["m01"] / M_mayor["m00"])
                centro_mayor = (cx_mayor, cy_mayor)

            # Centro del segundo contorno más grande
            segundo_mayor = contornos_ordenados[1]
            M_segundo = cv2.moments(segundo_mayor)
            if M_segundo["m00"] != 0:
                cx_segundo = int(M_segundo["m10"] / M_segundo["m00"])
                cy_segundo = int(M_segundo["m01"] / M_segundo["m00"])
                centro_segundo = (cx_segundo, cy_segundo)
                cv2.circle(mask_vis, centro_segundo, 5, (57, 255, 0), -1)  # Naranja

                # Calcular distancia euclidiana
                if centro_mayor:
                    distancia = np.sqrt((cx_mayor - cx_segundo) ** 2 + (cy_mayor - cy_segundo) ** 2)