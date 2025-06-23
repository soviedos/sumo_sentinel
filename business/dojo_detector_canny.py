import cv2
import numpy as np

def detectar_dojo_canny(frame):
    """
    Detecta el dojo usando Canny y devuelve:
    - imagen de resultado (BGR)
    - centro del dojo (x, y) o None
    - radio del dojo o None
    """
    # Convertir a escala de grises si es necesario
    if len(frame.shape) == 3:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    else:
        gray = frame.copy()

    # 1. Aplicar Canny
    edges = cv2.Canny(gray, 100, 200)

    # 2. Encontrar contornos
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        # Devuelve la imagen de Canny en BGR y None para centro/radio
        resultado = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        return resultado, None, None

    # 3. Buscar el contorno más grande
    mayor = max(contours, key=cv2.contourArea)
    # 4. Calcular centro y radio del círculo mínimo que lo contiene
    (x, y), radius = cv2.minEnclosingCircle(mayor)
    center = (int(x), int(y))
    radius = int(radius)

    # 5. Dibujar resultados para visualización
    resultado = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(resultado, [mayor], -1, (0, 255, 0), 2)
    #cv2.circle(resultado, center, radius, (0, 0, 255), 2)
    cv2.circle(resultado, center, 3, (255, 0, 0), -1)

    return resultado, center, radius