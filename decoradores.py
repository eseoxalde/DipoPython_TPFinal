"""
decoradores.py:
    Módulo que contiene los decoradores usados para el log
"""
import datetime


def registrar_log(tipo_registro):
    """
    Función para crear un decorador propio

    :param tipo_regstro: se utiliza para decidir que tipo de registro irá al log. Puede ser:
            update (para actualización de datos),
            alta (para un nuevo registro)
            o baja (para eliminación de un registro)
    :returns: una entrada nueva en el archivo registro:log.txt
    """

    def _registrar_log(funcion):
        def envoltura(*args, **kwargs):
            fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if tipo_registro == "update":
                frase = "Se ha actualizado el registro"
            if tipo_registro == "alta":
                frase = "Se ha ingresado un nuevo registro"
            if tipo_registro == "baja":
                frase = "Se ha eliminado un registro"
            # print(f"{fecha} - {frase}\n")
            funcion(*args, **kwargs)
            with open("registro_log.txt", "a") as archivo:
                archivo.write(f"{fecha} - {frase}\n")

        return envoltura

    return _registrar_log
