import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config')))
import config as cfg
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
import cv2
import numpy as np
from futuristic_controls import FuturisticScale  # archivo separado

class SumoSentinelCameraApp:
    def __init__(self, root):
        self.root = root
        self.root.title(cfg.WINDOW_NAME)
        self.root.geometry("1280x800")
        self.root.configure(bg="black")
        self.dojo_center = None
        self.dojo_radius = None

        # Título
        self.title_label = Label(root, text=cfg.WINDOW_NAME, font=("Orbitron", 20), fg="cyan", bg="black")
        self.title_label.pack(pady=10)

        # Contenedor de vistas
        self.image_container = tk.Frame(root, bg="black")
        self.image_container.pack()

        # Imagen principal
        self.image_label = Label(self.image_container, bg="black")
        self.image_label.grid(row=0, column=0, padx=10)

        # Máscara binaria
        self.mask_label = Label(self.image_container, bg="black")
        self.mask_label.grid(row=0, column=1, padx=10)

        # Panel de controles
        self.controls_frame = tk.Frame(root, bg="black")
        self.controls_frame.pack(pady=10)

        self.brillo_slider = FuturisticScale(self.controls_frame, "Brillo", -100, 100, initial=cfg.SCALE_BRILLO)
        self.brillo_slider.grid(row=0, column=0, padx=10)

        self.contraste_slider = FuturisticScale(self.controls_frame, "Contraste", 0.5, 3.0, initial=cfg.SCALE_CONTRASTE, resolution=0.1)
        self.contraste_slider.grid(row=1, column=0, padx=10)

        self.min_white_slider = FuturisticScale(self.controls_frame, "Min White (gris)", 0, 255, initial=cfg.SCALE_MIN_WHITE)
        self.min_white_slider.grid(row=0, column=1, padx=10)

        self.max_white_slider = FuturisticScale(self.controls_frame, "Max White (gris)", 0, 255, initial=cfg.SCALE_MAX_WHITE)
        self.max_white_slider.grid(row=1, column=1, padx=10)

        # Iniciar cámara
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.title_label.config(text="No se pudo abrir la cámara")

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.actualizar_frame()

    def ajustar_brillo_contraste(self, imagen, brillo, contraste):
        return cv2.convertScaleAbs(imagen, alpha=contraste, beta=brillo)

    def actualizar_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Ajustes
            brillo = self.brillo_slider.get()
            contraste = self.contraste_slider.get()
            min_white = int(self.min_white_slider.get())
            max_white = int(self.max_white_slider.get())

            self.frame_original = frame.copy()  # Guarda una copia para detección

            # Leer resolución desde config

            frame_ajustado = cv2.resize(frame, (cfg.FRAME_WIDTH, cfg.FRAME_HEIGHT))  # Ajusta el tamaño del frame

            # Ajuste de brillo y contraste
            frame_mejorado = self.ajustar_brillo_contraste(frame_ajustado, brillo, contraste)
            
            # Filtro HSV usando valores fijos
            hsv = cv2.cvtColor(frame_mejorado, cv2.COLOR_BGR2HSV)
            lower = np.array([cfg.H_MIN, cfg.S_MIN, cfg.V_MIN])
            upper = np.array([cfg.H_MAX, cfg.S_MAX, cfg.V_MAX])
            mask = cv2.inRange(hsv, lower, upper)
            frame_filtrado = cv2.bitwise_and(frame_mejorado, frame_mejorado, mask=mask)

            # Conversion a escala de grises
            gray = cv2.cvtColor(frame_filtrado, cv2.COLOR_BGR2GRAY)  # Convierte la imagen a escala de grises

            # Ecualización del histograma
            equalized = cv2.equalizeHist(gray)

            # Ajuste de min y max de blancos
            mask_white = cv2.inRange(equalized, min_white, max_white)

            # Aplicar morfología para limpiar la imagen
            kernel = np.ones((5, 5), np.uint8)
            closed = cv2.morphologyEx(mask_white, cv2.MORPH_CLOSE, kernel)

            # Aplicar filtro bilateral para suavizar la imagen
            filtered = cv2.bilateralFilter(closed, 9, 75, 75)

            # Mostrar imagen original
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb)
            imgtk = ImageTk.PhotoImage(image=img)
            self.image_label.imgtk = imgtk
            self.image_label.configure(image=imgtk)

            # Mostrar máscara después de ajuste de blancos y binarización
            mask_rgb = cv2.cvtColor(filtered, cv2.COLOR_GRAY2RGB)
            mask_img = Image.fromarray(mask_rgb)
            mask_tk = ImageTk.PhotoImage(image=mask_img)
            self.mask_label.imgtk = mask_tk
            self.mask_label.configure(image=mask_tk)

            # Llamar procesamiento del dojo si se desea continuo
            #self.procesar_dojo(filtered)
            #self.detectar_dojo_canny(filtered)

        self.root.after(30, self.actualizar_frame)

    def on_closing(self):
        self.cap.release()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SumoSentinelCameraApp(root)
    root.mainloop()

