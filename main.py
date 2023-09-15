from fastapi import FastAPI
from pydantic import BaseModel
import json

app = FastAPI()

# Nombre del archivo JSON
json_filename = "empleados.json"

# Función para cargar los datos desde el archivo JSON al inicio
def cargar_empleados():
    try:
        with open(json_filename, "r") as file:
            empleados = json.load(file)
    except FileNotFoundError:
        empleados = []
    return empleados

# Función para guardar los datos en el archivo JSON
def guardar_empleados(empleados):
    with open(json_filename, "w") as file:
        json.dump(empleados, file, default=lambda x: x.__dict__, indent=4)

# Simulación de una base de datos temporal para almacenar empleados
empleados_db = cargar_empleados()

class Empleado(BaseModel):
    nombre: str
    apellido: str
    id: int
    cursos: list

# Para agregar un empleado
@app.post("/empleados/")
async def crear_empleado(empleado: Empleado):
    empleados_db.append(empleado)
    guardar_empleados(empleados_db)
    return empleado

# Para obtener un empleado por ID
@app.get("/empleados/{empleado_id}")
async def obtener_empleado(empleado_id: int):
    for empleado in empleados_db:
        if empleado.id == empleado_id:
            return empleado
    return "Empleado no encontrado"

# Para actualizar un empleado por ID
@app.put("/empleados/{empleado_id}")
async def actualizar_empleado(empleado_id: int, empleado_actual: Empleado):
    for i, empleado in enumerate(empleados_db):
        if empleado.id == empleado_id:
            empleados_db[i] = empleado_actual
            guardar_empleados(empleados_db)
            return {"message": "Empleado actualizado"}
    return "Empleado no encontrado"

# Para listar todos los empleados
@app.get("/empleados/")
async def listar_empleados():
    return empleados_db

# Para eliminar un empleado por ID
@app.delete("/empleados/{empleado_id}")
async def borrar_empleado(empleado_id: int):
    for i, empleado in enumerate(empleados_db):
        if empleado.id == empleado_id:
            del empleados_db[i]
            guardar_empleados(empleados_db)
            return {"message": "Empleado eliminado"}
    return "Empleado no encontrado"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)