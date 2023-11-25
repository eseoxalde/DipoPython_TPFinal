"""
vista.py:
    Módulo que contiene la vista del programa.
"""
from tkinter import W, Button, Entry, Label, StringVar, ttk
from sympy import E
from modelo import Abm


class Mi_vista:
    """
    Clase que contiene la vista del programa
    """

    def __init__(self, window):
        """
        __init__: Dibuja la ventana con:
            los cuatro campos de entrada: nombre, tipo, raza y peso
            los seis botones: agregar, eliminar, ver_fila, actualizar, ver_todo y ver_nombre
            la grilla con los datos de la base de datos
        """
        self.master = window
        self.master.title("Veterinaria Perros y Gatos")
        self.objeto_abm = Abm()

        # Labels
        self.titulo = Label(self.master, text="Veterinaria Perros y Gatos")
        self.titulo.grid(row=0, column=1)
        self.titulo.config(fg="#196F3D", font=("Verdana", 20))
        self.nombre = Label(self.master, text="Nombre")
        self.nombre.grid(row=1, column=0, sticky=E)
        self.tipo = Label(self.master, text="Tipo")
        self.tipo.grid(row=3, column=0, sticky=E)
        self.raza = Label(self.master, text="Raza")
        self.raza.grid(row=4, column=0, sticky=E)
        self.peso = Label(self.master, text="Peso")
        self.peso.grid(row=5, column=0, sticky=E)

        # variables
        self.var_nombre = StringVar()
        self.var_tipo = StringVar()
        self.var_raza = StringVar()
        self.var_peso = StringVar()

        # campos de entrada
        self.entry_nombre = Entry(self.master, textvariable=self.var_nombre, width=50)
        self.entry_nombre.grid(row=1, column=1)
        self.entry_tipo = Entry(self.master, textvariable=self.var_tipo, width=50)
        self.entry_tipo.grid(row=3, column=1)
        self.entry_raza = Entry(self.master, textvariable=self.var_raza, width=50)
        self.entry_raza.grid(row=4, column=1)
        self.entry_peso = Entry(self.master, textvariable=self.var_peso, width=50)
        self.entry_peso.grid(row=5, column=1)

        # Campos de error en entradas
        self.e_nombre = Label(
            self.master,
            text="**El nombre es obligatorio y debe comenzar en mayúscula**",
        )
        self.e_nombre.grid(row=2, column=1, sticky=W)
        self.e_nombre.config(fg="#C0392B")
        self.e_peso = Label(self.master, text="**El peso debe ser un número**")
        self.e_peso.grid(row=6, column=1, sticky=W)
        self.e_peso.config(fg="#C0392B")

        # TreeView
        self.tree = ttk.Treeview(self.master)
        self.tree["columns"] = ("col1", "col2", "col3", "col4")
        self.tree.heading("#0", text="id", anchor=W)
        self.tree.heading("col1", text="Nombre", anchor=W)
        self.tree.heading("col2", text="Tipo", anchor=W)
        self.tree.heading("col3", text="Raza", anchor=W)
        self.tree.heading("col4", text="Peso", anchor=W)
        self.tree.column("#0", width=50, minwidth=50, anchor=W)
        self.tree.column("col1", width=80, minwidth=50, anchor=W)
        self.tree.column("col2", width=80, minwidth=50, anchor=W)
        self.tree.column("col3", width=80, minwidth=50, anchor=W)
        self.tree.column("col4", width=80, minwidth=50, anchor=W)
        self.tree.grid(column=0, row=20, columnspan=5)

        # Para cargar los datos que ya esten en la bd
        self.objeto_abm.ver_orden_nombre(self.tree)

        # botones
        self.boton_alta = Button(
            self.master,
            text="Agregar",
            background="#7DCEA0",
            command=lambda: self.objeto_abm.alta(
                self.var_nombre.get(),
                self.var_tipo.get(),
                self.var_raza.get(),
                self.var_peso.get(),
                self.tree,
                self.entry_nombre,
                self.entry_raza,
                self.entry_peso,
                self.entry_tipo,
            ),
            width=20,
        )
        self.boton_alta.grid(row=8, column=1)

        self.boton_borrar = Button(
            self.master,
            text="Eliminar",
            background="#F1948A",
            command=lambda: self.objeto_abm.borrar(self.tree),
            width=20,
        )
        self.boton_borrar.grid(row=9, column=1)

        self.e_ver = Label(
            self.master,
            text="Para ACTUALIZAR, primero seleccionar un dato de la tabla y presionar VER FILA",
        )
        self.e_ver.grid(row=10, column=0, columnspan=3)
        self.e_ver.config(fg="#34495E")
        self.e_actualizar = Label(
            self.master, text="Luego de cambiar los datos deseados presionar ACTUALIZAR"
        )
        self.e_actualizar.grid(row=11, column=1, columnspan=2)
        self.e_actualizar.config(fg="#34495E")

        self.boton_ver_fila = Button(
            self.master,
            background="#F7DC6F",
            text="Ver fila",
            command=lambda: self.objeto_abm.ver_elemento(
                self.tree,
                self.var_nombre,
                self.var_peso,
                self.var_raza,
                self.var_tipo,
                self.boton_alta,
            ),
            width=20,
        )

        self.boton_ver_fila.grid(row=12, column=1)

        self.boton_actualizar = Button(
            self.master,
            text="Actualizar",
            background="#F7DC6F",
            command=lambda: self.objeto_abm.actualizar(
                self.var_nombre.get(),
                self.var_tipo.get(),
                self.var_raza.get(),
                self.var_peso.get(),
                self.tree,
                self.entry_nombre,
                self.entry_raza,
                self.entry_peso,
                self.entry_tipo,
                self.boton_alta,
            ),
            width=20,
        )
        self.boton_actualizar.grid(row=13, column=1)

        self.boton_ver_todo = Button(
            self.master,
            background="#7FB3D5",
            text="Ver ordenado por tipo",
            command=lambda: self.objeto_abm.ver_todo(self.tree),
            width=20,
        )
        self.boton_ver_todo.grid(row=14, column=1)

        self.boton_ver_nombre = Button(
            self.master,
            background="#7FB3D5",
            text="Ver ordenado por nombre",
            command=lambda: self.objeto_abm.ver_orden_nombre(self.tree),
            width=20,
        )
        self.boton_ver_nombre.grid(row=15, column=1)
