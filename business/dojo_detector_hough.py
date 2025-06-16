import cv2
import numpy as np

def detectar_dojo_hough(frame):
    # 1. Convertir a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 2. Suavizar para reducir ruido
    blurred = cv2.medianBlur(gray, 7)
    # 3. Detectar círculos con Hough
    circles = cv2.HoughCircles(
        blurred,
        cv2.HOUGH_GRADIENT,
        dp=1.2,           # Resolución acumulador
        minDist=100,      # Distancia mínima entre círculos detectados
        param1=100,       # Umbral Canny
        param2=30,        # Umbral acumulador (ajusta sensibilidad)
        minRadius=50,     # Radio mínimo (ajusta según tu dojo)
        maxRadius=0       # Radio máximo (0 = sin límite)
    )
    resultado = frame.copy()
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            # Dibuja el círculo externo
            cv2.circle(resultado, (i[0], i[1]), i[2], (0, 255, 255), 2)
            # Dibuja el centro del círculo
            cv2.circle(resultado, (i[0], i[1]), 4, (0, 255, 0), -1)
        # Si solo quieres el círculo más grande:
        # mayor = max(circles[0, :], key=lambda c: c[2])
        # cv2.circle(resultado, (mayor[0], mayor[1]), mayor[2], (0, 255, 255), 2)
        # cv2.circle(resultado, (mayor[0], mayor[1]), 4, (0, 255, 0), -1)
    return resultado, circles