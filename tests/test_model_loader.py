from model_loader import cargar_modelo_dojo, cargar_modelo_robots
from config import YOLO8_DOJO_MODEL, YOLO5_ROBOT_MODEL

def test_config():
    print("Ruta modelo DOJO:", YOLO8_DOJO_MODEL)
    print("Ruta modelo ROBOTS:", YOLO5_ROBOT_MODEL)

def test_modelos():
    dojo = cargar_modelo_dojo()
    robots = cargar_modelo_robots()
    print("[OK] Modelos cargados correctamente")

if __name__ == "__main__":
    print("== Prueba Sección 1: Configuración ==")
    test_config()
    print("\n== Prueba Sección 2: Carga de Modelos ==")
    test_modelos()
