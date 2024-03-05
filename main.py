# Importaciones
from fastapi import FastAPI
from fastapi.responses import HTMLResponse 
import pandas as pd

df_developer = pd.read_parquet('Datasets/def_developer.parquet')
df_user_data_final = pd.read_parquet('Datasets/def_user_data.parquet')
df_best_developer = pd.read_parquet('Datasets/def_best_developer_year.parquet')


def presentacion():
    return '''
    <html>
        <head>
            <title>API Steam</title>
            <style>
                body {
                    font-family: 'Montserrat', sans-serif;
                    position: center;
                    text-align: center;
                }
                h1 {
                    color: #9c6e12;
                    font-size: 60px;
                    text-align: center;
                    text-shadow: 3px 3px 5px #aaaaaa;
                    margin-top: 15px;
                }
                .texto {
                    color: #9c6e12;
                    text-align: center;
                    font-size: 30px;

                    
                }
                .boton{
                    margin-top: 500px;
                    color: #9c6e12;
                    text-align: center;
                    font-size: 36px;
                }
                
            </style>
        </head>
        <body>
           
            <h1>CONSULTAS API EN STEAM</h1>
            <main>
                <div class="texto">
                    <p>Bienvenido a la API de Steam donde se pueden hacer diferentes consultas sobre la plataforma de videojuegos.</p>
                </div>
                <div class="boton">
                    <p>INSTRUCCIONES:</p>
                    <p>Presione <span style="color: #9c6e12; font-size: 50px "><botton class="boton">
                        <a href="https://pi-render-tt44.onrender.com/docs">AQUÍ</a>
                    </botton></span> para ser redirigido a la API</p>
                </div>
            </main>
            
        </body>
    </html>
    '''


def develop(desarrollador):
    developer_filtrado = df_developer[df_developer['developer'] == desarrollador]
    cantidad_anio = developer_filtrado.groupby('release_year')['item_id'].count()
    gratis_anio = (developer_filtrado[developer_filtrado['price'] == 0.0].groupby('release_year')['item_id'].count() / cantidad_anio * 100).fillna(0).astype(int)

    # Convertir los valores de las Series a listas
    cantidad_anio_list = cantidad_anio.tolist()
    gratis_anio_list = gratis_anio.tolist()

    # Convertir los índices a una lista
    anios_list = cantidad_anio.index.tolist()

    # Crear un diccionario con los resultados
    resultados = {
        'Año': anios_list,
        'Cantidad de juegos': cantidad_anio_list,
        '% juegos gratis': gratis_anio_list
    }

    return resultados


def userdata(usuario):
    user_filtrado = df_user_data_final[df_user_data_final['user_id'] == usuario]
    if not user_filtrado.empty:
        # Convertir los valores de NumPy a tipos nativos de Python usando int() y float()
        cantidad_dinero = int(user_filtrado['total_spent'].iloc[0])
        items_totales = int(user_filtrado['items_count'].iloc[0])
        total_recomendaciones = float(user_filtrado['recommend'].iloc[0])

        return {
            'Usuario': usuario, 
            'Cantidad de dinero gastado': cantidad_dinero, 
            'Porcentaje de recomendación': total_recomendaciones, 
            'Items totales en biblioteca': items_totales
        }
    else:
        return {'Error': 'Usuario no encontrado'}









def bestdeveloperyear(year):
    df = pd.DataFrame(df_best_developer)
    
    # Filtrar por año y recomendaciones True
    df_year = df[(df['release_year'] == year) & (df['recommend'] == True)]

    # Calcular la cantidad de recomendaciones por desarrollador
    developer_recommendations = df_year.groupby('developer')['recommend'].count().reset_index()

    # Ordenar en orden descendente y obtener el top 3
    top_developers = developer_recommendations.nlargest(3, 'recommend')

    # Crear la lista de resultados con los puestos y los desarrolladores
    resultado = [
        {"Puesto 1": top_developers.iloc[0]['developer'], "Recomendaciones": int(top_developers.iloc[0]['recommend'])},
        {"Puesto 2": top_developers.iloc[1]['developer'], "Recomendaciones": int(top_developers.iloc[1]['recommend'])},
        {"Puesto 3": top_developers.iloc[2]['developer'], "Recomendaciones": int(top_developers.iloc[2]['recommend'])},
    ]

    return resultado



# Se instancia la aplicación
app = FastAPI()

# Funciones
@app.get(path="/", 
         response_class=HTMLResponse,
         tags=["Home"])
def home():
    return presentacion()


@app.get(path = '/developer')
def developer(desarrollador: str):
    return develop(desarrollador)

@app.get('/user_data')
def user_data(usuario: str):
    return userdata(usuario)
    








@app.get(path = '/best_developer_year')
def best_developer_year(year: int):
    return bestdeveloperyear(year)