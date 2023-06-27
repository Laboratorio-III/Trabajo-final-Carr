from tareas import Tarea
# from basededatos import insertarFila, crearDB, crearTabla, traerTAREADB, traerTAREASDB, modificarValor
import sqlite3 as sql
from fastapi import HTTPException, status
from pydantic import BaseModel
import requests
import hashlib
from flask import Response
from passlib.context import CryptContext

class User(BaseModel):
    username: str
    password: str
crypt = CryptContext(schemes=["bcrypt"])
class administradorTarea:
    def __init__(self, db_file:str):
        self.db = sql.connect(db_file)

        
    def agregar_tarea(self, tarea: Tarea) -> int:
        tarea_dic = tarea.tarea_dict()
            
        conn = sql.connect('admintareas.db')
        cursor = conn.cursor()
        
        cursor.execute("""INSERT INTO tareas (id, titulo, descripcion, estado, creada, actualizada)
                        VALUES (?, ?, ?, ?, ?, ?)""", tuple(tarea_dic.values()))
        tarea_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return tarea_id
    
    def buscar_id_repetido(self, id):
    # Conectar a la base de datos
        conexion = sql.connect('admintareas.db')
        cursor = conexion.cursor()

        # Ejecutar la consulta SQL para buscar el campo "id" repetido
        
        cursor.execute("SELECT COUNT(*) FROM tareas WHERE id = ?", (id,))

        # Obtener el resultado
        resultado = cursor.fetchone()
        
        ids = resultado[0]
        
        # Cerrar la conexión a la base de datos
        conexion.close()
        
        # Verificar si el ID está repetido
        
        return ids

    def traer_tarea(self, tarea_id: int) -> Tarea:
       
        conn = sql.connect('admintareas.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tareas WHERE id=?"
        ,(tarea_id,))
        tarea = cursor.fetchone()
        conn.commit()
        conn.close()

        
        if tarea:
            # print(tarea)
            return Tarea(*tarea)
        else:
            return None

    def traer_todas_tareas(self):
        conn = sql.connect('admintareas.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tareas"
        )
        tareas = cursor.fetchall()
        conn.commit()
        conn.close()
        return tareas
    
    def eliminar_tarea(self, tarea_id: int):
        if tarea_id is None:
            raise ValueError("El ID de la tarea no puede ser nulo")

        conn = sql.connect('admintareas.db')
        cursor = conn.cursor()

        # Consultar la tarea antes de eliminarla
        cursor.execute("SELECT id FROM tareas WHERE id=?", (tarea_id,))
        tarea = cursor.fetchone()

        if tarea:
            # Guardar el ID de la tarea eliminada
            tarea_eliminada_id = tarea[0]

            # Eliminar la tarea
            cursor.execute("DELETE FROM tareas WHERE id=?", (tarea_id,))
            conn.commit()

            conn.close()
            return tarea_eliminada_id
        else:
            conn.close()
            raise HTTPException(status_code=404, detail="No se encontró la tarea")
        
    def actualizar_estado_tarea(self, tarea_id: int, estado: str, actualizada:str):
       
        conn = sql.connect('admintareas.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE tareas SET estado=?, actualizada=? WHERE id=?", (estado, actualizada, tarea_id))
        conn.commit()
        conn.close()

    def crearTabla(self):
        conn = sql.connect('admintareas.db')
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS usuarios(
                    user TEXT,
                    password TEXT
                    )""")
        conn.commit()
        conn.close()
    

    def agregarUser(self, user: User):
        conn = sql.connect('admintareas.db')
        cursor = conn.cursor()
        hashed_password = crypt.hash(user.password)
        cursor.execute("""INSERT INTO usuarios (user, password)
                        VALUES (?, ?)""", (user.username, hashed_password))
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return user_id
    
    # def buscarUser(self, username: str) -> bool:
    #     conn = sql.connect('admintareas.db')
    #     cursor = conn.cursor()

    #     cursor.execute("SELECT COUNT(*) FROM usuarios WHERE user=?", (username,))
    #     result = cursor.fetchone()

    #     conn.close()

    #     if result and result[0] > 0:
    #         return True
    #     else:
    #         return False
    
    def buscarUser(self, username: str) -> tuple:
            conn = sql.connect('admintareas.db')
            cursor = conn.cursor()

            cursor.execute("SELECT user, password FROM usuarios WHERE user=?", (username,))
            resultado = cursor.fetchone()

            conn.close()

            if resultado:
               
                return resultado  # Devuelve una tupla con el usuario y la contraseña
            else:
                
                return None 
    def eliminarUser(self, username: User):
        conn = sql.connect('admintareas.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE user=?", (username,))
        conn.commit()
        conn.close()