# inference/model_loader.py

from ultralytics import YOLO
import torch
from config import YOLO8_DOJO_MODEL, YOLO5_ROBOT_MODEL

def cargar_modelo_dojo():
    print("[INFO] Cargando modelo YOLOv8 para segmentación del dojo...")
    return YOLO(YOLO8_DOJO_MODEL)

def cargar_modelo_robots():
    print("[INFO] Cargando modelo YOLOv5 para detección de robots...")
    return torch.hub.load('ultralytics/yolov5', 'custom', path=YOLO5_ROBOT_MODEL, force_reload=True)
