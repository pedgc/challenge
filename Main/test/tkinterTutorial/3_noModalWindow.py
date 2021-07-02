#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import ttk

class Aplicacion():

    ventana = 0
    posx_y = 0

    def __init__(self):

        self.raiz = Tk()

        # Ventana 300x200, coordenada x=500,y=50
        self.raiz.geometry('300x200+500+50')
        self.raiz.resizable(0,0)
        self.raiz.title("Ventana de aplicación")

        boton = ttk.Button(self.raiz, text='Abrir', command=self.abrir)
        boton.pack(side=BOTTOM, padx=20, pady=20)
        self.raiz.mainloop()

    def abrir(self):

        # Define una nueva ventana de diálogo
        self.dialogo = Toplevel()

        # Incrementa en 1 el contador de ventanas
        Aplicacion.ventana+=1

        # Recalcula posición de la ventana
        Aplicacion.posx_y += 50
        tamypos = '200x100+'+str(Aplicacion.posx_y)+'+'+ str(Aplicacion.posx_y)
        self.dialogo.geometry(tamypos)
        self.dialogo.resizable(0,0)

        # Obtiene identicador de la nueva ventana
        ident = self.dialogo.winfo_id()

        # Construye mensaje de la barra de título
        titulo = str(Aplicacion.ventana)+": "+str(ident)
        self.dialogo.title(titulo)

        # Define el botón 'Cerrar'
        boton = ttk.Button(self.dialogo, text='Cerrar', command=self.dialogo.destroy)
        boton.pack(side=BOTTOM, padx=20, pady=20)

        # Cuando la ejecución del programa llega a este
        # punto se utiliza el método wait_window() para
        # esperar que la ventana 'self.dialogo' sea
        # destruida.
        # Mientras tanto se atiende a los eventos locales
        # que se produzcan, por lo que otras partes de la
        # aplicación seguirán funcionando con normalidad.
        # Si hay código después de esta línea se ejecutará
        # cuando la ventana 'self.dialogo' sea cerrada.
        self.raiz.wait_window(self.dialogo)

def main():
    mi_app = Aplicacion()
    return(0)

if __name__ == '__main__':
    main()
