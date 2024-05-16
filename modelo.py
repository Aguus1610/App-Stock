import re
from peewee import *
from tkinter import messagebox
from datetime import datetime


db = SqliteDatabase("Stock.db")
class BaseModel(Model):
    class Meta:
        database = db

class Producto(BaseModel):
    nombre = CharField(unique=True)
    precio = CharField()
    cantidad = CharField()
    valor = IntegerField()
    fecha_in = DateTimeField()

db.connect()
db.create_tables([Producto])

class Crud:

    
    def __init__(self):
        pass

    def crear(self, mi_tree, nombre, precio, cantidad):
        valor = int(precio * cantidad) 

        # Validar el nombre con expresiones regulares
        if not re.match("^[a-z, ,A-Z]+$", nombre):
            messagebox.showwarning("Error", "El nombre del producto solo debe contener letras.")
            return
        
        if nombre and precio and cantidad != " ":
            self.fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
            producto=Producto()
            producto.nombre=nombre
            producto.precio=precio
            producto.cantidad=cantidad
            producto.valor=valor
            producto.fecha_in=self.fecha_actual
            producto.save()

            messagebox.showinfo("Éxito", "Producto creado correctamente.")
            Crud.actualizar(self, mi_tree)
            messagebox.showinfo("Resultados SQLite3", "Alta exitosa")
        else:
            messagebox.showwarning("Error", "Por favor, ingrese todos los campos.")

    def actualizar(self, mi_tree):

        # Limpiar el Treeview antes de cargar los nuevos datos
        records=mi_tree.get_children()
        for element in records:
            mi_tree.delete(element)

        for filas in Producto.select():
                mi_tree.insert("", 0, text=filas.id, values=(filas.id, filas.nombre, filas.precio, filas.cantidad, filas.valor, filas.fecha_in))


    def eliminar(self, mi_tree):
        elemento_seleccionado = mi_tree.selection()
        if elemento_seleccionado:
            # Eliminar el producto seleccionado
            id_seleccionado = mi_tree.item(elemento_seleccionado, 'values')[0]
            borrar = Producto.get(Producto.id == id_seleccionado)
            borrar.delete_instance()
            messagebox.showinfo("Éxito", "Producto eliminado correctamente.")
            Crud.actualizar(self, mi_tree)
        else:
            messagebox.showwarning("Error", "Seleccione un producto para eliminar.")


    
    def modificar(self, mi_tree, nombre, precio, cantidad):

        if not self.conex.cursor or not self.conex.conexion:
            messagebox.showwarning("Error", "No se puede conectar a la base de datos.")
            return

        valor = int(precio * cantidad) 
        elemento_seleccionado = mi_tree.selection()
        if not elemento_seleccionado:
            messagebox.showwarning("Error", "Seleccione un producto para actualizar.")
            return

        id_seleccionado = mi_tree.item(elemento_seleccionado, 'values')[0]

        try:
            self.fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
            modificar = Producto.update({Producto.nombre:nombre, Producto.precio:precio, Producto.cantidad:cantidad, Producto.valor:valor, Producto.fecha_in:self.fecha_actual}).where(Producto.id == id_seleccionado)
            modificar.execute()
            messagebox.showinfo("Éxito", "Producto actualizado correctamente.")
            Crud.actualizar(self, mi_tree)
        except SyntaxError:
            messagebox.showinfo("ERROR", "Hay un error de tipo 'SyntaxError' ")
        except ValueError:
            messagebox.showinfo("ERROR", "Hay un error de tipo 'ValueError' ") 




