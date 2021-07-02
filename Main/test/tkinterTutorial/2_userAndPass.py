#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import ttk, font
import getpass

# Gestor de geometría (pack)

class Aplicacion():
    def __init__(self):
        self.raiz = Tk()
        self.raiz.title("Acceso")

        fuente = font.Font(weight='bold')
        self.etiq1 = ttk.Label(self.raiz, text="Usuario:", font=fuente)
        self.etiq2 = ttk.Label(self.raiz, text="Contraseña:", font=fuente)

        self.usuario = StringVar()
        self.clave = StringVar()

        # Realiza una lectura del nombre de usuario que
        # inició sesión en el sistema y lo asigna a la
        # variable 'self.usuario'
        self.usuario.set(getpass.getuser())

        # Cajas de Usuario y contraseña
        self.ctext1 = ttk.Entry(self.raiz, textvariable=self.usuario, width=30)
        self.ctext2 = ttk.Entry(self.raiz, textvariable=self.clave, width=30, show="*")
        self.separ1 = ttk.Separator(self.raiz, orient=HORIZONTAL)

        # Botones Aceptar y Cancelar
        self.boton1 = ttk.Button(self.raiz, text="Aceptar", command=self.aceptar)
        self.boton2 = ttk.Button(self.raiz, text="Cancelar", command=quit)

        # Se definen las posiciones de los widgets dentro de
        # la ventana. Todos los controles se van colocando
        # hacia el lado de arriba, excepto, los dos últimos,
        # los botones, que se situarán debajo del último 'TOP':
        # el primer botón hacia el lado de la izquierda y el
        # segundo a su derecha.
        # Los valores posibles para la opción 'side' son:
        # TOP (arriba), BOTTOM (abajo), LEFT (izquierda)
        # y RIGHT (derecha). Si se omite, el valor será TOP
        # La opción 'fill' se utiliza para indicar al gestor
        # cómo expandir/reducir el widget si la ventana cambia
        # de tamaño. Tiene tres posibles valores: BOTH
        # (Horizontal y Verticalmente), X (Horizontalmente) e
        # Y (Verticalmente). Funcionará si el valor de la opción
        # 'expand' es True.
        # Por último, las opciones 'padx' y 'pady' se utilizan
        # para añadir espacio extra externo horizontal y/o
        # vertical a los widgets para separarlos entre sí y de
        # los bordes de la ventana. Hay otras equivalentes que
        # añaden espacio extra interno: 'ipàdx' y 'ipady':
        self.etiq1.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)
        self.ctext1.pack(side=TOP, fill=X, expand=True, padx=5, pady=5)
        self.etiq2.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)
        self.ctext2.pack(side=TOP, fill=X, expand=True, padx=5, pady=5)
        self.separ1.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)
        self.boton1.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)
        self.boton2.pack(side=RIGHT, fill=BOTH, expand=True, padx=5, pady=5)

        self.ctext2.focus_set()
        self.raiz.mainloop()

    # Comprueba si la contraseña introducida es correcta
    def aceptar(self):
        if self.clave.get() == 'tkinter':
            print("Acceso permitido")
            print("Usuario:   ", self.ctext1.get())
            print("Contraseña:", self.ctext2.get())
        else:
            print("Acceso denegado")
            self.clave.set("")
            self.ctext2.focus_set()

def main():
    mi_app = Aplicacion()
    return 0

if __name__ == '__main__':
    main()
