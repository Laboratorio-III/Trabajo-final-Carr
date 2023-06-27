import tkinter as tk
from tkinter import messagebox
import requests
import json



class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ventana principal")
        self.geometry('500x600')
        self.config(bg='yellow')

        # Botones
        btn_crear_tarea = tk.Button(self, text="Crear tarea", command=self.crear_tarea)
        btn_crear_tarea.pack(pady=10)

        btn_traer_tarea = tk.Button(self, text="Traer tarea", command=self.traer_tarea)
        btn_traer_tarea.pack(pady=10)

        btn_actualizar_estado = tk.Button(self, text="Actualizar estado", command=self.actualizar_estado)
        btn_actualizar_estado.pack(pady=10)

        btn_eliminar_tarea = tk.Button(self, text="Eliminar tarea", command=self.eliminar_tarea)
        btn_eliminar_tarea.pack(pady=10)

    def crear_tarea(self):
        ventana = tk.Toplevel()
        ventana.title('Crear tarea')
        ventana.geometry("300x300")
        id_label = tk.Label(ventana, text="ID:")
        id_label.pack()

        id_entry = tk.Entry(ventana)
        id_entry.pack()

        # Etiqueta y campo de entrada para "Título"
        titulo_label = tk.Label(ventana, text="Título:")
        titulo_label.pack()

        titulo_entry = tk.Entry(ventana, width=60)
        titulo_entry.pack()

        # Etiqueta y campo de entrada para "Descripción"
        descripcion_label = tk.Label(ventana, text="Descripción:")
        descripcion_label.pack()

        descripcion_entry = tk.Entry(ventana)
        descripcion_entry.pack()

        # Etiqueta y campo de entrada para "Estado"
        estado_label = tk.Label(ventana, text="Estado:")
        estado_label.pack()

        estado_entry = tk.Entry(ventana)
        estado_entry.pack()

        def crear_tareadb():
            id_value = id_entry.get()
            titulo_value = titulo_entry.get()
            descripcion_value = descripcion_entry.get()
            estado_value = estado_entry.get()

            tarea = {
                "id": id_value,
                "titulo": titulo_value,
                "descripcion": descripcion_value,
                "estado": estado_value
            }

            response = requests.post('http://127.0.0.1:8000/tarea', json=tarea)

           

            if response.status_code == 200:
                        tarea_creada = response.json()
                        
                        messagebox.showinfo("Tarea creada", f"Tarea creada:\nID: {tarea_creada['id']}\nTítulo: {tarea_creada['titulo']}\nDescripción: {tarea_creada['descripcion']}\nEstado: {tarea_creada['estado']}")
            elif response.status_code == 422:
                        messagebox.showerror("Error", "El id debe ser un entero")
            elif response.status_code==409:
                        messagebox.showerror("Error", "Ya hay una tarea con ese id")
            elif response.status_code == 400:
                        messagebox.showerror("Error", "Campos vacios")
        

                                # Cerrar la ventana "Crear Tarea"
        btn_crear = tk.Button(ventana, text="Crear", command=crear_tareadb)
        btn_crear.pack(pady=10)
        
        

       
    def actualizar_estado(self):
   
        ventana = tk.Toplevel()
        ventana.title('Actualizar estado')
        ventana.geometry("300x300")

        def actualizar_estadodb(): 
            id = id_entry.get()
            estado = estado_entry.get()
            payload = {"id": id, "estado": estado}
            response = requests.put(f'http://127.0.0.1:8000/tarea/{id}/{estado}', json=payload)

            if response.status_code == 200:
                        messagebox.showinfo("Tarea actualizada", "Se ha actualizado la tarea")
            elif response.status_code == 404:
                        messagebox.showerror("Error", "No se encontro tarea con ese id")
            elif response.status_code == 422:
                         messagebox.showerror("Error", "El id no es un entero")
            else:
                    messagebox.showerror("Error", "No completo campo estado")

        id_label = tk.Label(ventana, text="ID:")
        id_label.pack()

        id_entry = tk.Entry(ventana)
        id_entry.pack()

        estado_label = tk.Label(ventana, text="Estado:")
        estado_label.pack()

        estado_entry = tk.Entry(ventana)
        estado_entry.pack()

        btn_actualizar = tk.Button(ventana, text="Actualizar", command=actualizar_estadodb)
        btn_actualizar.pack(pady=10)
        
    def eliminar_tarea(self):
        
        ventana = tk.Toplevel()
        ventana.title('Crear tarea')
        ventana.geometry("300x300")
        
        def eliminartarea_api(id):
            response = requests.delete(f'http://127.0.0.1:8000/tarea/{id}', json={"id": id})   
          
            
            if response.status_code == 200:
                messagebox.showinfo("Tarea eliminada", f"Tarea con {id} eliminada")
            elif response.status_code == 404: 
                messagebox.showerror("Error", "No se encontro tarea con ese id")
            elif response.status_code == 422:
                messagebox.showerror("Error", "El id debe ser un entero")
            else:
                messagebox.showerror("Error", "Complete id")
    
        id_label = tk.Label(ventana, text="ID:")
        id_label.pack()

        id_entry = tk.Entry(ventana)
        id_entry.pack()
            
        btn_eliminar = tk.Button(ventana, text="Eliminar", command=lambda: eliminartarea_api(id_entry.get()))
        btn_eliminar.pack(pady=10)
    
    def traer_tarea(self):
        ventana = tk.Toplevel()
        ventana.title('Crear tarea')
        ventana.geometry("300x300")

        def traertarea_api(id):
            response = requests.get(f'http://127.0.0.1:8000/tarea/{id}', json={"id": id})

            if response.status_code == 200:
                tarea_creada = response.json()
                messagebox.showinfo("Tarea", f"Tarea:\nID: {tarea_creada['id']}\nTítulo: {tarea_creada['titulo']}\nDescripción: {tarea_creada['descripcion']}\nEstado: {tarea_creada['estado']},\nCreada:{tarea_creada['creada']},\nActualizada: {tarea_creada['actualizada']}")
            elif response.status_code == 404:
                messagebox.showerror("Error", "No hay tarea con ese id")
            elif response.status_code == 422:
                messagebox.showerror("Error", "El id no es un entero")
            else:
                messagebox.showerror("Error", "Falta el id")
            

                 

        id_label = tk.Label(ventana, text="ID:")
        id_label.pack()

        id_entry = tk.Entry(ventana)
        id_entry.pack()
            
        btn_eliminar = tk.Button(ventana, text="Traer tarea", command=lambda: traertarea_api(id_entry.get()))
        btn_eliminar.pack(pady=10)