from interfaz import VentanaPrincipal
from administrador import administradorTarea
from fastapi import FastAPI
from datos import crearTabla, crearDB
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from main import administradorTarea
from tareas import Tarea
import datetime
from uvicorn import Config, Server

import threading
class tareaApi(BaseModel):
    id: int
    titulo: str
    descripcion: str
    estado: str
    creada: str | None
    actualizada: str | None

class User(BaseModel):
    username: str
    password: str
app = FastAPI()
crearDB('admintareas.db')
crearTabla()
administrador = administradorTarea('admintareas.db')
administrador.crearTabla()

@app.post('/tarea')
def insertar_tarea(tarea: tareaApi):
    tarea_dict = dict(tarea)
    tarea_objeto = Tarea(**tarea_dict)
    
    if any(value == "" for value in tarea_dict.values()):
        raise HTTPException(status_code=400, detail="Error: Uno o más campos están vacíos.")
    
    if administrador.buscar_id_repetido(tarea_objeto.id):
        raise HTTPException(status_code=409, detail="Error: El ID de la tarea ya está repetido.")
    else:
        administrador.agregar_tarea(tarea_objeto)
        return tarea_objeto

@app.delete("/tarea/{id}")
def eliminar_tarea_endpoint(id: int):
    if id is None:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="Se requiere un ID de tarea")

    tarea_id = administrador.eliminar_tarea(id)

    if tarea_id is not None:
        return {"mensaje": f"Tarea con ID {tarea_id} eliminada"}
    else:
        raise HTTPException(status_code=404, detail="No se encontró la tarea")

@app.put('/tarea/{id}/{estado}')
def actualizarestado_api(id: int, estado: str):
    tarea_actual = administrador.traer_tarea(id)
    
    if tarea_actual:
        tarea_actual.estado = estado
        tarea_actual.actualizada = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        administrador.actualizar_estado_tarea(tarea_actual.id, tarea_actual.estado, tarea_actual.actualizada)
        return {"mensaje": f"Tarea con id {id} actualizada"}
    else:
        raise HTTPException(status_code=404, detail="No se encontró la tarea")

@app.get('/tarea/{id}')
def traertarea_api(id: int):
    tarea = administrador.traer_tarea(id)
    
    if tarea:
        return tarea
    else:
        raise HTTPException(status_code=404, detail="No se encontró la tarea con ese id")

@app.post("/user")
async def agregar_user(user: User):
    administrador = administradorTarea('admintareas.db')
    administrador.agregarUser(user)  # Asegúrate de pasar el argumento 'user'
    usuario = administrador.buscarUser(user.username)
    return {"mensaje": f"Usuario: {usuario[0]} agregado"}

def iniciar_ventana():
    ventana = VentanaPrincipal()
    ventana.mainloop()

def iniciar_servidor():
    config = Config(app="main:app", host="0.0.0.0", port=8000, reload=True)
    server = Server(config)
    server.run()

if __name__ == "__main__":
    ventana_thread = threading.Thread(target=iniciar_ventana)
    servidor_thread = threading.Thread(target=iniciar_servidor)

    servidor_thread.start()
    ventana_thread.start()