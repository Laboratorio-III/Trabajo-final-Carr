from tkinter import *
from tkinter import ttk
from tinydb import TinyDB, Query
import datetime as dt
from tkinter import messagebox


# Clases papu

class Tareas:
    def __init__(self, id, titulo, descripcion, estado, creada, actualizada):
        self.id = id
        self.titulo = titulo
        self.descripcion = descripcion
        self.estado = estado
        self.creada = creada
        self.actualizada = actualizada

class AdminTarea:
    def __init__(self):
        self.db = TinyDB('db.json')
        self.tabla_tareas = self.db.table('tareas')
    
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
        print(f'Tarea con ID {tarea_id} agregada exitosamente.')

    def eliminarTarea(self):
        tarea_id = int(input('Ingrese el ID de la tarea que desea eliminar: '))
        tarea_query = Query()
        tarea_dict = self.tabla_tareas.get(tarea_query.id == tarea_id)
        if tarea_dict:
            self.tabla_tareas.remove(tarea_query.id == tarea_id)
            print('Tarea eliminada exitosamente.')
        else:
            print('No se encontró ninguna tarea con el ID especificado.')

# Fin clases

# Funcionalidad de los botones, codigos y etc

class Ventana(Frame):
    def __init__(self, master=None):
        super().__init__(master, width=590, height=300) 
        self.master = master
        self.pack()
        self.create_widgets()

        self.admin_tarea = AdminTarea()

    def limpiarCajas(self):
        self.texto1.delete(0, END)
        

    def fNuevo(self):
        ventana_nueva = Toplevel()
        ventana_nueva.geometry("400x300")
        ventana_nueva.title("Crear ID")
        ventana_nueva.configure(bg="#141b23")

        etiqueta2 = Label(ventana_nueva,text="Agregue Descripción", bg="#141b23", fg="white")
        etiqueta2.pack()
        self.texto2 = Entry(ventana_nueva)
        self.texto2.pack()

        etiqueta3 = Label(ventana_nueva,text="Estado", bg="#141b23", fg="white")
        etiqueta3.pack()
        self.texto3 = Entry(ventana_nueva)
        self.texto3.pack()

        etiqueta4 = Label(ventana_nueva,text="Titulo", bg="#141b23", fg="white")
        etiqueta4.pack()
        self.texto4 = Entry(ventana_nueva)
        self.texto4.pack()

        self.btnGuardar = Button(ventana_nueva, text="Guardar", command=self.fGuardar, bg="green", fg="white", bd=6)
        self.btnGuardar.place(x=10, y=190)

        self.btnCancelar = Button(ventana_nueva, text="Cancelar", command=self.fCancelar, bg="red", fg="white", bd=6)
        self.btnCancelar.place(x=80, y=190)
        pass

   
    def fBuscar(self):
        ventana_nueva = Toplevel()
        ventana_nueva.geometry("400x300")
        ventana_nueva.title("Resultado de búsqueda")
        ventana_nueva.configure(bg="#FFFFFF")

        lbl_id = Label(ventana_nueva, text="Ingrese ID:")
        lbl_id.pack()

        entry_id = Entry(ventana_nueva)
        entry_id.pack()

        btn_buscar = Button(ventana_nueva, text="Buscar", command=lambda: self.mostrarResultado(entry_id.get()))
        btn_buscar.pack()

        
    def mostrarResultado(self, tarea_id):
        tarea = self.admin_tarea.tabla_tareas.get(Query().id == int(tarea_id))

        if tarea is not None:
            self.grid.delete(*self.grid.get_children())  # Borra los datos existentes en el Treeview

            self.grid.insert("", "end", text=tarea['id'], values=(tarea['titulo'], tarea['descripcion'], tarea['estado'], tarea['creada'], tarea['actualizada']))
        
    def fEliminar(self):
        ventana_nueva = Toplevel()
        ventana_nueva.geometry("400x300")
        ventana_nueva.title("Eliminar tarea")
        ventana_nueva.configure(bg="#FFFFFF")

        lbl_id = Label(ventana_nueva, text="Ingrese ID:")
        lbl_id.pack()

        entry_id = Entry(ventana_nueva)
        entry_id.pack()

        btn_eliminar = Button(ventana_nueva, text="Eliminar", command=lambda: self.eliminarTarea(entry_id.get(), ventana_nueva))
        btn_eliminar.pack()

    def eliminarTarea(self, tarea_id, ventana_nueva):
        tarea = self.admin_tarea.tabla_tareas.get(Query().id == int(tarea_id))

        if tarea is not None:
            confirmacion = messagebox.askyesno("Confirmar eliminación", f"¿Estás seguro de eliminar la tarea con ID {tarea_id}?")

            if confirmacion:
                self.admin_tarea.tabla_tareas.remove(Query().id == int(tarea_id))
                messagebox.showinfo("Eliminación exitosa", f"La tarea con ID {tarea_id} ha sido eliminada exitosamente.")
            else:
                messagebox.showinfo("Eliminación cancelada", f"No se eliminó la tarea con ID {tarea_id}.")

            self.mostrarResultado(tarea_id)
        else:
            messagebox.showinfo("Error", f"No se encontró ninguna tarea con el ID {tarea_id}.")

        ventana_nueva.destroy()


    def fGuardar(self):
        admin_tarea = AdminTarea()
        titulo = self.texto4.get()
        descripcion = self.texto2.get()
        admin_tarea.agregar_tarea(titulo, descripcion)
        self.limpiarCajas()
        self.texto1.focus()
        messagebox.showinfo("Guardado exitoso", "Se ha guardado el ID exitosamente.")


    def fCancelar(self):
        self.limpiarCajas()
        self.texto1.focus()

    # Fin de las Funcionalidades de los botones y etc

    # Diseño de la ventana de inicio 

    def create_widgets(self):
        frame1 = Frame(self, bg="#141b23")
        frame1.place(x=0, y=0, width=93, height=300)

        # Botones de Nuevo, Buscar, Eliminar.

        self.btnNuevo = Button(frame1, text="Nuevo", command=self.fNuevo, bg="grey", fg="white", bd=6)
        self.btnNuevo.place(x=5, y=20, width=80, height=30)

        self.btnBuscar = Button(frame1, text="Buscar", command=self.fBuscar, bg="grey", fg="white", bd=6)
        self.btnBuscar.place(x=5, y=60, width=80, height=30)

        self.btnEliminar = Button(frame1, text="Eliminar", command=self.fEliminar, bg="grey", fg="white", bd=6)
        self.btnEliminar.place(x=5, y=100, width=80, height=30)

        # Fin de botones Nuevo, Buscar, Eliminar.

        frame2 = Frame(self, bg="#d3dde3")
        frame2.place(x=95, y=0, width=150, height=300)

        etiqueta1 = Label(frame2, text="Ingrese ID", bg="#d3dde3")
        etiqueta1.place(x=50, y=20)
        self.texto1 = Entry(frame2)
        self.texto1.place(x=15, y=40)

        btnAutenticar = Button(frame2, text="Iniciar")
        btnAutenticar.place(x=35, y=80, width=80)


        self.grid = ttk.Treeview(self, columns=("col1", "col2", "col3", "col4"))

        self.grid.column("#0", width=50)
        self.grid.column("col1", width=60, anchor=CENTER)
        self.grid.column("col2", width=60, anchor=CENTER)
        self.grid.column("col3", width=60, anchor=CENTER)
        self.grid.column("col4", width=60, anchor=CENTER)

        self.grid.heading("#0", text="ID")
        self.grid.heading("col1", text="Col1")
        self.grid.heading("col2", text="Col2")
        self.grid.heading("col3", text="Col3")
        self.grid.heading("col4", text="Col4")

        self.grid.place(x=260, y=40)

def main():
    root = Tk()
    root.wm_title("Trabajo Final")
    app = Ventana(root)
    app.mainloop()

if __name__ == "__main__":
    main()
