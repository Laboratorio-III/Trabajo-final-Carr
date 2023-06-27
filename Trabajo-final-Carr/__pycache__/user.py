# from pydantic import BaseModel
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from jose import jwt
# from fastapi import FastAPI, Depends, HTTPException, status
# from pydantic import BaseModel
# from administrador import administradorTarea
# from passlib.context import CryptContext
# from jose import jwt, JWTError
# Secret = "af3e251a3bdc7684f4835167aa0bfe2c80cbc9b611bf0180a078b9104ff06659"
# from datetime import datetime, timedelta
# algoritmo = "HS256"
# ACCESS_TOKEN_DURATION = 1

# crypt = CryptContext(schemes=["bcrypt"])
# # aouth2 = OAuth2PasswordBearer(tokenurl="login")
# administrador = administradorTarea

# class User(BaseModel):
#     username: str
#     pasword: str

# algoritmo = "HS256"
# ACCESS_TOKEN_DURATION = 1
# app = FastAPI()
# crypt = CryptContext(schemes=["bcrypt"])
# oaouth2 = OAuth2PasswordBearer(tokenUrl="login")
# administrador = administradorTarea

# class User(BaseModel):
#     username: str
#     password: str

# async def autenticacion_user(token:str = Depends(oaouth2)):
#     exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales de autenticacion invalidas")
#     try:
#         username = jwt.decode(token,Secret, algorithms=[algoritmo] ).get("sub")
#         if username is None:
#             raise exception
        
#         return username
#     except JWTError:
#          raise exception
         



# async def current_user(user:User = Depends(autenticacion_user)):
#         administrador = administradorTarea('admintareas.db')
#         user =administrador.buscarUser(user.username)
#         if not user:
#                 raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales de autenticacion invalidas")
#         return user
# @app.post("/login")
# async def login(form: OAuth2PasswordRequestForm = Depends()):
#     administrador = administradorTarea('admintareas.db')
#     username = form.username
    
#     usuario = administrador.buscarUser(username)  # Asegúrate de pasar el argumento 'username'
#     user = User(username=usuario[0], password=usuario[1])
    
#     if not usuario:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
    
#     crypt.verify(form.password, usuario[1])
    
#     if not crypt.verify(form.password, usuario[1]):
#         if not usuario:
#             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
    
#     access_token = {"sub": user.username, "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)}
#     return {"access_token": jwt.encode(access_token, Secret, algorithm=algoritmo), "token_type": "bearer"}

# @app.get("user/me")
# async def me(user:User = Depends(current_user)):
#     if user:
#          return user
#     else:
#          return {"mensaje":"No hay"}