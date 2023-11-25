"""
modelo.py:
    Módulo que contiene la lógica del programa.
"""

import re
import sqlite3
from tkinter import messagebox
from decoradores import registrar_log
from observador import Sujeto


class Abm(Sujeto):
    """
    Clase que contiene:
    - Conexión a la base de datos
    - ABM de registros de la base de datos.
    - Actualiza y limpia el treeview.
    - Base de datos:
        veterinaria.db
        campos:
            - id: llave primaria
            - nombre: string no nulo
            - tipo: string
            - raza: string
            - peso: integer
    """

    def __init__(
        self,
    ):
        try:
            con = sqlite3.connect("veterinaria.db")
            cursor = con.cursor()
            sql = """CREATE TABLE IF NOT EXISTS animales
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre varchar(20) NOT NULL,
                tipo varchar(10),
                raza varchar(20),
                peso real)
        """
            cursor.execute(sql)
            con.commit()
        except:
            print("Error de conexion")

    def conexion(
        self,
    ):
        con = sqlite3.connect("veterinaria.db")
        return con

    ###################### ABM #########################################

    @registrar_log("alta")
    def alta(self, nombre, tipo, raza, peso, tree, e_nombre, e_raza, e_peso, e_tipo):
        """
        Realiza el alta en la base de datos y actualiza el treeview. Valida el nombre, si existe y si comienza con mayúuscula y el peso, que sea un número

        :param nombre, tipo, raza, peso: valores ingresados por el usuario
        :param tree: el treeview
        :param e_nombre, e_raza, e_peso, e_tipo: entry type de la vista
        :returns: nueva fila en bd, nueva vista en treeview y mensaje de éxito o error según el caso
        """
        patron_nombre = re.compile(r"[A-Z][a-z]")
        patron_peso = re.compile(r"[^0-9]")
        if nombre == "":
            messagebox.showerror("ERROR", "El nombre es obligatorio")
        elif re.match(patron_peso, peso):
            messagebox.showerror("ERROR", "El peso debe ser un número")
        elif re.match(patron_nombre, nombre):
            con = self.conexion()
            cursor = con.cursor()
            data = (nombre, tipo, raza, peso)
            sql = "INSERT INTO animales(nombre, tipo, raza, peso) VALUES(?, ?, ?, ?)"
            cursor.execute(sql, data)
            con.commit()
            self.actualizar_treeview(tree)
            self.notificar(nombre, tipo, raza, peso)
            messagebox.showinfo("Éxito", "El alta fue exitosa")
            self.limpia_entry(e_nombre, e_raza, e_peso, e_tipo)

        else:
            messagebox.showerror("ERROR", "El nombre debe empezar en mayúscula")

    @registrar_log("baja")
    def borrar(self, tree):
        """
        Realiza la baja en la base de datos y actualiza el treeview.

        :param tree: el treeview
        :returns: nueva vista en treeview y mensaje de éxito o error según el caso
        """
        try:
            valor = tree.selection()
            item = tree.item(valor)
            mi_id = item["text"]
            con = self.conexion()
            cursor = con.cursor()
            data = (mi_id,)
            sql = "DELETE FROM animales WHERE id = ?;"
            cursor.execute(sql, data)
            con.commit()
            tree.delete(valor)
            messagebox.showinfo("Éxito", "La baja fue exitosa")
        except:
            messagebox.showerror("ERROR", "Primero debe seleccionar un item")

    def ver_elemento(self, tree, var_nombre, var_peso, var_raza, var_tipo, boton_alta):
        """
        Selecciona un elemento del treeview, lo busca en la base de datos y completa los campos
            correspondientes, también desactiva el botón para dar de alta un registro para
            evitar un alta accidental.

        :param tree: el treeview
        :param var_nombre, var_raza, var_peso, var_tipo: variables de la vista
        :param boton_alta: botón de alta en la vista
        :returns: los campos completos para la vista o mensaje de error si no se selecciono nada
        """
        try:
            valor = tree.selection()
            boton_alta.config(
                state="disabled",
            )
            item = tree.item(valor)
            mi_id = item["text"]
            con = self.conexion()
            cursor = con.cursor()
            data = (mi_id,)
            sql = "Select * FROM animales WHERE id = ?;"
            cursor.execute(sql, data)
            rows = cursor.fetchall()
            for row in rows:
                print(row)
            var_nombre.set(row[1])
            var_tipo.set(row[2])
            var_raza.set(row[3])
            var_peso.set(row[4])
        except:
            messagebox.showerror("ERROR", "Primero debe seleccionar un item")

    @registrar_log("update")
    def actualizar(
        self,
        nombre,
        tipo,
        raza,
        peso,
        tree,
        e_nombre,
        e_raza,
        e_peso,
        e_tipo,
        boton_alta,
    ):
        """
        Realiza la modificación en la base de datos, actualiza el treeview y habilita el botón de alta
        Valida: el nombre, si existe
                el peso, que sea un número

        :param nombre, tipo, raza, peso: valores ingresados por el usuario
        :param tree: el treeview
        :param e_nombre, e_raza, e_peso, e_tipo: entry type de la vista
        :param boton_alta: botón de alta en la vista
        :returns: nueva vista en treeview y mensaje de éxito o error según el caso
        :regex patron_peso: El peso no debe contener caracteres no numéricos
        """
        patron_peso = re.compile(r"[^0-9]")
        if nombre == "":
            messagebox.showerror(
                "ERROR", "Primero seleccione un elemento con el boton 'Ver Fila'"
            )
        elif re.match(patron_peso, peso):
            messagebox.showerror("ERROR", "El peso debe ser un número")
        else:
            valor = tree.selection()
            item = tree.item(valor)
            mi_id = item["text"]
            con = self.conexion()
            cursor = con.cursor()
            data = (nombre, tipo, raza, peso, mi_id)
            sql = "UPDATE animales SET nombre=?, tipo=?, raza=?, peso=? WHERE id=?"
            cursor.execute(sql, data)
            con.commit()
            boton_alta.config(
                state="normal",
            )
            self.actualizar_treeview(tree)
            messagebox.showinfo("Éxito", "La actualización fue exitosa")
            self.limpia_entry(e_nombre, e_raza, e_peso, e_tipo)

    def ver_todo(self, tree):
        """
        Realiza una búsqueda de todos los registos de la base de datos y actualiza el treeview.

        :param tree: el treeview
        :returns: nueva vista en treeview ordenada por tipo
        """
        self.limpiar_treeview(tree)
        con = self.conexion()
        cursor = con.cursor()
        sql = "SELECT * FROM animales ORDER BY tipo ASC;"
        cursor.execute(sql)
        filas = cursor.fetchall()
        for row in filas:
            print(row)
            tree.insert("", "end", text=row[0], values=(row[1], row[2], row[3], row[4]))

    def ver_orden_nombre(self, tree):
        """
        Realiza una búsqueda de todos los registos de la base de datos y actualiza el treeview.

        :param tree: el treeview
        :returns: nueva vista en treeview ordenada por nombre
        """
        self.limpiar_treeview(tree)
        con = self.conexion()
        cursor = con.cursor()
        sql = "SELECT * FROM animales ORDER BY nombre ASC;"
        cursor.execute(sql)
        filas = cursor.fetchall()
        for row in filas:
            print(row)
            tree.insert("", "end", text=row[0], values=(row[1], row[2], row[3], row[4]))

    ### Treevieww ####

    def actualizar_treeview(self, mitreeview):
        """
        Actualiza el treeview con todos los registros de la base de datos ordenados por id

        :param mitreeview: el treeview
        :returns: nueva vista en treeview ordenada por id
        """
        records = mitreeview.get_children()
        for element in records:
            mitreeview.delete(element)
        sql = "SELECT * FROM animales ORDER BY id ASC"
        con = self.conexion()
        cursor = con.cursor()
        datos = cursor.execute(sql)
        resultado = datos.fetchall()
        for fila in resultado:
            print(fila)
            mitreeview.insert(
                "", 0, text=fila[0], values=(fila[1], fila[2], fila[3], fila[4])
            )

    def limpiar_treeview(self, tree):
        """
        Elimina del treeview todos los registros

        :param tree: el treeview
        :returns: nueva vista en treeview vacía
        """
        tree.delete(*tree.get_children())

    def limpia_entry(self, nombre, raza, peso, tipo):
        """
        Elimina los datos de los campos de la vista

        :param nombre, raza, peso, tipo: variables de la vista
        """
        nombre.delete(0, "end")
        tipo.delete(0, "end")
        raza.delete(0, "end")
        peso.delete(0, "end")
