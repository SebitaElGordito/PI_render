# Importaciones
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
import api_functions 

# Se instancia la aplicación
app = FastAPI()

# Funciones
@app.get(path="/", 
         response_class=HTMLResponse,
         tags=["Home"])
def home():
    return api_functions.presentacion()


@app.get(path = '/developer')
def developer(desarrollador: str):
    return api_functions.developer(desarrollador)


@app.get('/user_data')
def user_data(usuario: str):
    return api_functions.user_data(usuario)
    

@app.get(path = '/user_for_genre')
def user_for_genre(genero: str):
    return api_functions.user_for_genre(genero)

    
@app.get(path = '/best_developer_year')
def best_developer_year(year: int):
    return api_functions.best_developer_year(year)


@app.get('/developer_reviews_analisis')
def developer_reviews_analysis(developer: str):
    return api_functions.developer_reviews_analysis(developer)


@app.get('/recomendacion_juego')
def recomendacion_juego(id_producto: int):
    return api_functions.recomendacion_juego(id_producto)