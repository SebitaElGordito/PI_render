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


@app.get(path = '/developer',
          description = """ <font color="blue">
                        1. Haga clik en "Try it out".<br>
                        2. Ingrese el nombre del desarrollador en el box abajo.<br>
                        3. Scrollear a "Resposes" para ver la cantidad de items y porcentaje de contenido Free por año de ese desarrollador.
                        </font>
                        """,
         tags=["Consultas"])
def developer(desarrollador: str = Query(..., 
                            description="Desarrollador del videojuego")):
    return api_functions.developer(desarrollador)


@app.get('/user_data', description="""INSTRUCCIONES<br>1. Haga clic en "Try it out".<br>2. Ingrese el user_id en el box abajo.<br>3. Scrollear a "Responses" para ver la cantidad de dinero gastado por el usuario, el porcentaje de recomendación que realizó el usuario y cantidad de items que tiene en su biblioteca de juegos.""", tags=["Consultas"])
def user_data(usuario: str = Query(..., description="Id del usuario")):
    return api_functions.user_data(usuario)
    

@app.get(path = '/user_for_genre',
          description = """ <font color="blue">
                        INSTRUCCIONES<br>
                        1. Haga clik en "Try it out".<br>
                        2. Ingrese el género en el box abajo.<br>
                        3. Scrollear a "Responses" para ver Top 5 de usuarios con más horas de juego en el género dado, y una lista de horas jugadas por año de lanzamiento.
                        </font>
                        """,
         tags=["Consultas"])
def user_for_genre(genero: str = Query(..., 
                            description="Género del videojuego")):
    return api_functions.user_for_genre(genero)

    
@app.get(path = '/best_developer_year',
          description = """ <font color="blue">
                        INSTRUCCIONES<br>
                        1. Haga clik en "Try it out".<br>
                        2. Ingrese el año, entre 1988 y 2017, en el box de abajo.<br>
                        3. Scrollear a "Responses" para ver el top 3 desarrolladoras con mas recomendaciones por usuarios.
                        </font>
                        """,
         tags=["Consultas"])
def best_developer_year(year: int = Query(..., 
                                description="Año de lanzamiento")):
    return api_functions.best_developer_year(year)


@app.get('/developer_reviews_analisis',
         description=""" <font color="blue">
                    INSTRUCCIONES<br>
                    1. Haga clik en "Try it out".<br>
                    2. Ingrese una desarrolladora en el box abajo.<br>
                    3. Scrollear a "Responses" para ver la cantidad de recomendaciones positivas y negativas de los usuarios para esa desarrolladora.
                    </font>
                    """,
         tags=["Consultas"])
def developer_reviews_analysis(developer: str = Query(..., 
                                         description="Nombre de desarrolladora")):
    return api_functions.developer_reviews_analysis(developer)


@app.get('/recomendacion_juego',
         description=""" <font color="blue">
                    INSTRUCCIONES<br>
                    1. Haga clik en "Try it out".<br>
                    2. Ingrese el item_id del juego en el box abajo.<br>
                    3. Scrollear a "Responses" para ver la lista de 5 juegos recomendados.
                    </font>
                    """,
         tags=["Recomendación"])
def recomendacion_juego(id_producto: int = Query(..., 
                                         description="Juego a partir del cuál se hace la recomendación de otros juego")):
    return api_functions.recomendacion_juego(id_producto)