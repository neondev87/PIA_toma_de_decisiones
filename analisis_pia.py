# =============================================================================
# PIA - Análisis de datos para la toma de decisiones
# UANL - FACPYA | 6to semestre | Grupo 62 | Equipo 10
# Maestra: Hernández Sánchez Victoria Abigail
# Integrantes: Alvarez Perez David Marcos, García Espinosa Ana Lucia,
#              Meléndez Aguilera Daniela, Flores Gutiérrez Erick Alejandro
#
# Cómo se corre:  python analisis_pia.py
# Genera: resultados.txt (todo lo que sale en consola) y las gráficas en capturas/
# =============================================================================

import os

import matplotlib
matplotlib.use("Agg")  # backend que guarda los PNG sin abrir ventanas
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import StrMethodFormatter

# Carpeta del script, para que funcione sin importar desde dónde se ejecute
carpeta = os.path.dirname(os.path.abspath(__file__))
carpeta_capturas = os.path.join(carpeta, "capturas")
os.makedirs(carpeta_capturas, exist_ok=True)

# Archivo donde se guarda todo lo que se imprime
archivo_resultados = open(os.path.join(carpeta, "resultados.txt"), "w", encoding="utf-8")


# Función sencilla: imprime en consola y además lo escribe en resultados.txt
def mostrar(texto=""):
    print(texto)
    archivo_resultados.write(str(texto) + "\n")


# Imprime un título bonito para separar cada paso
def titulo(texto):
    mostrar("")
    mostrar("=" * 70)
    mostrar(texto)
    mostrar("=" * 70)


# Formato de pesos para los ejes de las gráficas (ej. $20,000)
formato_pesos = StrMethodFormatter("${x:,.0f}")

# Colores para las gráficas (uno fijo por sucursal / producto)
colores = ["#2a78d6", "#eb6834", "#1baf7a"]


# =============================================================================
# PASO 1: Importar pandas
# =============================================================================
import pandas as pd

# Para que las tablas se vean completas en consola
pd.set_option("display.width", 120)
pd.set_option("display.max_columns", 20)

titulo("PASO 1: Importar pandas")
mostrar(f"pandas importado correctamente, versión {pd.__version__}")


# =============================================================================
# PASO 2: Cargar DatosPIA.csv en un DataFrame
# =============================================================================
titulo("PASO 2: Cargar el archivo DatosPIA.csv")

# El archivo está separado por comas y en texto normal (UTF-8 / ASCII)
df = pd.read_csv(os.path.join(carpeta, "DatosPIA.csv"), sep=",", encoding="utf-8")
mostrar("Archivo cargado en el DataFrame 'df'")


# =============================================================================
# PASO 3: Exploración de datos
# =============================================================================
titulo("PASO 3: Exploración de datos")

# Primeras 5 filas
mostrar("--- Primeras 5 filas (head) ---")
mostrar(df.head())

# Últimas 5 filas
mostrar("")
mostrar("--- Últimas 5 filas (tail) ---")
mostrar(df.tail())

# Tamaño de la tabla (filas, columnas)
mostrar("")
mostrar("--- Tamaño (shape) ---")
mostrar(f"{df.shape[0]} filas y {df.shape[1]} columnas")

# Tipo de dato de cada columna
mostrar("")
mostrar("--- Tipos de datos (dtypes) ---")
mostrar(df.dtypes)

# Resumen general con info(); info imprime directo, así que lo pasamos a texto
mostrar("")
mostrar("--- Información general (info) ---")
import io
buffer = io.StringIO()
df.info(buf=buffer)
mostrar(buffer.getvalue())

# Valores perdidos por columna
mostrar("--- Valores perdidos por columna (isnull().sum()) ---")
mostrar(df.isnull().sum())
mostrar(f"Total de valores perdidos: {df.isnull().sum().sum()}")

# Filas repetidas
mostrar(f"Filas duplicadas: {df.duplicated().sum()}")

# La fecha viene como texto, la convertimos a fecha real para poder usarla
mostrar("")
mostrar("--- Limpieza: convertir FechaVenta de texto a fecha ---")
mostrar(f"Tipo antes: {df['FechaVenta'].dtype}")
df["FechaVenta"] = pd.to_datetime(df["FechaVenta"], format="%Y-%m-%d")
mostrar(f"Tipo después: {df['FechaVenta'].dtype}")
mostrar(f"Periodo de los datos: del {df['FechaVenta'].min().date()} al {df['FechaVenta'].max().date()}")

# Revisamos que TotalVenta sí sea Cantidad x PrecioUnitario
df["TotalCalculado"] = (df["Cantidad"] * df["PrecioUnitario"]).round(2)
df["Diferencia"] = (df["TotalVenta"] - df["TotalCalculado"]).round(2)
mostrar("")
mostrar("--- Revisión: ¿TotalVenta = Cantidad x PrecioUnitario? ---")
mostrar(f"Filas donde no cuadra exacto: {(df['Diferencia'] != 0).sum()}")
mostrar(f"Diferencia más grande encontrada: ${df['Diferencia'].abs().max():.2f}")
# Quitamos las columnas de apoyo para no ensuciar la tabla
df = df.drop(columns=["TotalCalculado", "Diferencia"])

# Valores únicos de las columnas de texto
mostrar("")
mostrar(f"Sucursales: {sorted(df['Sucursal'].unique())}")
mostrar(f"Productos: {sorted(df['Producto'].unique())}")


# =============================================================================
# PASO 4: Crear Series y DataFrames a partir de los datos
# =============================================================================
titulo("PASO 4: Crear Series y DataFrames")

# Una Serie con solo la columna de ventas
serie_ventas = df["TotalVenta"]
mostrar("--- Serie con TotalVenta (primeros 5 valores) ---")
mostrar(serie_ventas.head())
mostrar(f"Tipo de objeto: {type(serie_ventas).__name__}, largo: {len(serie_ventas)}")

# Una Serie con las ventas usando la fecha como índice
serie_ventas_fecha = pd.Series(df["TotalVenta"].values, index=df["FechaVenta"], name="TotalVenta")
mostrar("")
mostrar("--- Serie de ventas con la fecha como índice (primeros 5) ---")
mostrar(serie_ventas_fecha.head())

# Un DataFrame nuevo solo con 4 columnas
df_resumen = df[["FechaVenta", "Sucursal", "Producto", "TotalVenta"]]
mostrar("")
mostrar("--- DataFrame nuevo con 4 columnas (primeras 5 filas) ---")
mostrar(df_resumen.head())
mostrar(f"Tipo de objeto: {type(df_resumen).__name__}, shape: {df_resumen.shape}")


# =============================================================================
# PASO 5: Filtrar por características (sucursal y producto)
# =============================================================================
titulo("PASO 5: Filtrar por sucursal y por producto")

# Ejemplo 1: solo las ventas de la Sucursal1
ventas_sucursal1 = df[df["Sucursal"] == "Sucursal1"]
mostrar("--- Ejemplo 1: ventas de la Sucursal1 ---")
mostrar(ventas_sucursal1)
mostrar(f"Registros: {len(ventas_sucursal1)} | Total vendido: ${ventas_sucursal1['TotalVenta'].sum():,.2f}")

# Ejemplo 2: solo las ventas del Producto2
ventas_producto2 = df[df["Producto"] == "Producto2"]
mostrar("")
mostrar("--- Ejemplo 2: ventas del Producto2 ---")
mostrar(ventas_producto2)
mostrar(f"Registros: {len(ventas_producto2)} | Total vendido: ${ventas_producto2['TotalVenta'].sum():,.2f}")

# Ejemplo 3: ventas de la Sucursal3 o Sucursal2 usando isin
ventas_suc2_suc3 = df[df["Sucursal"].isin(["Sucursal2", "Sucursal3"])]
mostrar("")
mostrar("--- Ejemplo 3: ventas de Sucursal2 y Sucursal3 (con isin) ---")
mostrar(f"Registros: {len(ventas_suc2_suc3)} | Total vendido: ${ventas_suc2_suc3['TotalVenta'].sum():,.2f}")


# =============================================================================
# PASO 6: Filtrado booleano
# =============================================================================
titulo("PASO 6: Filtrado booleano")

# Ejemplo 1: ventas mayores a 20,000
monto_limite = 20000
ventas_grandes = df[df["TotalVenta"] > monto_limite]
mostrar(f"--- Ejemplo 1: ventas mayores a ${monto_limite:,} ---")
mostrar(ventas_grandes)
mostrar(f"Son {len(ventas_grandes)} de {len(df)} ventas ({len(ventas_grandes) / len(df) * 100:.1f}%) "
        f"y suman ${ventas_grandes['TotalVenta'].sum():,.2f} "
        f"({ventas_grandes['TotalVenta'].sum() / df['TotalVenta'].sum() * 100:.1f}% del total)")

# Ejemplo 2 (con &): Sucursal1 Y ventas de más de 15,000
filtro_y = df[(df["Sucursal"] == "Sucursal1") & (df["TotalVenta"] > 15000)]
mostrar("")
mostrar("--- Ejemplo 2 (&): Sucursal1 Y venta mayor a $15,000 ---")
mostrar(filtro_y)
mostrar(f"Registros: {len(filtro_y)}")

# Ejemplo 3 (con |): ventas de 8 o más piezas O precio unitario mayor a 3,800
filtro_o = df[(df["Cantidad"] >= 8) | (df["PrecioUnitario"] > 3800)]
mostrar("")
mostrar("--- Ejemplo 3 (|): Cantidad de 8 o más O precio unitario mayor a $3,800 ---")
mostrar(filtro_o)
mostrar(f"Registros: {len(filtro_o)}")


# =============================================================================
# PASO 7: Agrupar datos con groupby
# =============================================================================
titulo("PASO 7: Agrupar con groupby")

# Ventas totales por sucursal
ventas_por_sucursal = df.groupby("Sucursal")["TotalVenta"].sum()
mostrar("--- Ventas totales por sucursal ---")
mostrar(ventas_por_sucursal.round(2))
for sucursal, total in ventas_por_sucursal.items():
    mostrar(f"{sucursal}: {total / ventas_por_sucursal.sum() * 100:.1f}% del total")

# Producto más vendido por sucursal (por piezas y por dinero)
piezas_suc_prod = df.groupby(["Sucursal", "Producto"])["Cantidad"].sum()
dinero_suc_prod = df.groupby(["Sucursal", "Producto"])["TotalVenta"].sum()
mostrar("")
mostrar("--- Piezas vendidas por sucursal y producto ---")
mostrar(piezas_suc_prod.unstack())
mostrar("")
mostrar("--- Dinero vendido por sucursal y producto ---")
mostrar(dinero_suc_prod.unstack().round(2))

mostrar("")
mostrar("--- Producto más vendido en cada sucursal ---")
mas_vendido_piezas = piezas_suc_prod.groupby(level="Sucursal").idxmax()
mas_vendido_dinero = dinero_suc_prod.groupby(level="Sucursal").idxmax()
for sucursal in ventas_por_sucursal.index:
    prod_piezas = mas_vendido_piezas[sucursal][1]
    prod_dinero = mas_vendido_dinero[sucursal][1]
    mostrar(f"{sucursal}: por piezas -> {prod_piezas} ({piezas_suc_prod[(sucursal, prod_piezas)]} pzas) | "
            f"por dinero -> {prod_dinero} (${dinero_suc_prod[(sucursal, prod_dinero)]:,.2f})")

# Groupby extra 1: resumen por producto
resumen_producto = df.groupby("Producto").agg(
    ventas_totales=("TotalVenta", "sum"),
    piezas=("Cantidad", "sum"),
    num_ventas=("IDVenta", "count"),
    precio_promedio=("PrecioUnitario", "mean"),
)
mostrar("")
mostrar("--- Extra 1: resumen por producto ---")
mostrar(resumen_producto.round(2))

# Groupby extra 2: ventas por semana del mes (los datos son solo de junio 2023,
# así que agrupar por mes daría un solo grupo; por eso agrupamos por semana)
df["Semana"] = (df["FechaVenta"].dt.day - 1) // 7 + 1
ventas_por_semana = df.groupby("Semana")["TotalVenta"].agg(["sum", "count"])
ventas_por_semana.columns = ["ventas_totales", "num_ventas"]
mostrar("")
mostrar("--- Extra 2: ventas por semana de junio (semana 1 = días 1-7, ... semana 5 = días 29-30) ---")
mostrar(ventas_por_semana.round(2))

# Groupby extra 3: ventas por día de la semana
dias_es = {"Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles", "Thursday": "Jueves",
           "Friday": "Viernes", "Saturday": "Sábado", "Sunday": "Domingo"}
df["DiaSemana"] = df["FechaVenta"].dt.day_name().map(dias_es)
orden_dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
ventas_por_dia = df.groupby("DiaSemana")["TotalVenta"].agg(["sum", "count", "mean"]).reindex(orden_dias)
ventas_por_dia.columns = ["ventas_totales", "num_ventas", "venta_promedio"]
mostrar("")
mostrar("--- Extra 3: ventas por día de la semana ---")
mostrar(ventas_por_dia.round(2))


# =============================================================================
# PASO 8: Estadísticas descriptivas de las ventas
# =============================================================================
titulo("PASO 8: Estadísticas descriptivas de TotalVenta")

media = df["TotalVenta"].mean()
mediana = df["TotalVenta"].median()
moda = df["TotalVenta"].mode()
minimo = df["TotalVenta"].min()
maximo = df["TotalVenta"].max()
rango = maximo - minimo
desviacion = df["TotalVenta"].std()

mostrar(f"Media:               ${media:,.2f}")
mostrar(f"Mediana:             ${mediana:,.2f}")
if len(moda) == len(df):
    mostrar("Moda:                no hay, ningún monto se repite (cada venta es distinta)")
else:
    mostrar(f"Moda:                {list(moda)}")
mostrar(f"Mínimo:              ${minimo:,.2f}")
mostrar(f"Máximo:              ${maximo:,.2f}")
mostrar(f"Rango:               ${rango:,.2f}")
mostrar(f"Desviación estándar: ${desviacion:,.2f}")
mostrar(f"Coef. de variación:  {desviacion / media * 100:.1f}%")

# Moda de la cantidad de piezas (aquí sí se repiten valores)
mostrar(f"Moda de Cantidad (piezas más común por venta): {list(df['Cantidad'].mode())}")

# describe() de las columnas numéricas
mostrar("")
mostrar("--- describe() de las columnas numéricas ---")
mostrar(df[["Cantidad", "PrecioUnitario", "TotalVenta"]].describe().round(2))

# Correlación: qué influye más en el total, la cantidad o el precio
corr_cantidad = df["Cantidad"].corr(df["TotalVenta"])
corr_precio = df["PrecioUnitario"].corr(df["TotalVenta"])
mostrar("")
mostrar("--- Correlación con TotalVenta ---")
mostrar(f"Cantidad vs TotalVenta:       {corr_cantidad:.2f}")
mostrar(f"PrecioUnitario vs TotalVenta: {corr_precio:.2f}")


# =============================================================================
# PASO 9: Gráficos con pandas (.plot) guardados en capturas/
# =============================================================================
titulo("PASO 9: Gráficas")

# Gráfica 1: ventas totales por sucursal (barras)
ax = ventas_por_sucursal.plot(kind="bar", color=colores, figsize=(8, 5), rot=0)
ax.set_title("Ventas totales por sucursal (junio 2023)", fontsize=14)
ax.set_xlabel("Sucursal")
ax.set_ylabel("Ventas totales ($)")
ax.yaxis.set_major_formatter(formato_pesos)
ax.grid(axis="y", alpha=0.3)
for i, valor in enumerate(ventas_por_sucursal):
    ax.text(i, valor, f"${valor:,.0f}", ha="center", va="bottom", fontsize=11)
plt.tight_layout()
plt.savefig(os.path.join(carpeta_capturas, "captura_01_ventas_por_sucursal.png"), dpi=150)
plt.close()
mostrar("Guardada: capturas/captura_01_ventas_por_sucursal.png")

# Gráfica 2: ventas a lo largo del tiempo (línea por día)
ventas_por_fecha = df.groupby("FechaVenta")["TotalVenta"].sum()
ax = ventas_por_fecha.plot(kind="line", marker="o", color=colores[0], figsize=(11, 5), linewidth=2,
                           label="Ventas del día", x_compat=True)
ax.axhline(ventas_por_fecha.mean(), color="gray", linestyle="--", linewidth=1,
           label=f"Promedio diario: ${ventas_por_fecha.mean():,.0f}")
ax.set_title("Ventas diarias a lo largo de junio 2023", fontsize=14)
ax.set_xlabel("Fecha (día/mes)")
ax.set_ylabel("Ventas del día ($)")
ax.yaxis.set_major_formatter(formato_pesos)
ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
ax.grid(alpha=0.3)
ax.legend()
plt.tight_layout()
plt.savefig(os.path.join(carpeta_capturas, "captura_02_ventas_en_el_tiempo.png"), dpi=150)
plt.close()
mostrar("Guardada: capturas/captura_02_ventas_en_el_tiempo.png")

# Gráfica 3: participación de cada producto en las ventas (pastel)
ventas_por_producto = resumen_producto["ventas_totales"]
ax = ventas_por_producto.plot(kind="pie", colors=colores, autopct="%1.1f%%", figsize=(7, 7),
                              startangle=90, textprops={"fontsize": 12},
                              wedgeprops={"edgecolor": "white", "linewidth": 2})
ax.set_title("Participación de cada producto en las ventas totales", fontsize=14)
ax.set_ylabel("")
plt.tight_layout()
plt.savefig(os.path.join(carpeta_capturas, "captura_03_participacion_por_producto.png"), dpi=150)
plt.close()
mostrar("Guardada: capturas/captura_03_participacion_por_producto.png")

# Gráfica 4: ventas por sucursal y producto (barras agrupadas)
tabla_suc_prod = dinero_suc_prod.unstack()
ax = tabla_suc_prod.plot(kind="bar", color=colores, figsize=(9, 5), rot=0, edgecolor="white")
ax.set_title("Ventas por sucursal y producto", fontsize=14)
ax.set_xlabel("Sucursal")
ax.set_ylabel("Ventas totales ($)")
ax.yaxis.set_major_formatter(formato_pesos)
ax.grid(axis="y", alpha=0.3)
ax.legend(title="Producto")
plt.tight_layout()
plt.savefig(os.path.join(carpeta_capturas, "captura_04_ventas_sucursal_producto.png"), dpi=150)
plt.close()
mostrar("Guardada: capturas/captura_04_ventas_sucursal_producto.png")

# Gráfica 5: ventas por semana (barras)
ax = ventas_por_semana["ventas_totales"].plot(kind="bar", color=colores[0], figsize=(8, 5), rot=0)
ax.set_title("Ventas por semana de junio 2023", fontsize=14)
ax.set_xlabel("Semana del mes (la 5 solo tiene los días 29 y 30)")
ax.set_ylabel("Ventas totales ($)")
ax.yaxis.set_major_formatter(formato_pesos)
ax.grid(axis="y", alpha=0.3)
for i, valor in enumerate(ventas_por_semana["ventas_totales"]):
    ax.text(i, valor, f"${valor:,.0f}", ha="center", va="bottom", fontsize=10)
plt.tight_layout()
plt.savefig(os.path.join(carpeta_capturas, "captura_05_ventas_por_semana.png"), dpi=150)
plt.close()
mostrar("Guardada: capturas/captura_05_ventas_por_semana.png")

# Gráfica 6: cómo se reparten los montos de las ventas (histograma)
ax = df["TotalVenta"].plot(kind="hist", bins=8, color=colores[2], edgecolor="white", figsize=(8, 5),
                             label="Número de ventas")
ax.axvline(media, color="black", linestyle="--", linewidth=1, label=f"Media: ${media:,.0f}")
ax.axvline(mediana, color="gray", linestyle=":", linewidth=1.5, label=f"Mediana: ${mediana:,.0f}")
ax.set_title("Distribución de los montos de venta", fontsize=14)
ax.set_xlabel("Monto de la venta ($)")
ax.xaxis.set_major_formatter(formato_pesos)
ax.set_ylabel("Número de ventas")
ax.legend()
plt.tight_layout()
plt.savefig(os.path.join(carpeta_capturas, "captura_06_distribucion_montos.png"), dpi=150)
plt.close()
mostrar("Guardada: capturas/captura_06_distribucion_montos.png")


# =============================================================================
# PASO 10: Hallazgos y conclusiones (datos clave para redactarlas)
# =============================================================================
titulo("PASO 10: Hallazgos y conclusiones (datos clave)")

total_general = df["TotalVenta"].sum()
mejor_sucursal = ventas_por_sucursal.idxmax()
peor_sucursal = ventas_por_sucursal.idxmin()
mejor_producto = ventas_por_producto.idxmax()
peor_producto = ventas_por_producto.idxmin()
mejor_dia = ventas_por_fecha.idxmax()
peor_dia = ventas_por_fecha.idxmin()
venta_max = df.loc[df["TotalVenta"].idxmax()]
venta_min = df.loc[df["TotalVenta"].idxmin()]

mostrar(f"1. Total vendido en junio 2023: ${total_general:,.2f} en {len(df)} ventas")
mostrar(f"2. Sucursal que más vendió: {mejor_sucursal} (${ventas_por_sucursal.max():,.2f}); "
        f"la que menos: {peor_sucursal} (${ventas_por_sucursal.min():,.2f}). "
        f"Diferencia: ${ventas_por_sucursal.max() - ventas_por_sucursal.min():,.2f}")
mostrar(f"3. Producto con más ventas: {mejor_producto} (${ventas_por_producto.max():,.2f}); "
        f"el de menos: {peor_producto} (${ventas_por_producto.min():,.2f})")
mostrar(f"4. Mejor día: {mejor_dia.date()} (${ventas_por_fecha.max():,.2f}); "
        f"peor día: {peor_dia.date()} (${ventas_por_fecha.min():,.2f})")
mostrar(f"5. Venta más grande: ID {venta_max['IDVenta']} ({venta_max['Sucursal']}, {venta_max['Producto']}, "
        f"{venta_max['Cantidad']} pzas) por ${venta_max['TotalVenta']:,.2f}")
mostrar(f"   Venta más chica: ID {venta_min['IDVenta']} ({venta_min['Sucursal']}, {venta_min['Producto']}, "
        f"{venta_min['Cantidad']} pza) por ${venta_min['TotalVenta']:,.2f}")
mostrar(f"6. La cantidad de piezas explica mucho más el total (correlación {corr_cantidad:.2f}) "
        f"que el precio unitario ({corr_precio:.2f})")
mostrar(f"7. Ventas mayores a ${monto_limite:,}: {len(ventas_grandes)} ventas que juntas son el "
        f"{ventas_grandes['TotalVenta'].sum() / total_general * 100:.1f}% del dinero")
mostrar("")
mostrar("La redacción completa de los hallazgos está en hallazgos.md")

archivo_resultados.close()
print("\nListo. Resultados guardados en resultados.txt y gráficas en capturas/")
