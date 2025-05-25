 # 🤖 Sumo Sentinel

**Sumo Sentinel** es un sistema de visión por computadora optimizado para actuar como juez automático en competiciones de sumo robótico. Implementa algoritmos de inteligencia artificial para el reconocimiento de patrones en tiempo real utilizando hardware embebido de bajo costo como **Nicla Vision** y **Portenta H7**.

El sistema detecta elementos clave como el **dojo** (área de combate) y los **robots participantes**, permitiendo juzgar con precisión si un robot ha salido del área permitida.

---

## 📁 Estructura del Proyecto

sumo_sentinel/
├── datasets/
│ ├── dojo/
│ │ ├── images/{train,val,test}/
│ │ ├── labels/{train,val,test}/
│ │ └── data_dojo.yaml
│ ├── robot/
│ │ ├── images/{train,val,test}/
│ │ ├── labels/{train,val,test}/
│ │ └── data_robot.yaml
├── yolov5/ # Repositorio de Ultralytics
├── training/train.py # Script de entrenamiento
├── inference/ # Scripts de inferencia
├── deployment/ # Código para Nicla y Portenta
├── models/converted/ # Modelos .tflite, .onnx, .pt
├── requirements.txt
├── .gitignore
└── README.md
---

## 🛠 Instalación

1. Clona el repositorio:


git clone https://github.com/soviedos/sumo-sentinel.git
cd sumo-sentinel

2. Clona YOLOv5 dentro del proyecto

git clone https://github.com/ultralytics/yolov5.git

3. Crea y activa el entorno virtual

python3 -m venv venv
source venv/bin/activate

3. Instala las dependencias

pip install -r requirements.txt
cd yolov5
pip install -r requirements.txt
cd ..

# 🔧 Entrenamiento

# Entrenar dojo
python training/train.py --target dojo

# Entrenar robot
python training/train.py --target robot --img 640 --epochs 100 --batch 16

Las rutas están preconfiguradas para funcionar desde yolov5/

El modelo se guarda en: yolov5/runs/train/dojo_model/weights/best.pt

# 🛠 Corrección de estructura de carpetas

Asegúrate de que no haya subcarpetas erróneas como images/train/images. Si importaste desde Roboflow, puede que necesites mover los archivos correctamente:

mv datasets/dojo/images/train/images/* datasets/dojo/images/train/
rmdir datasets/dojo/images/train/images

mv datasets/dojo/labels/train/labels/* datasets/dojo/labels/train/
rmdir datasets/dojo/labels/train/labels

# Repetir para val y test si aplica

# 🚀 Conversión a TensorFlow Lite

Para convertir el modelo entrenado a .tflite:

1. Exportar de .pt a .onnx:

cd yolov5
python export.py --weights runs/train/dojo_model/weights/best.pt --include onnx

2. Convertir a .pb y luego a .tflite con TensorFlow:

import tensorflow as tf

converter = tf.lite.TFLiteConverter.from_saved_model("best_tf")
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_model = converter.convert()
with open("dojo.tflite", "wb") as f:
    f.write(tflite_model)

#📲 Despliegue embebido
Nicla Vision (OpenMV)

    Modelo .tflite debe ser int8 quantizado

    Ejecuta el modelo en OpenMV IDE desde deployment/nicla_vision/

Portenta H7 (Arduino)

    Usa la biblioteca Arduino_TensorFlowLite

    Integra el modelo .tflite como array C++ y despliega con inferencia local

# 🧪 Validación de dataset

Asegúrate de que por cada imagen exista un .txt con el mismo nombre en labels/ y que contenga coordenadas normalizadas:

<class_id> <x_center> <y_center> <width> <height>

# 🐞 Errores comunes
❌ No labels found in labels.cache

    Verifica que los .txt existan en labels/train

    Asegúrate de que no estén vacíos

    Elimina archivos .cache:

find datasets/ -name "*.cache" -delete

# ❌ Dataset not found o missing paths

    Revisa que data_dojo.yaml tenga rutas correctas:

train: ../datasets/dojo/images/train
val: ../datasets/dojo/images/val
test: ../datasets/dojo/images/test

 📄 Licencia

MIT © 2025 Sergio Oviedo Seas

# 🙌 Créditos

Este proyecto forma parte de la tesis de investigación aplicada para la Maestría en Ingeniería de Software con énfasis en Inteligencia Artificial de la Universidad CENFOTEC.





