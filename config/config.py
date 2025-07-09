# config.py

# ==== Rutas a modelos ====
YOLO8_DOJO_MODEL = "models/yolov8n_dojo.pt"   # Modelo segmentación dojo (YOLOv8)
YOLO5_ROBOT_MODEL = "models/yolov5_robot.pt"  # Modelo detección robots (YOLOv5)

# ==== Umbrales ====
CONF_THRESHOLD = 0.5  # confianza mínima para detección válida
IOU_THRESHOLD = 0.5   # umbral de IoU si se compara superposición

# ==== Colores BGR ====
COLOR_DOJO_CONTOUR = (255, 0, 0)    # amarillo (RGB)
COLOR_DOJO_CENTER = (255, 255, 0)       # rojo (RGB)
COLOR_ROBOT_INSIDE = (0, 255, 255)    # amarillo
COLOR_ROBOT_OUTSIDE = (0, 0, 255)     # rojo
COLOR_ROBOT_LOST = (100, 100, 100)    # gris oscuro

# ==== Arbitraje ====
MAX_FRAMES_OUTSIDE = 20  # Cuántos frames puede estar fuera el robot antes de perder

# ==== Visualización ====
WINDOW_NAME = "Sumo Sentinel - Vision System App"

# ==== Resolución del frame de la camara====
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# ==== Valores iniciales de las escalas ====
SCALE_BRILLO = 0
SCALE_CONTRASTE = 1.0
SCALE_MIN_WHITE = 200
SCALE_MAX_WHITE = 255
SCALE_UMBRAL_BIN = 127

# ==== Valores fijos recomendados para detectar blancos en HSV ====
H_MIN = 0
H_MAX = 180
S_MIN = 0
S_MAX = 30
V_MIN = 200
V_MAX = 255

# ==== Tamaño del Kernel para filtro morfológico ====

KERNEL_SIZE = 5  # Tamaño del kernel para operaciones morfológicas

# ==== Valores fijos recomendados para el filtro bilateral ====

PIXEL_NEIGHBORS = 9  # Vecindario de píxeles para el filtro bilateral
SIGMACOLOR = 75  # Sigma para el filtro bilateral
SIGMASPACE = 75  # Sigma para el filtro bilaterail

# ==== Canny Threshold values ====

UPPER_THRESHOLD = 200  # Umbral superior para Canny
LOWER_THRESHOLD = 100  # Umbral inferior para Canny