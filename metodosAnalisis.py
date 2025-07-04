import os
import inspect

from db_modulos.obj_sql import SqlObj
from collections import defaultdict

import matplotlib.pyplot as plt
import matplotlib.cm as cm

MESES = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']

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

            # Gráfico de barras verticales
            fig, ax = plt.subplots()
            ax.bar(titulos, ventas)
            ax.set_title(f"Top 10 Películas por Ventas en {anio}")
            ax.set_ylabel("Número de boletos vendidos")

            # solución
            ax.set_xticks(range(len(titulos)))

            ax.set_xticklabels(titulos, rotation=45, ha="right")
            plt.tight_layout()

            # Guardar y mostrar...

            # Asegurar que la carpeta "graficos" exista
            os.makedirs(f"graficos/{inspect.currentframe().f_code.co_name}", exist_ok=True)

            # Guardamos el gráfico
            ruta = f"graficos/{inspect.currentframe().f_code.co_name}/{anio}.png"
            plt.savefig(ruta)

            #plt.show()
            print(f"Gráfico guardado en {ruta}")

        except Exception as e: print(f"# Error con el analisis 'top 10 peliculas mas vendidas'\nDetalle -> {e}")

    def analisis_top_10_generos_menos_vistos(self, anio):
        try:
            # Consulta: 10 generos por menor número de ventas en el año dado
            consulta = f'''
            WITH ranking_generos AS (
                SELECT
                    hb.genero,
                    COUNT(*) AS ventas,
                    RANK() OVER (ORDER BY COUNT(*) ASC) AS r
                FROM hechos_boletos hb
                WHERE EXTRACT(YEAR FROM hb.hora_compra) = {anio}
                GROUP BY hb.genero
            )
            SELECT genero, ventas
            FROM ranking_generos
            WHERE r <= 10;
            '''
            # Corregido para no usar LIMIT, como pidió el profe
            # Usa RANK OVER COUNT y tabla anidada

            self.obj.cur.execute(consulta)
            resultados = self.obj.cur.fetchall()
            if not resultados: raise Exception(f"No hay datos de generos para el año {anio}.")

            # Preparar datos
            generos, ventas = zip(*resultados)
            if not generos or not ventas: raise Exception(f"No hay datos de generos suficientes para el año {anio}.")

            generos, ventas = zip(*sorted(zip(generos, ventas), key=lambda x: x[1]))
            generos = generos[::-1]
            ventas = ventas[::-1]
            # Gráfico de barras horizontales
            plt.figure(figsize=(8, 6))
            plt.barh(generos, ventas)
            plt.xlabel('Número de entradas vendidas')
            plt.title(f'10 géneros menos vistos en {anio}')
            plt.tight_layout()

            # Guardar figura...

            # Asegurar que la carpeta "graficos" exista
            os.makedirs(f"graficos/{inspect.currentframe().f_code.co_name}", exist_ok=True)

            # Guardamos
            ruta = f'graficos/{inspect.currentframe().f_code.co_name}/{anio}.png'
            plt.savefig(ruta)

            #plt.show()
            print(f'Gráfico guardado en: {ruta}')

        except Exception as e: print(f"# Error con el analisis 'top 10 generos menos vendidos'\nDetalle -> {e}")

    def analisis_ventas_anuales(self, anio):
        try:
            # Consulta: Ventas anuales por mes
            consulta = f'''
            SELECT EXTRACT(MONTH FROM hora_compra) AS mes, SUM(precio)
            FROM hechos_boletos
            WHERE EXTRACT(YEAR FROM hora_compra) = {anio}
            GROUP BY mes
            ORDER BY mes;
            '''

            self.obj.cur.execute(consulta)
            resultados = self.obj.cur.fetchall()
            if not resultados: raise Exception(f"No hay datos de venta para el año {anio}.")

            # Preparar datos
            meses, ventas = zip(*resultados)
            if not meses or not ventas: raise Exception(f"No hay datos de venta suficientes para el año {anio}.")

            etiquetas_meses = [MESES[int(m)-1] for m in meses]

            # Grafico de linea
            plt.figure(figsize=(10, 5))
            plt.plot(meses, ventas, marker='o')
            plt.title(f"Ventas mensuales en el año {anio}")
            plt.xlabel("Mes")
            plt.ylabel("Recaudación total en ventas (CLP)")
            plt.xticks(meses, etiquetas_meses)
            plt.grid(True)

            # Guardar y mostrar...

            # Asegurar que la carpeta "graficos" exista
            os.makedirs(f"graficos/{inspect.currentframe().f_code.co_name}", exist_ok=True)

            # Guardamos
            ruta = f'graficos/{inspect.currentframe().f_code.co_name}/{anio}.png'
            plt.savefig(ruta)

            #plt.show()
            print(f"Gráfico guardado en: {ruta}")

        except Exception as e: print(f"# Error con el analisis 'ventas anuales'\nDetalle -> {e}")

    def analisis_ventas_anuales_por_genero(self, anio):
        try:
            # Consulta: Ventas anuales por mes y genero
            consulta = f'''
            SELECT
            EXTRACT(MONTH FROM hb.hora_inicio_funcion)::int AS mes,
            hb.genero,
            COUNT(*) AS total_ventas
            FROM hechos_boletos hb
            JOIN pelicula p ON hb.id_pelicula = p.id
            WHERE EXTRACT(YEAR FROM hb.hora_inicio_funcion) = {anio}
            GROUP BY mes, hb.genero
            ORDER BY mes;
            '''

            self.obj.cur.execute(consulta)
            resultados = self.obj.cur.fetchall()
            if not resultados: raise Exception(f"No hay datos de venta para el año {anio}.")

            # Preparar datos
            datos = defaultdict(lambda: [0]*len(MESES))
            for mes, genero, total in resultados: datos[genero][mes - 1] = total
            n_generos = len(datos)
            colores = cm.get_cmap('tab20', n_generos)  # paleta con hasta 20 colores

            plt.figure(figsize=(10, 5))

            for i, (genero, ventas) in enumerate(datos.items()):
                plt.plot(
                    MESES, ventas,
                    label=genero,
                    color=colores(i),
                    linewidth=2,
                    marker='o',
                    markersize=6
                )

            # Grafico de linea
            plt.title(f'Ventas mensuales por género - {anio}', fontsize=16)
            plt.xlabel('Mes', fontsize=12)
            plt.ylabel('Entradas vendidas', fontsize=12)
            plt.grid(True, linestyle='--', alpha=0.5)
            plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
            plt.tight_layout(rect=[0, 0, 1, 1])

            # Guardar y mostrar...

            # Asegurar que la carpeta "graficos" exista
            os.makedirs(f"graficos/{inspect.currentframe().f_code.co_name}", exist_ok=True)

            # Guardamos
            ruta = f'graficos/{inspect.currentframe().f_code.co_name}/{anio}.png'
            plt.savefig(ruta)

            #plt.show()
            print(f"Gráfico guardado en: {ruta}")

        except Exception as e: print(f"# Error con el analisis 'ventas anuales por genero'\nDetalle -> {e}")

    
    def analisis_edad_por_genero_pelicula(self, anio):
        try:
            # Consulta: Obtener los géneros más vistos y las edades de sus clientes
            consulta = f'''
            WITH generos_populares AS (
                SELECT hb.genero, COUNT(*) as total_ventas
                FROM hechos_boletos hb
                WHERE EXTRACT(YEAR FROM hb.hora_inicio_funcion) = {anio}
                GROUP BY hb.genero
                ORDER BY total_ventas DESC
                LIMIT 10
            )
            SELECT
                hb.genero,
                c.edad
            FROM hechos_boletos hb
            JOIN cliente c ON hb.id_cliente = c.id
            JOIN generos_populares gp ON hb.genero = gp.genero
            WHERE EXTRACT(YEAR FROM hb.hora_inicio_funcion) = {anio}
            AND c.edad IS NOT NULL
            ORDER BY hb.genero;
            '''
            
            self.obj.cur.execute(consulta)
            resultados = self.obj.cur.fetchall()
            if not resultados: raise Exception(f"No hay datos de edades para el año {anio}.")

            # Preparar datos
            datos_por_genero = defaultdict(list)
            for genero, edad in resultados:
                if edad is not None:  # Filtrar edades nulas
                    datos_por_genero[genero].append(edad)

            # Filtrar géneros con al menos 5 muestras para un boxplot válido
            datos_filtrados = {genero: edades for genero, edades in datos_por_genero.items() 
                             if len(edades) >= 5}
            
            if not datos_filtrados: 
                raise Exception(f"No hay suficientes datos de edades por género para el año {anio}.")

            generos = list(datos_filtrados.keys())
            edades = list(datos_filtrados.values())

            # Gráfico de caja horizontal
            fig, ax = plt.subplots(figsize=(12, 8))
            
            # Crear el boxplot
            box_plot = ax.boxplot(edades, vert=False, patch_artist=True, showmeans=True,
                                boxprops=dict(facecolor='lightblue', color='black', alpha=0.7),
                                meanprops=dict(marker='D', markerfacecolor='red', markersize=6),
                                medianprops=dict(color='orange', linewidth=2),
                                whiskerprops=dict(color='black'),
                                capprops=dict(color='black'))
            
            # Configurar ejes y etiquetas
            edad_min = min(min(edades_genero) for edades_genero in edades)
            edad_max = max(max(edades_genero) for edades_genero in edades)
            ax.set_xlim(0,80)
            ax.set_yticks(range(1, len(generos) + 1))
            ax.set_yticklabels(generos, fontsize=10)
            ax.set_xlabel("Edad", fontsize=12)
            ax.set_ylabel("Género de Película", fontsize=12)
            ax.set_title(f"Distribución de Edades por Género más visto en {anio}", fontsize=14)
            
            # Agregar grid para mejor lectura
            ax.grid(True, alpha=0.3, axis='x')
            
            plt.tight_layout()

            # Guardar y mostrar...
            os.makedirs(f"graficos/{inspect.currentframe().f_code.co_name}", exist_ok=True)

            # Guardamos
            ruta = f'graficos/{inspect.currentframe().f_code.co_name}/{anio}.png'
            plt.savefig(ruta, dpi=300, bbox_inches='tight')

            print(f"Gráfico guardado en: {ruta}")
            print(f"Géneros analizados: {', '.join(generos)}")

        except Exception as e: print(f"# Error con el analisis 'edad por genero'\nDetalle -> {e}")



    def analisis_pelicula_con_mayor_recaudacion_por_mes(self, anio):
        try:
            # consulta anidada para sacar las q más recaudación tuvieron x mes
            consulta = f'''
                    WITH recaudacion_mensual AS (
                        SELECT
                            DATE_TRUNC('month', bol.hora_compra) AS mes,
                            p.id AS id_pelicula,
                            p.titulo,
                            SUM(bol.precio) AS total_recaudado
                        FROM hechos_boletos bol
                        JOIN pelicula p ON bol.id_pelicula = p.id
                        WHERE EXTRACT(YEAR FROM bol.hora_compra) = {anio}
                        GROUP BY mes, p.id, p.titulo
                    ),
                    maximos_por_mes AS (
                        SELECT
                            mes,
                            MAX(total_recaudado) AS max_recaudo
                        FROM recaudacion_mensual
                        GROUP BY mes
                    )
                    SELECT
                        r.mes,
                        r.titulo,
                        r.total_recaudado
                    FROM recaudacion_mensual r
                    JOIN maximos_por_mes m
                        ON r.mes = m.mes AND r.total_recaudado = m.max_recaudo
                    ORDER BY r.mes;
                '''

            self.obj.cur.execute(consulta)
            resultados = self.obj.cur.fetchall()
            if not resultados: raise Exception(f"No se obtuvieron datos de recaudación para el año {anio}.")

            #eje X (meses)
            meses = [MESES[row[0].month - 1] for row in resultados]
            peliculas = [row[1] for row in resultados]

            #eje Y
            recaudaciones = [row[2] for row in resultados]

            plt.figure(figsize=(10, 6))
            bars = plt.bar(meses, recaudaciones, color='indianred')

            #d las barras obtenidas ponerles las etiquetas
            for i, bar in enumerate(bars):
                altura = bar.get_height()
                plt.text(bar.get_x() + bar.get_width() / 2,
                    altura * 0.5,
                    peliculas[i],
                    ha='center',
                    va='center',
                    fontsize=10,
                    color='white',
                    rotation=90)

            plt.title(f'Películas con más recaudación por mes del año {anio}')
            plt.xlabel('Mes')
            plt.ylabel('Recaudación en pesos chilenos (CLP)')
            plt.xticks(rotation=45)
            plt.ylim(0, max(recaudaciones) * 1.2)
            plt.grid(axis='y', linestyle='--')
            os.makedirs(f"graficos/{inspect.currentframe().f_code.co_name}", exist_ok=True)

            # Guardamos
            ruta = f'graficos/{inspect.currentframe().f_code.co_name}/{anio}.png'
            plt.savefig(ruta)
            print(f"Gráfico guardado en: {ruta}")

        except Exception as e: print(f"# Error con analisis_pelicula_con_mayor_recaudacion_por_mes \nDetalle -> {e}")

    def analisis_ventas_clasificacion_etaria(self, anio):
        try:
            self.obj.cur.execute(f"""
            SELECT clasificacion_etaria, COUNT(*)
            FROM hechos_boletos
            WHERE EXTRACT(YEAR FROM hora_compra) = {anio}
            GROUP BY clasificacion_etaria
            ORDER BY COUNT(*) DESC;
            """)
            resultados = self.obj.cur.fetchall()
            if not resultados:
                print("No hay ventas para mostrar.")
                return

            etiquetas, cantidades = zip(*resultados)

            plt.figure(figsize=(7, 7))
            plt.pie(cantidades, labels=etiquetas, autopct='%1.1f%%', startangle=90)
            plt.title(f"Distribución de ventas por clasificación etaria en el año {anio}")
            plt.axis('equal')

            os.makedirs(f"graficos/{inspect.currentframe().f_code.co_name}", exist_ok=True)
            ruta = f"graficos/{inspect.currentframe().f_code.co_name}/{anio}.png"
            plt.savefig(ruta)
            print(f"Gráfico guardado en: {ruta}")
        except Exception as e:
            print(f"Error con analisis_ventas_clasificacion_etaria \n{e}")

    def cerrar(self):
        self.obj.cerrar_conexion()


#obj = ConsultasSql()
#obj.analisis_top_10_peliculas_mas_vistas(2024)
#obj.analisis_top_10_generos_menos_vistos(2024)
#obj.analisis_ventas_anuales(2024)
#obj.analisis_ventas_anuales_por_genero(2024)
#obj.analisis_edad_por_genero_pelicula(2024)
