# ============================================================================= #1 Jhony
# Importamos las librerías necesarias
# =============================================================================
import pandas as pd
from matplotlib import pyplot as plt
# =============================================================================
# Validación de código de observatorio
# =============================================================================
codigo_observatorio= input("Ingresar el código del observatorio: ")
codigo_observatorio = codigo_observatorio.upper()
name = "homog_mo_" + str(codigo_observatorio) + ".txt"
# =============================================================================
# Creación de Serie con base a diccionario de las regiones climáticas
# =============================================================================
climreg = {
    "Code":["ALT","ANT","RAG","BAS","BER","CHM","CHD","GSB","DAV","ELM","ENG","GVE","GRH","GRC","JUN","CDF","OTL","LUG","LUZ","MER","NEU","PAY","SBE","SAM","SAR","SIA","SIO","STG","SAE","SMA"],
    "Region":["Central Alpine North Slope","Central Alpine North Slope","Northern & Central Grisons","Eastern Jura","Central Plaetau","Western Jura","Western Alpine North Slope","Alpine South Side","Northern & Central Grisons","Eastern Alpine North Slope","Central Alpine North Slope","Western Plateau","Western Alpine North Slope","Valais","Western Alpine North Slope","Western Jura","Alpine South Side","Alpine South Side","Central Plateau","Western Alpine North Slope","Western PLateau","Western Plateau","Alpine South Side","Engainde","Northern & Central Grisons","Engadine","Valais","North-Eastern Plateau","Estern Alpine North Slope","North-Eastern Plateau"]
    }
climreg = pd.DataFrame(climreg)
climreg.set_index("Code",inplace=True)
# =============================================================================
# Lectura de archivos y registro de datos. En la primera excepción, se intentará
# leer el archivo a partir de la fila 23 (conveniente para JUN, RAG, SAR), en el 
# caso de levantarse un ParserError, se procederá a leer a partir de la fila 26, lo
# que es conveniente para el resto de archivos.
# ============================================================================= #2 Daniel
try:
    df = pd.read_csv(name, delim_whitespace=True, skiprows=23)  
except:
    df = pd.read_csv(name, delim_whitespace=True, skiprows=26)
# =============================================================================
# Para el título de la gráfica. Para extraer datos del nombre del observatorio y
# altura, se hizo una serie de pandas con los parámetros: skiprows que empieza a
# leer desde la fila 5, nrows que permite leer sólo 3 filas, engine que nos ayuda
# a designar el motor Python por su potencia de funcionalidad, index_col que nos 
# permite indexar con base a la primera columna, squeeze convierte la unica serie
# en arreglo
# =============================================================================
info = pd.read_csv(name,sep=":",skiprows=5,nrows=3,header=None,engine="python",index_col=0,skipinitialspace=True,squeeze=True)
# =============================================================================
# Crea una columna de día 1 para todas las filas, crea un nuevo DataFrame con los
# datos de las fechas, se concatenan como fecha y se agrega una columna de fechas
# en el DataFrame original
# ============================================================================= #1 Jhony
df['Day'] = pd.Series([1 for x in range(len(df.index))]) 
df2, df2.columns = df[["Year", "Month", "Day"]].copy(),["year", "month", "day"] 
df["Date"] = pd.to_datetime(df2) 
# =============================================================================
# En caso de ser posible, calcula la media de la temperatura, calcula la media de 
# de las precipitaciones, o bien ambas, exceptuando el KeyError si se necesita
# =============================================================================
try:
    µT = df["Temperature"].mean()
except:
    KeyError    
try:
    µP = df["Precipitation"].mean()
except:
    KeyError    
# =============================================================================
# Graficación de los datos, en caso de haber ambas variables de precipitación y
# temperatura, gráfica ambos datos con base a las especificaciones requeridas,
# caso contrario, trabajará con uno solo de los datos que existiera
# ============================================================================= #4 Jocelyn
if "Temperature" in df.columns and "Precipitation" in df.columns:
    fig, ax1 = plt.subplots()
    ax1.set_xlabel('Fecha')
    ax1.set_ylabel('Temperature (°C)')
    graf1, = ax1.plot(df["Date"],df["Temperature"],color="royalblue",label="Temperatura",linewidth=0.75)
    mean1, = ax1.plot(df["Date"],[µT]*len(df.index),ls="--",label="Temperatura Media",color="b",linewidth=1.5)
    ax1.tick_params(axis='y')
    ax2 = ax1.twinx() #Nos permite mantener el mismo eje en x, pero para un segundo eje en y
    ax2.set_ylabel('Precipitación (mm)')
    graf2, = ax2.plot(df["Date"],df["Precipitation"],color="lightcoral",label="Precipitación",linewidth=0.75)
    mean2, = ax2.plot(df["Date"],[µP]*len(df.index),ls="--",label="Precipitación Media",color="r",linewidth=1.5)
    ax2.tick_params(axis='y')
    plt.legend(handles=[graf1,graf2,mean1,mean2],loc="upper left")
elif "Temperature" in df.columns and "Precipitation" not in df.columns:
    plt.plot(df["Date"],df["Temperature"],color="royalblue",label="Temperatura",linewidth=1)
    plt.plot(df["Date"],[µT]*len(df.index),ls="--",label="Temperatura Media",color="b",linewidth=2)
    plt.legend()
    plt.ylabel("Temperatura (°C)")
    plt.xlabel("Fecha")
elif "Temperature" not in df.columns and "Precipitation" in df.columns:
    plt.plot(df["Date"],df["Precipitation"],color="lightcoral",label="Precipitación",linewidth=1)
    plt.plot(df["Date"],[µP]*len(df.index),ls="--",label="Precipitación Media",color="r",linewidth=2)
    plt.legend()
    plt.ylabel("Precipitación (mm)")
    plt.xlabel("Fecha")                 
# =============================================================================
# Para el orden de componentes del título, en negrita y grande
# =============================================================================
plt.suptitle(info[0] + " | " + codigo_observatorio + " | " + info[1] + " | " + climreg._get_value(codigo_observatorio,'Region'),fontsize=15,fontweight="bold")