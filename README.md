 # 🤖 Sumo Sentinel

**Sumo Sentinel** es un sistema de visión por computadora optimizado para actuar como juez automático en competiciones de sumo robótico. Implementa algoritmos de inteligencia artificial para el reconocimiento de patrones en tiempo real utilizando hardware embebido de bajo costo como **Nicla Vision** y **Portenta H7**.

El sistema detecta elementos clave como el **dojo** (área de combate) y los **robots participantes**, permitiendo juzgar con precisión si un robot ha salido del área permitida.

---

## 📁 Estructura del Proyecto
sumo_sentinel/
├── datasets/ # Dataset en formato YOLOv5
├── training/ # Entrenamiento de modelos (PyTorch + YOLOv5)
├── inference/ # Inferencia local
├── models/ # Modelos entrenados y convertidos
├── deployment/ # Scripts para Nicla Vision y Portenta H7
├── requirements.txt # Dependencias
├── README.md # Este archivo

---

## 🛠 Instalación

1. Clona el repositorio:


git clone https://github.com/soviedos/sumo-sentinel.git
cd sumo-sentinel

2. Crea y activa el entorno virtual

python3 -m venv venv
source venv/bin/activate

3. Instala las dependencias

pip install -r requirements.txt


