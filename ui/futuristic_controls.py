import tkinter as tk
from tkinter import Frame, Label, Scale, HORIZONTAL

class FuturisticScale(Frame):
    def __init__(self, parent, label, from_, to, initial=0, resolution=1, command=None):
        super().__init__(parent, bg="black")
        self.command = command

        Label(self, text=label, font=("Arial", 12), fg="cyan", bg="black").pack()

        range_frame = tk.Frame(self, bg="black")
        range_frame.pack(fill="x", padx=5)
        tk.Label(range_frame, text="Min", fg="white", bg="black").pack(side="left")
        tk.Label(range_frame, text="Max", fg="white", bg="black").pack(side="right")

        self.scale = Scale(
            self, from_=from_, to=to, orient=HORIZONTAL,
            resolution=resolution, length=300, fg="white", bg="black",
            troughcolor="deepskyblue", sliderrelief="flat", highlightthickness=0,
            command=self._on_change
        )
        self.scale.set(initial)
        self.scale.pack()

        self.value_label = Label(self, text=f"Valor: {initial}", fg="white", bg="black", font=("Arial", 10))
        self.value_label.pack()

    def _on_change(self, val):
        self.value_label.config(text=f"Valor: {val}")
        if self.command:
            self.command(float(val))

    def get(self):
        return self.scale.get()
