from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from modelo import *
from base_datos import *
import json
from ttkthemes import ThemedStyle
class Ventana:
    

    def __init__(self, master, nombre_base_datos):

        self.conex = ConexionSql(nombre_base_datos)
        self.conex.conectar(nombre_base_datos)
    
        # Interfaz de usuario
        master.title("Control de Stock")
        
        master.geometry("800x400")

        
            
        titulo = ttk.Label(master, text="Ingrese sus datos",anchor="center", padding=6)
        titulo.grid(row=0, column=0, columnspan=10)

        menubar=tk.Menu(master)
        menuotros=tk.Menu(menubar, tearoff=0)
        
        menuotros.add_command(label="Vaciar Base de Datos", command=lambda:FuncionesVentana.vaciar_base_datos(self))
        menuotros.add_command(label="Salir", command=lambda:FuncionesVentana.salir_aplicacion(self, master))
        menubar.add_cascade(label="Otros",menu=menuotros )

        menubase=tk.Menu(menubar, tearoff=0)
        menubase.add_command(label="Borrar campos", command=lambda:FuncionesVentana.limpiar_campos(self))
        menubar.add_cascade(label="Campos de Datos",menu=menubase )

        master.config(menu=menubar)

        # Variables de control para los Entry widgets

        self.nombre_var = StringVar()
        self.precio_var = IntVar()
        self.cantidad_var = IntVar()

        # Etiquetas y Entry para ingresar datos
        self.label_1 = ttk.Label(master, text="Nombre:").grid(row=1, column=1, pady=5, padx=5)
        self.nombre_entry = tk.Entry(master, textvariable=self.nombre_var)
        self.nombre_entry.grid(row=1, column=2, pady=5, padx=5)
        
        self.label_2=ttk.Label(master, text="Precio:").grid(row=2, column=1, pady=5, padx=5)
        self.precio_entry = tk.Entry(master, textvariable=self.precio_var)
        self.precio_entry.grid(row=2, column=2, pady=5, padx=5)

        self.label_3=ttk.Label(master, text="Cantidad:").grid(row=3, column=1, pady=5, padx=5)
        self.cantidad_entry = tk.Entry(master, textvariable=self.cantidad_var)
        self.cantidad_entry.grid(row=3, column=2, pady=5, padx=5)

        # self.Treeview para mostrar datos
        self.tree = ttk.Treeview(master, columns=("ID", "Nombre", "Precio", "Cantidad", "Valor", "Fecha"), show="headings")
        self.tree.column("ID", width=50, minwidth=100, anchor= W)
        self.tree.column("Nombre", width=100, minwidth=100)
        self.tree.column("Precio", width=100, minwidth=100)
        self.tree.column("Cantidad", width=100, minwidth=100)
        self.tree.column("Valor", width=100, minwidth=100)
        self.tree.column("#0", width=100, minwidth=100, anchor=E)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Precio", text="Precio")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.heading("Valor", text="Valor")
        self.tree.heading("Fecha", text="Fecha")
        self.tree.grid(row=9, column=0, columnspan=6, pady=10, padx=10)

        # Botones de acciones
        self.boton_crear=ttk.Button(master, text="Crear Registro",  command=lambda:Crud.crear(self, self.tree, self.nombre_var.get(), self.precio_var.get(), self.cantidad_var.get())).grid(row=5, column=1)
        self.boton_actual=ttk.Button(master, text="Actualizar Vista", command=lambda:Crud.actualizar(self, self.tree)).grid(row=5, column=2)
        self.boton_modif=ttk.Button(master, text="Modificar", command=lambda:Crud.modificar(self, self.tree, self.nombre_var.get(), self.precio_var.get(), self.cantidad_var.get())).grid(row=5, column=3)
        self.boton_baja=ttk.Button(master, text="Eliminar", command=lambda:Crud.eliminar(self, self.tree)).grid(row=5, column=4)
        self.boton_mostrar=ttk.Button(master, text="Mostrar", command=lambda:FuncionesVentana.leer_producto(self)).grid(row=2, column=3)

        # Función para cambiar el tema con decorador

        def decorador_cambiar_tema(funcion):
            def wrapper(*args):
                messagebox.askquestion("Cambiar tema", "¿Desea cambiar el tema?")
                self.estilo.theme_use(self.combo_theme.get())
                print("La ventana cambio de tema a: ", self.combo_theme.get())
                return funcion(*args)
            return wrapper
        
        @decorador_cambiar_tema
        def cambiar_tema(self, master):
            tema_seleccionado = self.combo_theme.get()
            self.estilo.theme_use(tema_seleccionado)
            master.configure(bg=self.colores_fondo.get(tema_seleccionado, "white"))

        self.estilo = ThemedStyle(master)

        # Obtener la lista de temas disponibles
        temas_disponibles = self.estilo.theme_names()

        # Crear una lista desplegable para seleccionar el tema
        self.combo_theme = ttk.Combobox(master, values=temas_disponibles)
        self.combo_theme.grid(row=1, column=5)
        self.combo_theme.current(0)  # Selecciona el primer tema por defecto

        # Botón para cambiar el tema
        boton_cambiar_tema = ttk.Button(master, text="Cambiar Tema", command=lambda:cambiar_tema(self, master))
        boton_cambiar_tema.grid(row=2, column=5)

    colores_fondo = {
            "clam": "#dbdbdb",
            "alt": "#f0f0f0",
            "default": "#f0f0f0",
            "classic": "#d9d9d9",
            "winnative": "#ececec",
            "vista": "#d2d2d2",
            "xpnative": "#d2d2d2",
            "aquativo": "#d6e9f8",
            "arc": "#dae3f0",
            "black": "#b5b5b5",
            "blue": "#c8d7e1",
            "clearlooks": "#e5e5e5",
            "keramik": "#dcdcdc",
            "plastik": "#f5f5f5",
            "radiance": "#ededed",
            "scid themes": "#f4f4f4",
            "breeze": "#deeaf5",
            "equilux": "#2c3e50",
            "kroc": "#ff6961",
            "scid": "#ffdd54",
            "adapta": "#b8c9ff",
            "breeze-dark": "#232629",
            "blue": "#007bff",
            "dark": "#2c3e50",
            "elegance": "#ececec",
            "itft1": "#f5f5f5",
            "plastic": "#f0f0f0",
            "winxpblue": "#ffffff",
            "vista": "#d2d2d2"
            # Puedes agregar más temas y colores aquí
        }
    
    


class FuncionesVentana:

    def salir_aplicacion(self, master): 
        valor=messagebox.askquestion("Salir","¿Deseas salir de la aplicación?")
        if valor=="yes":
            self.conex.desconectar()
            master.destroy()

    ### Decorador de limpiar campos
    def decorador_limpiar_campos(funcion):
        def wrapper(*args):
            print("------- CAMPOS VACIOS -------")
            messagebox.showinfo("Campos vacios", "Los campos estan vacios.")
            return funcion(*args)
        return wrapper
    
    @decorador_limpiar_campos
    def limpiar_campos(self):
        self.nombre_var.set("")
        self.precio_var.set("0")
        self.cantidad_var.set("0")

    def leer_producto(self):
        producto = self.tree.selection()
        if producto:
            self.item = self.tree.item(producto)
            producto_seleccionado = self.tree.item(producto, "values" )
            self.nombre_entry.delete(0,tk.END)
            self.precio_entry.delete(0,tk.END)
            self.cantidad_entry.delete(0,tk.END)
            self.nombre_entry.insert(0, producto_seleccionado[1])
            self.precio_entry.insert(0, producto_seleccionado[2])
            self.cantidad_entry.insert(0, producto_seleccionado[3])
            mensaje = {"ID": producto_seleccionado[0],
                "Nombre": producto_seleccionado[1],
                "Precio": producto_seleccionado[2],
                "Cantidad": producto_seleccionado[3],
                "Valor Total": producto_seleccionado[4]}
            contenido = "\n".join([f"{clave}: {valor}" for clave, valor in mensaje.items()])
            messagebox.showinfo("Producto Seleccionado", contenido)
            print("Campos completos")
        else:
            messagebox.showwarning("Error", "Por favor, seleccione un producto de la lista.")

    
    def vaciar_base_datos(self):
        confirm=messagebox.askquestion("Salir","¿Desea eliminar el contenido de la base de datos?")
        if confirm=="yes":
            self.conex.cursor.execute("DELETE FROM productos")
            self.conex.cursor.execute("DELETE FROM sqlite_sequence WHERE name='productos'")
            self.conex.cursor.execute("SELECT MAX(id) FROM productos")
            max_id = self.conex.cursor.fetchone()[0] or 0
            self.conex.cursor.execute("INSERT INTO sqlite_sequence (name, seq) VALUES ('productos', ?)", (max_id,))
            self.conex.conexion.commit()
            messagebox.showinfo("Base de datos", "Base de datos vaciada")
            Crud.actualizar(self, self.tree)
        else:
            messagebox.showwarning("Base de Datos", "Error! Hubo un problema al vaciar la base de datos")

    

        

            


 

    











