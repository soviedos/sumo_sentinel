import cv2
import numpy as np

def detectar_dojo_hough(frame):
    # Convertir a escala de grises si es necesario
    if len(frame.shape) == 3:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    else:
        gray = frame.copy()

    # Aplicar un umbral para aislar áreas blancas (ajustar valor si es necesario)
    _, mask = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)

    # Suavizar para reducir ruido
    mask = cv2.medianBlur(mask, 7)

    # Detectar círculos con Hough solo en la máscara blanca
    circles = cv2.HoughCircles(
        mask,
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=100,
        param1=100,
        param2=30,
        minRadius=50,
        maxRadius=300  # Ajusta este valor según el tamaño esperado del dojo
    )

    resultado = frame.copy()
    if circles is not None:
        circles = np.uint16(np.around(circles))
        # Seleccionar el círculo más grande (probablemente el dojo blanco)
        mayor = max(circles[0, :], key=lambda c: c[2])
        # Dibuja el círculo externo
        cv2.circle(resultado, (mayor[0], mayor[1]), mayor[2], (0, 255, 255), 2)
        # Dibuja el centro del círculo
        cv2.circle(resultado, (mayor[0], mayor[1]), 4, (0, 255, 0), -1)
    return resultado