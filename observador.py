"""
observador.py
    Clase para utilizar el patrón observador en el programa
"""


class Sujeto:
    observadores = []

    def agregar(self, obj):
        self.observadores.append(obj)

    def quitar(self, obj):
        pass

    def notificar(self, *args):
        for observador in self.observadores:
            observador.update(args)


class Observador:
    def update(self):
        raise NotImplementedError("Delegación de actualización")


class ConcreteObservaorA(Observador):
    """
    ConcreteObservaorA: El observador concreto
    """

    def __init__(self, obj):
        self.observador_a = obj
        self.observador_a.agregar(self)

    def update(self, *args):
        print("Actualización dentro del observador ")
        print("Acá están los parámetos: ", args)
