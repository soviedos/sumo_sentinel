import os
import argparse
from pathlib import Path

def train_model(data_yaml, model_name, weights="yolov5n.pt", img_size=640, batch=16, epochs=50):
    """
    Ejecuta el entrenamiento con YOLOv5 desde un dataset en formato YOLOv5.
    """
    yolov5_path = Path(__file__).resolve().parent.parent / "yolov5"
    command = (
        f"cd {yolov5_path} && "
        f"python train.py "
        f"--img {img_size} "
        f"--batch {batch} "
        f"--epochs {epochs} "
        f"--data {data_yaml} "
        f"--weights {weights} "
        f"--name {model_name}"
    )
    print(f"\n[INFO] Ejecutando entrenamiento:\n{command}\n")
    os.system(command)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Entrena modelos YOLOv5 para Sumo Sentinel")
    parser.add_argument("--target", choices=["dojo", "robot"], required=True, help="Nombre del modelo a entrenar")
    parser.add_argument("--img", type=int, default=640, help="Tamaño de imagen (ej: 640)")
    parser.add_argument("--batch", type=int, default=16, help="Tamaño del batch")
    parser.add_argument("--epochs", type=int, default=50, help="Número de épocas de entrenamiento")
    parser.add_argument("--weights", type=str, default="yolov5n.pt", help="Pesos base de YOLOv5")

    args = parser.parse_args()

    if args.target == "dojo":
        data_yaml = "/home/soviedos/Documents/UCenfotec/MISIA/PIA-02/Code/sumo_sentinel/datasets/data_dojo.yaml"
        model_name = "dojo_model"
    elif args.target == "robot":
        data_yaml = "/home/soviedos/Documents/UCenfotec/MISIA/PIA-02/Code/sumo_sentinel/datasets/data_robot.yaml"
        model_name = "robot_model"

    train_model(
        data_yaml=data_yaml,
        model_name=model_name,
        weights=args.weights,
        img_size=args.img,
        batch=args.batch,
        epochs=args.epochs
    )
