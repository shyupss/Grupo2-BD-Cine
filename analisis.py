import os
import inspect

from db_modulos.obj_sql import SqlObj
import matplotlib.pyplot as plt

class ConsultasSql:

    def __init__(self, database="db_cine", user="user_cine", password="1234", host="localhost"):
        self.obj = SqlObj(database, user, password, host)

        # Asegurar que la carpeta "graficos" exista
        os.makedirs("graficos", exist_ok=True)

    def analisis_top_10_peliculas_mas_vistas(self, anio):
        try:
            # Consulta: Top 10 películas por mayor número de ventas en el año dado
            consulta = f'''
            SELECT p.titulo,
            COUNT(*) AS ventas
            FROM hechos_boletos hb
            JOIN pelicula p ON hb.id_pelicula = p.id
            WHERE EXTRACT(YEAR FROM hb.hora_compra) = {anio}
            GROUP BY p.titulo
            ORDER BY ventas DESC
            LIMIT 10;
            '''
            
            self.obj.cur.execute(consulta)
            resultados = self.obj.cur.fetchall()
            if not resultados: raise Exception(f"No hay datos de ventas para el año {anio}.")

            # Preparar datos
            titulos, ventas = zip(*resultados)
            if not titulos or not ventas: raise Exception(f"No hay datos de generos suficientes para el año {anio}.")

            # Gráfico
            fig, ax = plt.subplots()
            ax.bar(titulos, ventas)
            ax.set_title(f"Top 10 Películas por Ventas en {anio}")
            ax.set_ylabel("Número de boletos vendidos")
            ax.set_xticklabels(titulos, rotation=45, ha="right")
            plt.tight_layout()

            # Guardar y mostrar
            ruta = f"graficos/{inspect.currentframe().f_code.co_name}_{anio}.png"
            plt.savefig(ruta)
            plt.show()
            print(f"Gráfico guardado en {ruta}")

        except Exception as e: print(f"# Error con el analisis 'top 10 peliculas mas vendidas'\nDetalle -> {e}")

    def analisis_top_10_generos_menos_vistos(self, anio):
        try:
            # Consulta: Top 10 generos por menor número de ventas en el año dado
            consulta = f'''
            SELECT p.genero, COUNT(*) AS ventas
            FROM hechos_boletos hb
            JOIN pelicula p ON hb.id_pelicula = p.id
            WHERE EXTRACT(YEAR FROM hb.hora_compra) = {anio}
            GROUP BY p.genero
            ORDER BY ventas ASC
            LIMIT 10;
            '''

            self.obj.cur.execute(consulta)
            resultados = self.obj.cur.fetchall()
            if not resultados: raise Exception(f"No hay datos de generos para el año {anio}.")

            # Preparar datos
            generos, ventas = zip(*resultados)
            if not generos or not ventas: raise Exception(f"No hay datos de generos suficientes para el año {anio}.")

            # Gráfico de barras horizontales
            plt.figure(figsize=(8, 6))
            plt.barh(generos, ventas)
            plt.xlabel('Número de entradas vendidas')
            plt.title(f'10 géneros menos vistos en {anio}')
            plt.tight_layout()

            # Guardar figura
            ruta = f'graficos/{inspect.currentframe().f_code.co_name}_{anio}.png'
            plt.savefig(ruta)
            plt.show()
            print(f'Gráfico guardado en: {ruta}')

        except Exception as e: print(f"# Error con el analisis 'top 10 generos menos vendidos'\nDetalle -> {e}")

obj = ConsultasSql()
obj.analisis_top_10_peliculas_mas_vistas(2024)
#obj.analisis_top_10_generos_menos_vistos(2024)