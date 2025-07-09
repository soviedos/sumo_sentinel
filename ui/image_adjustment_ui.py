import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config')))
import config as cfg
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
import cv2
import numpy as np
from sumo_sentinel.ui.futuristic_controls import FuturisticScale  # archivo separado
from sumo_sentinel.business.dojo_detector_filters import DojoFilters as df
from sumo_sentinel.business.dojo_detector_canny import detectar_dojo_canny as dd_canny
from sumo_sentinel.business.dojo_detector_findContour import procesar_dojo_findContours as dd_findContours
from sumo_sentinel.business.dojo_detector_hough import detectar_dojo_hough as dd_hough
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

        self.min_white_slider = FuturisticScale(self.controls_frame, "Min Blanco (gris)", 0, 255, initial=cfg.SCALE_MIN_WHITE)
        self.min_white_slider.grid(row=0, column=1, padx=10)

        self.max_white_slider = FuturisticScale(self.controls_frame, "Max Blanco (gris)", 0, 255, initial=cfg.SCALE_MAX_WHITE)
        self.max_white_slider.grid(row=1, column=1, padx=10)

        # Frame para toggles
        self.toggles_frame = tk.Frame(root, bg="black")
        self.toggles_frame.pack(pady=10)

        # Título para los toggles
        self.toggles_title = Label(self.toggles_frame, text="Seleccion de filtros de binarizacion", font=("Arial", 12), fg="cyan", bg="black")
        self.toggles_title.grid(row=0, column=0, columnspan=4, pady=(0, 8))

        # Variables para toggles (primer fila)
        self.toggle_var1 = tk.BooleanVar(value=False)
        self.toggle_var2 = tk.BooleanVar(value=False)
        self.toggle_var3 = tk.BooleanVar(value=False)
        self.toggle_var4 = tk.BooleanVar(value=False)
        # Variables para toggles (segunda fila)
        self.toggle_var5 = tk.BooleanVar(value=False)
        self.toggle_var6 = tk.BooleanVar(value=False)
        self.toggle_var7 = tk.BooleanVar(value=False)
        self.toggle_var8 = tk.BooleanVar(value=False)

        # Función para actualizar el color de fondo y texto del toggle
        def update_toggle_style(toggle, var):
            if var.get():
                toggle.config(bg="deepskyblue", fg="black", activebackground="deepskyblue", activeforeground="black")
            else:
                toggle.config(bg="white", fg="black", activebackground="white", activeforeground="black")

        # Callback para cada toggle
        def make_toggle_callback(toggle, var):
            return lambda: update_toggle_style(toggle, var)

        # Toggle switches (primer fila)
        self.toggle1 = tk.Checkbutton(self.toggles_frame, text="Brillo_Contraste", variable=self.toggle_var1,
              onvalue=True, offvalue=False, font=("Orbitron", 10),
              command=make_toggle_callback(None, self.toggle_var1))
        self.toggle1.grid(row=1, column=0, padx=8, sticky="ew")

        self.toggle2 = tk.Checkbutton(self.toggles_frame, text="HSV", variable=self.toggle_var2,
              onvalue=True, offvalue=False, font=("Orbitron", 10),
              command=make_toggle_callback(None, self.toggle_var2))
        self.toggle2.grid(row=1, column=1, padx=8, sticky="ew")

        self.toggle3 = tk.Checkbutton(self.toggles_frame, text="Esc_Grises", variable=self.toggle_var3,
              onvalue=True, offvalue=False, font=("Orbitron", 10),
              command=make_toggle_callback(None, self.toggle_var3))
        self.toggle3.grid(row=1, column=2, padx=8, sticky="ew")

        self.toggle4 = tk.Checkbutton(self.toggles_frame, text="Ecu_Histograma", variable=self.toggle_var4,
              onvalue=True, offvalue=False, font=("Orbitron", 10),
              command=make_toggle_callback(None, self.toggle_var4))
        self.toggle4.grid(row=1, column=3, padx=8, sticky="ew")

        # Toggle switches (segunda fila) con separación vertical
        self.toggle5 = tk.Checkbutton(self.toggles_frame, text="Min_Max_Blancos", variable=self.toggle_var5,
              onvalue=True, offvalue=False, font=("Orbitron", 10),
              command=make_toggle_callback(None, self.toggle_var5))
        self.toggle5.grid(row=2, column=0, padx=8, pady=(16, 0), sticky="ew")

        self.toggle6 = tk.Checkbutton(self.toggles_frame, text="Morfologia", variable=self.toggle_var6,
              onvalue=True, offvalue=False, font=("Orbitron", 10),
              command=make_toggle_callback(None, self.toggle_var6))
        self.toggle6.grid(row=2, column=1, padx=8, pady=(16, 0), sticky="ew")

        self.toggle7 = tk.Checkbutton(self.toggles_frame, text="Bilateral", variable=self.toggle_var7,
              onvalue=True, offvalue=False, font=("Orbitron", 10),
              command=make_toggle_callback(None, self.toggle_var7))
        self.toggle7.grid(row=2, column=2, padx=8, pady=(16, 0), sticky="ew")

        self.toggle8 = tk.Checkbutton(self.toggles_frame, text="Gaussiano", variable=self.toggle_var8,
              onvalue=True, offvalue=False, font=("Orbitron", 10),
              command=make_toggle_callback(None, self.toggle_var8))
        self.toggle8.grid(row=2, column=3, padx=8, pady=(16, 0), sticky="ew")

        # Asignar los toggles a los callbacks correctos (para acceso en callback)
        self.toggle1.config(command=make_toggle_callback(self.toggle1, self.toggle_var1))
        self.toggle2.config(command=make_toggle_callback(self.toggle2, self.toggle_var2))
        self.toggle3.config(command=make_toggle_callback(self.toggle3, self.toggle_var3))
        self.toggle4.config(command=make_toggle_callback(self.toggle4, self.toggle_var4))
        self.toggle5.config(command=make_toggle_callback(self.toggle5, self.toggle_var5))
        self.toggle6.config(command=make_toggle_callback(self.toggle6, self.toggle_var6))
        self.toggle7.config(command=make_toggle_callback(self.toggle7, self.toggle_var7))
        self.toggle8.config(command=make_toggle_callback(self.toggle8, self.toggle_var8))

        # Inicializar colores según estado inicial
        update_toggle_style(self.toggle1, self.toggle_var1)
        update_toggle_style(self.toggle2, self.toggle_var2)
        update_toggle_style(self.toggle3, self.toggle_var3)
        update_toggle_style(self.toggle4, self.toggle_var4)
        update_toggle_style(self.toggle5, self.toggle_var5)
        update_toggle_style(self.toggle6, self.toggle_var6)
        update_toggle_style(self.toggle7, self.toggle_var7)
        update_toggle_style(self.toggle8, self.toggle_var8)

        # --- NUEVO GRUPO DE TOGGLES: Algoritmos de detección del dojo ---
        self.dojo_detection_frame = tk.Frame(root, bg="black")
        self.dojo_detection_frame.pack(pady=10)

        self.dojo_detection_title = Label(self.dojo_detection_frame, text="Algoritmos de detección del dojo", font=("Arial", 12), fg="cyan", bg="black")
        self.dojo_detection_title.grid(row=0, column=0, columnspan=3, pady=(0, 8))

        self.dojo_detection_var1 = tk.BooleanVar(value=False)
        self.dojo_detection_var2 = tk.BooleanVar(value=False)
        self.dojo_detection_var3 = tk.BooleanVar(value=False)

        self.dojo_detection1 = tk.Checkbutton(self.dojo_detection_frame, text="Hough", variable=self.dojo_detection_var1,
                                         onvalue=True, offvalue=False, font=("Orbitron", 10),
                                         bg="white", fg="black", activebackground="white", activeforeground="black")
        self.dojo_detection1.grid(row=1, column=0, padx=8, sticky="ew")

        self.dojo_detection2 = tk.Checkbutton(self.dojo_detection_frame, text="Contornos", variable=self.dojo_detection_var2,
                                         onvalue=True, offvalue=False, font=("Orbitron", 10),
                                         bg="white", fg="black", activebackground="white", activeforeground="black")
        self.dojo_detection2.grid(row=1, column=1, padx=8, sticky="ew")

        self.dojo_detection3 = tk.Checkbutton(self.dojo_detection_frame, text="Canny", variable=self.dojo_detection_var3,
                                         onvalue=True, offvalue=False, font=("Orbitron", 10),
                                         bg="white", fg="black", activebackground="white", activeforeground="black")
        self.dojo_detection3.grid(row=1, column=2, padx=8, sticky="ew")

        # Estilo para los toggles de algoritmos
        def update_dojo_detection_style(toggle, var):
            if var.get():
                toggle.config(bg="deepskyblue", fg="black", activebackground="deepskyblue", activeforeground="black")
            else:
                toggle.config(bg="white", fg="black", activebackground="white", activeforeground="black")

        self.dojo_detection1.config(command=lambda: update_dojo_detection_style(self.dojo_detection1, self.dojo_detection_var1))
        self.dojo_detection2.config(command=lambda: update_dojo_detection_style(self.dojo_detection2, self.dojo_detection_var2))
        self.dojo_detection3.config(command=lambda: update_dojo_detection_style(self.dojo_detection3, self.dojo_detection_var3))

        update_dojo_detection_style(self.dojo_detection1, self.dojo_detection_var1)
        update_dojo_detection_style(self.dojo_detection2, self.dojo_detection_var2)
        update_dojo_detection_style(self.dojo_detection3, self.dojo_detection_var3)
        # --- FIN NUEVO GRUPO DE TOGGLES ---

        # Iniciar cámara
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.title_label.config(text="No se pudo abrir la cámara")

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.actualizar_frame()

    def actualizar_frame(self):
        ret, frame = self.cap.read()
        if ret:
            brillo = self.brillo_slider.get()
            contraste = self.contraste_slider.get()
            min_white = int(self.min_white_slider.get())
            max_white = int(self.max_white_slider.get())

            self.frame_original = frame.copy()

            frame_procesada = cv2.resize(frame, (cfg.FRAME_WIDTH, cfg.FRAME_HEIGHT))

            contorno = None
            center = None
            radius = None

            # Filtro 1: Ajuste de brillo y contraste
            if self.toggle_var1.get():
                frame_procesada = df.ajustar_brillo_contraste(frame_procesada, brillo, contraste)

            # Filtro 2: HSV
            if self.toggle_var2.get():
                lower = np.array([cfg.H_MIN, cfg.S_MIN, cfg.V_MIN])
                upper = np.array([cfg.H_MAX, cfg.S_MAX, cfg.V_MAX])
                frame_procesada = df.filtro_hsv(frame_procesada, lower, upper)

            # Filtro 3: Escala de grises
            if self.toggle_var3.get():
                frame_procesada = df.a_grises(frame_procesada)

            # Filtro 4: Ecualización del histograma
            if self.toggle_var4.get() and len(frame_procesada.shape) == 2:
                frame_procesada = df.ecualizacion_histograma(frame_procesada)

            # Filtro 5: Ajuste de min y max de blancos
            if self.toggle_var5.get() and len(frame_procesada.shape) == 2:
                frame_procesada = df.filtro_min_max_blancos(frame_procesada, min_white, max_white)

            # Filtro 6: Morfología
            if self.toggle_var6.get() and len(frame_procesada.shape) == 2:
                frame_procesada = df.filtro_morfologico(frame_procesada, cv2.MORPH_CLOSE, cfg.KERNEL_SIZE)

            # Filtro 7: Filtro bilateral
            if self.toggle_var7.get() and len(frame_procesada.shape) == 2:
                frame_procesada = df.filtro_bilateral(frame_procesada, cfg.PIXEL_NEIGHBORS, cfg.SIGMACOLOR, cfg.SIGMASPACE)

            # Filtro 8: Desenfoque Gaussiano
            if self.toggle_var8.get():
                frame_procesada = df.desenfoque_gaussiano(frame_procesada, (cfg.KERNEL_SIZE, cfg.KERNEL_SIZE))  

            # --- Algoritmos de detección del dojo ---
            # Hough
            if self.dojo_detection_var1.get():
                # Suponiendo que el método se llama detectar_hough y retorna una imagen
                frame_procesada = dd_hough(frame_procesada)
            # Contornos
            if self.dojo_detection_var2.get():
                # Suponiendo que el método se llama detectar_contornos y retorna una imagen
                frame_procesada, center, radius, contorno = dd_findContours(frame_procesada)               
            # Canny
            if self.dojo_detection_var3.get():
                # Suponiendo que el método se llama detectar_canny y retorna una imagen
                frame_procesada, center, radius, contorno = dd_canny(frame_procesada)

            # Mostrar imagen original directamente de la cámara (sin procesamiento)
            rgb = cv2.cvtColor(self.frame_original, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb)
            imgtk = ImageTk.PhotoImage(image=img)
            self.image_label.imgtk = imgtk
            self.image_label.configure(image=imgtk)

            # Mostrar máscara procesada
            mask_rgb = frame_procesada
            # Si la imagen es de un canal, convertir a RGB para mostrar
            if len(mask_rgb.shape) == 2:
                mask_rgb = cv2.cvtColor(mask_rgb, cv2.COLOR_GRAY2RGB)

            # 5. Dibujar resultados para visualización
            if contorno is not None:
                cv2.drawContours(mask_rgb, [contorno], -1, (cfg.COLOR_DOJO_CENTER), 2)
            if center is not None:
                # center debe ser una tupla de enteros
                center_int = (int(center[0]), int(center[1]))
                cv2.circle(mask_rgb, center_int, 2, cfg.COLOR_DOJO_CONTOUR, -1)
                # Si quieres dibujar el círculo del radio:
                # cv2.circle(mask_rgb, center_int, int(radius), (0, 0, 255), 2)

            mask_img = Image.fromarray(mask_rgb)
            mask_tk = ImageTk.PhotoImage(image=mask_img)
            self.mask_label.imgtk = mask_tk
            self.mask_label.configure(image=mask_tk)

        self.root.after(30, self.actualizar_frame)

    def on_closing(self):
        self.cap.release()
        self.root.destroy()

def agregar_filtros_toggle(app):
    # Crear un frame para los toggles
    app.filtros_frame = tk.Frame(app.root, bg="black")
    app.filtros_frame.pack(pady=5)

    # Diccionario para almacenar el estado de cada filtro
    app.filtros_estado = {
        "HSV": tk.BooleanVar(value=True),
        "Grises": tk.BooleanVar(value=True),
        "Ecualizar": tk.BooleanVar(value=True),
        "Blancos": tk.BooleanVar(value=True),
        "Morfología": tk.BooleanVar(value=True),
        "Bilateral": tk.BooleanVar(value=True)
    }

if __name__ == "__main__":
    root = tk.Tk()
    app = SumoSentinelCameraApp(root)
    agregar_filtros_toggle(app)
    SumoSentinelCameraApp.actualizar_frame
    root.mainloop()