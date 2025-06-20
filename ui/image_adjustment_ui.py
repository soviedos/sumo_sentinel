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
        self.toggle1 = tk.Checkbutton(self.toggles_frame, text="Filtro 1", variable=self.toggle_var1,
              onvalue=True, offvalue=False, font=("Orbitron", 10),
              command=make_toggle_callback(None, self.toggle_var1))
        self.toggle1.grid(row=1, column=0, padx=8, sticky="ew")

        self.toggle2 = tk.Checkbutton(self.toggles_frame, text="Filtro 2", variable=self.toggle_var2,
              onvalue=True, offvalue=False, font=("Orbitron", 10),
              command=make_toggle_callback(None, self.toggle_var2))
        self.toggle2.grid(row=1, column=1, padx=8, sticky="ew")

        self.toggle3 = tk.Checkbutton(self.toggles_frame, text="Filtro 3", variable=self.toggle_var3,
              onvalue=True, offvalue=False, font=("Orbitron", 10),
              command=make_toggle_callback(None, self.toggle_var3))
        self.toggle3.grid(row=1, column=2, padx=8, sticky="ew")

        self.toggle4 = tk.Checkbutton(self.toggles_frame, text="Filtro 4", variable=self.toggle_var4,
              onvalue=True, offvalue=False, font=("Orbitron", 10),
              command=make_toggle_callback(None, self.toggle_var4))
        self.toggle4.grid(row=1, column=3, padx=8, sticky="ew")

        # Toggle switches (segunda fila) con separación vertical
        self.toggle5 = tk.Checkbutton(self.toggles_frame, text="Filtro 5", variable=self.toggle_var5,
              onvalue=True, offvalue=False, font=("Orbitron", 10),
              command=make_toggle_callback(None, self.toggle_var5))
        self.toggle5.grid(row=2, column=0, padx=8, pady=(16, 0), sticky="ew")

        self.toggle6 = tk.Checkbutton(self.toggles_frame, text="Filtro 6", variable=self.toggle_var6,
              onvalue=True, offvalue=False, font=("Orbitron", 10),
              command=make_toggle_callback(None, self.toggle_var6))
        self.toggle6.grid(row=2, column=1, padx=8, pady=(16, 0), sticky="ew")

        self.toggle7 = tk.Checkbutton(self.toggles_frame, text="Filtro 7", variable=self.toggle_var7,
              onvalue=True, offvalue=False, font=("Orbitron", 10),
              command=make_toggle_callback(None, self.toggle_var7))
        self.toggle7.grid(row=2, column=2, padx=8, pady=(16, 0), sticky="ew")

        self.toggle8 = tk.Checkbutton(self.toggles_frame, text="Filtro 8", variable=self.toggle_var8,
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
            brillo = self.brillo_slider.get()
            contraste = self.contraste_slider.get()
            min_white = int(self.min_white_slider.get())
            max_white = int(self.max_white_slider.get())

            self.frame_original = frame.copy()

            frame_procesada = cv2.resize(frame, (cfg.FRAME_WIDTH, cfg.FRAME_HEIGHT))

            # Filtro 1: Ajuste de brillo y contraste
            if self.toggle_var1.get():
                frame_procesada = self.ajustar_brillo_contraste(frame_procesada, brillo, contraste)

            # Filtro 2: HSV
            if self.toggle_var2.get():
                hsv = cv2.cvtColor(frame_procesada, cv2.COLOR_BGR2HSV)
                lower = np.array([cfg.H_MIN, cfg.S_MIN, cfg.V_MIN])
                upper = np.array([cfg.H_MAX, cfg.S_MAX, cfg.V_MAX])
                mask = cv2.inRange(hsv, lower, upper)
                frame_procesada = cv2.bitwise_and(frame_procesada, frame_procesada, mask=mask)

            # Filtro 3: Escala de grises
            if self.toggle_var3.get():
                frame_procesada = cv2.cvtColor(frame_procesada, cv2.COLOR_BGR2GRAY)

            # Filtro 4: Ecualización del histograma
            if self.toggle_var4.get() and len(frame_procesada.shape) == 2:
                frame_procesada = cv2.equalizeHist(frame_procesada)

            # Filtro 5: Ajuste de min y max de blancos
            if self.toggle_var5.get() and len(frame_procesada.shape) == 2:
                frame_procesada = cv2.inRange(frame_procesada, min_white, max_white)

            # Filtro 6: Morfología
            if self.toggle_var6.get() and len(frame_procesada.shape) == 2:
                kernel = np.ones((5, 5), np.uint8)
                frame_procesada = cv2.morphologyEx(frame_procesada, cv2.MORPH_CLOSE, kernel)

            # Filtro 7: Filtro bilateral
            if self.toggle_var7.get() and len(frame_procesada.shape) == 2:
                frame_procesada = cv2.bilateralFilter(frame_procesada, 9, 75, 75)

            # Mostrar imagen original
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb)
            imgtk = ImageTk.PhotoImage(image=img)
            self.image_label.imgtk = imgtk
            self.image_label.configure(image=imgtk)

            # Mostrar máscara procesada
            if len(frame_procesada.shape) == 2:
                mask_rgb = cv2.cvtColor(frame_procesada, cv2.COLOR_GRAY2RGB)
            else:
                mask_rgb = frame_procesada
            mask_img = Image.fromarray(mask_rgb)
            mask_tk = ImageTk.PhotoImage(image=mask_img)
            self.mask_label.imgtk = mask_tk
            self.mask_label.configure(image=mask_tk)

        self.root.after(30, self.actualizar_frame)

    def on_closing(self):
        self.cap.release()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SumoSentinelCameraApp(root)
    root.mainloop()

    # Agrega después de la clase principal para extender la interfaz con toggles

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

        # Crear toggles (Checkbutton) para cada filtro
        col = 0
        for filtro, var in app.filtros_estado.items():
            toggle = tk.Checkbutton(
                app.filtros_frame, text=filtro, variable=var,
                onvalue=True, offvalue=False,
                fg="cyan", bg="black", selectcolor="gray20",
                font=("Orbitron", 10), activebackground="black", activeforeground="cyan"
            )
            toggle.grid(row=0, column=col, padx=8)
            col += 1

    # Modifica el método actualizar_frame para aplicar los filtros según los toggles
    def actualizar_frame_con_filtros(self):
        ret, frame = self.cap.read()
        if ret:
            brillo = self.brillo_slider.get()
            contraste = self.contraste_slider.get()
            min_white = int(self.min_white_slider.get())
            max_white = int(self.max_white_slider.get())

            self.frame_original = frame.copy()
            frame_ajustado = cv2.resize(frame, (cfg.FRAME_WIDTH, cfg.FRAME_HEIGHT))
            frame_mejorado = self.ajustar_brillo_contraste(frame_ajustado, brillo, contraste)

            img_procesada = frame_mejorado

            # Filtro HSV
            if self.filtros_estado["HSV"].get():
                hsv = cv2.cvtColor(img_procesada, cv2.COLOR_BGR2HSV)
                lower = np.array([cfg.H_MIN, cfg.S_MIN, cfg.V_MIN])
                upper = np.array([cfg.H_MAX, cfg.S_MAX, cfg.V_MAX])
                mask = cv2.inRange(hsv, lower, upper)
                img_procesada = cv2.bitwise_and(img_procesada, img_procesada, mask=mask)

            # Escala de grises
            if self.filtros_estado["Grises"].get():
                img_procesada = cv2.cvtColor(img_procesada, cv2.COLOR_BGR2GRAY)
            else:
                # Si no está en grises, convertir a RGB para mostrar la máscara
                img_procesada = cv2.cvtColor(img_procesada, cv2.COLOR_BGR2RGB)

            # Ecualización del histograma
            if self.filtros_estado["Ecualizar"].get() and len(img_procesada.shape) == 2:
                img_procesada = cv2.equalizeHist(img_procesada)

            # Ajuste de blancos
            if self.filtros_estado["Blancos"].get() and len(img_procesada.shape) == 2:
                img_procesada = cv2.inRange(img_procesada, min_white, max_white)

            # Morfología
            if self.filtros_estado["Morfología"].get() and len(img_procesada.shape) == 2:
                kernel = np.ones((5, 5), np.uint8)
                img_procesada = cv2.morphologyEx(img_procesada, cv2.MORPH_CLOSE, kernel)

            # Bilateral
            if self.filtros_estado["Bilateral"].get() and len(img_procesada.shape) == 2:
                img_procesada = cv2.bilateralFilter(img_procesada, 9, 75, 75)

            # Mostrar imagen original
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb)
            imgtk = ImageTk.PhotoImage(image=img)
            self.image_label.imgtk = imgtk
            self.image_label.configure(image=imgtk)

            # Mostrar máscara procesada
            if len(img_procesada.shape) == 2:
                mask_rgb = cv2.cvtColor(img_procesada, cv2.COLOR_GRAY2RGB)
            else:
                mask_rgb = img_procesada
            mask_img = Image.fromarray(mask_rgb)
            mask_tk = ImageTk.PhotoImage(image=mask_img)
            self.mask_label.imgtk = mask_tk
            self.mask_label.configure(image=mask_tk)

        self.root.after(30, self.actualizar_frame)

    # Reemplaza el método actualizar_frame de la clase por el nuevo
    SumoSentinelCameraApp.actualizar_frame = actualizar_frame_con_filtros

    # Llama a la función para agregar los toggles después de crear la app
    agregar_filtros_toggle(app)
    # Asegúrate de que el método after apunte al nuevo actualizar_frame
    app.root.after_cancel(app.root.after_id) if hasattr(app.root, 'after_id') else None
    app.root.after_id = app.root.after(30, app.actualizar_frame)