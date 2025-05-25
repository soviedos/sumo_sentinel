# 🤖 Sumo Sentinel

**Sumo Sentinel** es un sistema de visión por computadora optimizado para actuar como juez automático en competiciones de sumo robótico. Implementa algoritmos de inteligencia artificial para el reconocimiento de patrones en tiempo real utilizando hardware embebido de bajo costo como **Nicla Vision** y **Portenta H7**.

El sistema detecta elementos clave como el **dojo** (área de combate) y los **robots participantes**, permitiendo juzgar con precisión si un robot ha salido del área permitida.

---

## 📁 Estructura del Proyecto

```text
sumo_sentinel/
├── datasets/
│   ├── dojo/
│   │   ├── images/{train,val,test}/
│   │   ├── labels/{train,val,test}/
│   │   └── data_dojo.yaml
│   ├── robot/
│   │   ├── images/{train,val,test}/
│   │   ├── labels/{train,val,test}/
│   │   └── data_robot.yaml
├── yolov5/                  # Repositorio de Ultralytics
├── training/train.py        # Script de entrenamiento
├── inference/               # Scripts de inferencia
├── deployment/              # Código para Nicla y Portenta
├── models/converted/        # Modelos .tflite, .onnx, .pt
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🛠 Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/soviedos/sumo-sentinel.git
cd sumo-sentinel
```

2. Clona YOLOv5 dentro del proyecto:

```bash
git clone https://github.com/ultralytics/yolov5.git
```

3. Crea y activa el entorno virtual:

```bash
python3 -m venv venv
source venv/bin/activate
```

4. Instala las dependencias:

```bash
pip install -r requirements.txt
cd yolov5
pip install -r requirements.txt
cd ..
```

---

## 🔧 Entrenamiento

```bash
# Entrenar dojo
python training/train.py --target dojo

# Entrenar robot
python training/train.py --target robot --img 640 --epochs 100 --batch 16
```

> Las rutas están preconfiguradas para funcionar desde `yolov5/`  
> El modelo se guarda en: `yolov5/runs/train/dojo_model/weights/best.pt`

---

## 🛠 Corrección de estructura de carpetas

Asegúrate de que no haya subcarpetas erróneas como `images/train/images`. Si importaste desde Roboflow, ejecuta:

```bash
mv datasets/dojo/images/train/images/* datasets/dojo/images/train/
rmdir datasets/dojo/images/train/images

mv datasets/dojo/labels/train/labels/* datasets/dojo/labels/train/
rmdir datasets/dojo/labels/train/labels
```

> Repite lo mismo para `val` y `test` si aplica.

---

## 🚀 Conversión a TensorFlow Lite

### 1. Exportar de `.pt` a `.onnx`:

```bash
cd yolov5
python export.py --weights runs/train/dojo_model/weights/best.pt --include onnx
```

### 2. Convertir a `.tflite` con TensorFlow:

```python
import tensorflow as tf

converter = tf.lite.TFLiteConverter.from_saved_model("best_tf")
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_model = converter.convert()
with open("dojo.tflite", "wb") as f:
    f.write(tflite_model)
```

---

## 📲 Despliegue embebido

### Nicla Vision (OpenMV)

- El modelo `.tflite` debe estar cuantizado a **int8**
- Se ejecuta desde OpenMV IDE usando los scripts en `deployment/nicla_vision/`

### Portenta H7 (Arduino)

- Usa la biblioteca `Arduino_TensorFlowLite`
- Integra el `.tflite` como array C++ y realiza inferencia local

---

## 🧪 Validación de dataset

Por cada imagen debe existir un archivo `.txt` con el mismo nombre base en `labels/`, con el siguiente formato:

```
<class_id> <x_center> <y_center> <width> <height>
```

> Los valores deben estar normalizados entre 0 y 1.

---

## 🐞 Errores comunes

### ❌ No labels found in labels.cache

- Verifica que los `.txt` existan en `labels/train`
- Asegúrate de que no estén vacíos
- Elimina los archivos `.cache`:

```bash
find datasets/ -name "*.cache" -delete
```

### ❌ Dataset not found o missing paths

- Revisa que el archivo `data_dojo.yaml` tenga rutas correctas:

```yaml
train: ../datasets/dojo/images/train
val: ../datasets/dojo/images/val
test: ../datasets/dojo/images/test
```

---

## 📄 Licencia

MIT © 2025 Sergio Oviedo Seas

---

## 🙌 Créditos

Este proyecto forma parte de la tesis de investigación aplicada para la Maestría en Ingeniería de Software con énfasis en Inteligencia Artificial de la Universidad CENFOTEC.





