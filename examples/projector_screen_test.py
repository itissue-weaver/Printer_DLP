# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 15/may/2025  at 20:11 $"
import ttkbootstrap as ttk
from templates.daemons.DLPViewer import DlpViewer

# Definir la variable global
projector = None


def start_projector():
    global projector  # Indicar que estamos modificando la variable global
    if projector and projector.is_alive():
        print("El hilo ya está en ejecución.")
    else:
        projector = DlpViewer()  # Crear una nueva instancia accesible globalmente
        projector.start_projecting()


def stop_projector():
    global projector
    if projector:
        projector.stop_projecting()
        projector = None  # Resetear la referencia después de detenerlo


if __name__ == "__main__":
    # Crear la ventana de la interfaz
    root = ttk.Window(themename="darkly")
    root.geometry("300x200")
    root.title("Control de Hilo")

    btn_start = ttk.Button(root, text="Iniciar", command=start_projector)
    btn_start.pack(pady=5)

    btn_stop = ttk.Button(root, text="Detener", command=stop_projector)
    btn_stop.pack(pady=5)

    root.mainloop()
