from fastapi import FastAPI, Query
from tinydb import TinyDB, Query
import datetime as dt
import hashlib
import threading
import tkinter as tk
from tkinter import messagebox
import uvicorn

app = FastAPI()

class Persona:
    def __init__(self, id, nombre, apellido, fecha_nacimiento, dni):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.fecha_nacimiento = fecha_nacimiento
        self.dni = dni

class Usuario(Persona):
    def __init__(self, id, nombre, apellido, fecha_nacimiento, dni, contraseña):
        super().__init__(id, nombre, apellido, fecha_nacimiento, dni)
        self.contraseña = hashlib.md5(contraseña.encode()).hexdigest()
        self.ultimo_acceso = None

    def verificar_contraseña(self, contraseña):
        return hashlib.md5(contraseña.encode()).hexdigest() == self.contraseña

class AdminTarea:
    def __init__(self):
        self.db = TinyDB('db.json')
        self.tabla_tareas = self.db.table('tareas')
        self.tabla_usuarios = self.db.table('usuarios')

    def agregar_tarea(self, titulo: str, descripcion: str):
        tarea_id = len(self.tabla_tareas) + 1
        nueva_tarea = {
            'id': tarea_id,
            'titulo': titulo,
            'descripcion': descripcion,
            'estado': 'pendiente',
            'creada': dt.datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            'actualizada': dt.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        }
        self.tabla_tareas.insert(nueva_tarea)
        return tarea_id

    def eliminar_tarea(self, tarea_id: int):
        tarea_query = Query()
        tarea_dict = self.tabla_tareas.get(tarea_query.id == tarea_id)
        if tarea_dict:
            self.tabla_tareas.remove(tarea_query.id == tarea_id)
            return True
        else:
            return False

    def agregar_usuario(self, nombre: str, apellido: str, fecha_nacimiento: str, dni: str, contraseña: str):
        usuario_id = len(self.tabla_usuarios) + 1
        nuevo_usuario = {
            'id': usuario_id,
            'nombre': nombre,
            'apellido': apellido,
            'fecha_nacimiento': fecha_nacimiento,
            'dni': dni,
            'contraseña': hashlib.md5(contraseña.encode()).hexdigest()
        }
        self.tabla_usuarios.insert(nuevo_usuario)
        return usuario_id

    def autenticar(self, usuario: str, contraseña: str):
        usuario_query = Query()
        usuario_dict = self.tabla_usuarios.get(usuario_query.nombre == usuario)
        if usuario_dict:
            usuario_obj = Usuario(**usuario_dict)
            if usuario_obj.verificar_contraseña(contraseña):
                usuario_obj.ultimo_acceso = dt.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                self.tabla_usuarios.update({'ultimo_acceso': usuario_obj.ultimo_acceso}, usuario_query.nombre == usuario)
                messagebox.showinfo("Autenticación exitosa", "Usuario autenticado correctamente.")
            else:
                messagebox.showerror("Autenticación fallida", "Contraseña incorrecta.")
        else:
            messagebox.showerror("Autenticación fallida", "Usuario no encontrado.")

admin_tarea = AdminTarea()

# Resto del código y la interfaz gráfica...

# Ventana de tkinter
def iniciar_interfaz():
    root = tk.Tk()
    root.wm_title("Trabajo Final")

    texto1 = tk.Entry(root)
    texto1.pack()

    texto2 = tk.Entry(root)
    texto2.pack()

    btn_guardar = tk.Button(root, text="Guardar", command=lambda: guardar_tarea(texto1.get(), texto2.get()))
    btn_guardar.pack()

    btn_listar = tk.Button(root, text="Listar Tareas", command=listar_tareas)
    btn_listar.pack()

    btn_autenticar = tk.Button(root, text="Autenticar", command=lambda: autenticar(texto1.get(), texto2.get()))
    btn_autenticar.pack()

    root.mainloop()

# Función para guardar tarea
def guardar_tarea(titulo, descripcion):
    tarea_id = admin_tarea.agregar_tarea(titulo, descripcion)
    messagebox.showinfo("Guardado exitoso", f"Se ha guardado el ID {tarea_id} exitosamente.")

# Función para listar tareas
def listar_tareas():
    tarea_query = Query()
    tareas = admin_tarea.tabla_tareas.all()
    tarea_list = []
    for tarea in tareas:
        tarea_list.append(f"ID: {tarea['id']}, Título: {tarea['titulo']}, Descripción: {tarea['descripcion']}, Estado: {tarea['estado']}")
    messagebox.showinfo("Tareas", "\n".join(tarea_list))

# Función para autenticar
def autenticar(usuario, contraseña):
    usuario_query = Query()
    usuario_dict = admin_tarea.tabla_usuarios.get(usuario_query.nombre == usuario)
    if usuario_dict:
        usuario_obj = Usuario(**usuario_dict)
        if usuario_obj.verificar_contraseña(contraseña):
            usuario_obj.ultimo_acceso = dt.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            admin_tarea.tabla_usuarios.update({'ultimo_acceso': usuario_obj.ultimo_acceso}, usuario_query.nombre == usuario)
            messagebox.showinfo("Autenticación exitosa", "Usuario autenticado correctamente.")
        else:
            messagebox.showerror("Autenticación fallida", "Contraseña incorrecta.")
    else:
        messagebox.showerror("Autenticación fallida", "Usuario no encontrado.")

# Hilos para ejecutar FastAPI y tkinter simultáneamente
def start_api():
    uvicorn.run(app, host="0.0.0.0", port=8000)

def start_tkinter():
    iniciar_interfaz()

if __name__ == "__main__":
    api_thread = threading.Thread(target=start_api)
    tkinter_thread = threading.Thread(target=start_tkinter)

    api_thread.start()
    tkinter_thread.start()

    api_thread.join()
    tkinter_thread.join()