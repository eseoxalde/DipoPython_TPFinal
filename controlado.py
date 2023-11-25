"""
controlado.py:
    Módulo principal:
"""
from tkinter import Tk
from vista import Mi_vista
import observador

__author__ = "Ese Kai Oxalde"
__maintainer__ = "Ese Kai Oxalde"
__email__ = "ese.oxalde@gmail.com"
__version__ = "0.1"


class Controller:
    """
    Clase responsable de crear la ventana de la interfaz gráfica,
    gestionar la interacción con la vista y setear el observador concreto.
    """

    def __init__(self, master):
        self.root_controller = master
        self.objeto_vista = Mi_vista(self.root_controller)
        self.el_observador = observador.ConcreteObservaorA(self.objeto_vista.objeto_abm)


if __name__ == "__main__":
    master = Tk()
    mi_app = Controller(master)
    master.mainloop()
