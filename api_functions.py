# FUNCIONES A UTILIZAR EN app.py

# Importaciones
import pandas as pd
import numpy as np


# Datos a usar

df_developer = pd.read_parquet('Datasets/def_developer.parquet')
df_user_data_final = pd.read_parquet('Datasets/def_user_data.parquet')
df_user_genre = pd.read_parquet('Datasets/def_user_for_genre.parquet')
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
                        <a href="http://127.0.0.1:8000/docs">AQUÍ</a>
                    </botton></span> para ser redirigido a la API</p>
                </div>
            </main>
            
        </body>
    </html>
    '''


def developer(desarrolladora):
    developer_filtrado = df_developer[df_developer['developer'] == desarrolladora]
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



def user_data(usuario):
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




def user_for_genre(genero):
    df=pd.DataFrame(df_user_genre)
    
    # Filtrar por género
    df_genero = df[df['genres'] == genero]

    # Usuario con más horas jugadas por género
    usuario_mas_horas = df_genero.groupby('user_id')['playtime_forever'].sum().idxmax()
    usuario_mas_horas_df = df_genero[df_genero['user_id'] == usuario_mas_horas].iloc[0]

    # Filtrar por el usuario con más horas jugadas y calcular las horas jugadas por año de lanzamiento
    df_usuario_mas_horas = df_genero[df_genero['user_id'] == usuario_mas_horas]
    horas_por_anio = df_usuario_mas_horas.groupby('release_year')['playtime_forever'].sum().to_dict()

    return {"Usuario con más horas jugadas por género": usuario_mas_horas_df['user_id'], 
            "Género": usuario_mas_horas_df['genres'], 
            "Horas jugadas por año de lanzamiento" : horas_por_anio}



def best_developer_year(year):
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
