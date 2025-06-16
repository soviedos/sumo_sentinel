# inference/test_camera.py

import cv2
from config.config import WINDOW_NAME

print("[INFO] Iniciando prueba de cámara...")

cap = cv2.VideoCapture(0)  # usa cámara por defecto
cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)

if not cap.isOpened():
    print("[ERROR] No se pudo abrir la cámara")
    exit()

while True:
    ret, frame = cap.read()
    if not ret or cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
        print("[INFO] Cámara desconectada o ventana cerrada")
        break

    cv2.imshow(WINDOW_NAME, frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("[INFO] Salida manual con Q")
        break

cap.release()
cv2.destroyAllWindows()
