# Importar
import pandas as pd
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype
import numpy as np
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import json 
import camelot
import re

def crear_query(df:pd.DataFrame) -> str:
  # Imprimir aviso
  print("Se está generando la query de actualización. Por favor, aguarde...")
  # Definir mi lista de RFCs únicos
  lista_rfcs:list = list(df["rfc"].to_list())
  # Definir mi lista de columnas (sin index ni rfc)
  lista_columnas:list = list(df.columns)[2:]
  # Definir mi tupla de valores ordenados
  lista_valores:list = []
  for columna in lista_columnas:
    lista_valores.extend(df[columna].tolist())
  tupla_valores:tuple = tuple(lista_valores)
  # Inicializar el string inicial de la consulta
  consulta:str = "UPDATE org SET"
  # Empezar bucle
  for columna in lista_columnas:
    consulta+= f" {columna} = (CASE rfc "
    for rfc in lista_rfcs:
        try:
          valor = df.loc[df["rfc"]==rfc][columna].values[0]
          consulta+=f"WHEN '{rfc}' THEN %s "
        except Exception as e:
           print(f"Filtrando por el rfc {rfc}, en la columna {columna}, cuyo valor es {valor}, se obtiene el error {e}")
    if columna == lista_columnas[-1]:
       consulta+= f"END) WHERE rfc in {tuple(lista_rfcs)}"
    else:
      consulta+= f"END),"
  #Return
  return consulta, tupla_valores

def set_categorias_entidades(df, año):
  """
  Función que fillea las columnas Categoría y Ent.Federativa en el Reporte de Donatarias Autorizadas
  """
  # Categorías
  df.loc[(df[df.columns[0]] == df[df.columns[1]]), "CATEGORIA"] = df.loc[(df[df.columns[0]] == df[df.columns[1]]), df.columns[0]]
  df["CATEGORIA"] = df["CATEGORIA"].ffill()
  # Entidades federativas
  if int(año) in list(range(2014,2019)):
    # Agrego Aguascalientes si no esta en los primeros registros
    if pd.isna(df['ENTIDAD FEDERATIVA'].iloc[0]):
      df['ENTIDAD FEDERATIVA'].iloc[0] = "Aguascalientes"
    df.loc[df["RFC"] == df[df.columns[-4]],"ENTIDAD FEDERATIVA"] = df.loc[df["RFC"] == df[df.columns[-4]],"RFC"]
    df["ENTIDAD FEDERATIVA"] = df["ENTIDAD FEDERATIVA"].ffill()
  else:
    #df[df.columns[0]] = df[df.columns[0]].str.upper()
    # Eliminar columna extra si existe
    df.drop("Unnamed: 0", inplace = True, axis=1) if "Unnamed: 0" in df.columns else None
    # Filtro para encontrar Total + Entidad 
    df.loc[df[df.columns[0]].astype(str).str.startswith("TOTAL "), "ENTIDAD FEDERATIVA"] = df.loc[df[df.columns[0]].astype(str).str.startswith("TOTAL "), df.columns[0]]
    # Quitar palabra TOTAL
    df.loc[:,"ENTIDAD FEDERATIVA"] = df.loc[:,"ENTIDAD FEDERATIVA"].str.replace("TOTAL ", "")
    # Rellenar
    df["ENTIDAD FEDERATIVA"] = df["ENTIDAD FEDERATIVA"].bfill()

def get_headers_from_dataframe(df: pd.DataFrame, denominacion):
  """
  Función que asigna headers al crudo de camelot en el RDA
  """
  for index, row in df.iterrows():
    if (row[0] == "RFC") and (row[1] == denominacion):
        alto_header = 1
        while(df.iloc[index+alto_header, 0] == "RFC"):
            alto_header += 1
        for column in range(2, len(row.tolist())):
            for i in range(1, alto_header):
                row[column] = f"{row[column]} - {df.iloc[index+i, column]}"

        return [a.replace("\n", "").strip() for a in row.tolist() if type(a) is str]
    else:
        continue

def add_zero_fields(dfs, MAP_CAMPOS):
  """
  Función que rellena con 0 los valores del DataFrame
  """
  add = []
  for value in MAP_CAMPOS.values():
    flag_in_df = False
    for df in dfs.values():
      if value in df.columns.tolist():
        flag_in_df = True
    if flag_in_df == False:
      add.append(value)  
  if len(add):
    dfs[list(dfs.keys())[0]][add] = 0

def get_new_headers(headers_df: list, headers_estimados: dict): 
  """
  Función que chequea la coincidencia de los headers reales con los esperados con FuzzyWuzzy
  """
  new_headers = dict()
  for header_df in headers_df:
      for h_estimado, value in headers_estimados.items():
          coincidencia = fuzz.partial_ratio(header_df.lower(), h_estimado.lower())
          if  coincidencia > 95:
              new_headers[header_df] = value
  if len(new_headers.keys()) < len(headers_df):
      print("Falló un header. Por favor revisar el/los siguiente/s registro/s: ")
      for header in headers_df:
          if header not in new_headers.keys():
              print(header)
  return new_headers

def clear_merged_values(x):
  """
  Función que limpia los valores mergeados
  """
  if ~(pd.isna(x)) and str(x).find("   ") != -1:
    return float(str(x).strip().rsplit(" ")[-1])
  else:
    try:
      return float(x)
    except:
      print(f"""Se encontró el valor [{x}] en una celda de datos, por favor
                revisar y corregir en caso de corresponder. Se asignará el 
                valor 0 para efectuar la carga correspondiente.""")
      return 0
    
def is_empty(lista : list) -> bool:
  """
  Predicado que devuelve True si la lista ingresada contiene todos guiones medios.
  """
  for element in lista:
    if element != "-":
      return False
    else:
      continue
  return True

def distribuir_celda_bug(row, n_cols):
  """
  Función que distribuye las celdas bug en un orden específico en el RDA
  """
  # Obtener los valores de una celda y spitear por newline
  values = str(row.iloc[1]).split("\n")
  # Borrar los que son espacios (los de interés deben contener letras o ser '-') 
  new_values = [value for value in values if not value.isspace()]
  # Si está completo
  if len(new_values) == n_cols-1:
    if re.findall(r'[A-Z]{3}\d+', new_values[0], flags=re.S):
      # Iterar y asignar nuevos valores a cada celda
      for index, value in enumerate(new_values):
        # Asignar RFC
        if index == 0:
          row.iloc[0] = value
        # Asignar Denominación
        elif index == len(new_values)-1:
          row.iloc[1] = value
        # Asignar primeros tres valores
        elif index in [1,2,3]:
          row.iloc[index+1] = value
        # Asignar los cuatro siguientes
        elif index in [5,6,7,8]:
          row.iloc[index] = value
        else:
          row.iloc[index+1] = None
      # Return
      return row
    else:
      pass
    # Colocar sí en col. revisar
    row.iloc[-1] = "Sí"
    # Return
    return row
 
def distribuir_rfc_r_social(row):
  # Splitear valores
  valores = str(row.iloc[1]).split("\n")
  if len(valores) == 2:
    # Asignar RFC
    row.iloc[0] = valores[0]
    # Asignar denominación
    row.iloc[1] = valores[1]
  else:
     pass
  return row

def confirmar_c_err(string):
        while True:
            in_ = input(string) 
            if in_.lower() not in ["l","e"]:
                print("Ha ingresado un valor no permitido. Pruebe de nuevo")
            elif in_.lower()=="e":
                return exit()
            elif in_.lower()=="l":
                break
        return

def get_table_from_pdf(filepath, hojas, MAP_CAMPOS, DICT_CAT, denominacion, anio):
    """
    Función que lee el pdf y devuelve un DataFrame transformado del RDA
    """
    tables = camelot.read_pdf(filepath, pages=f"{hojas[0]}-{hojas[1]}", copy_text=['h', 'v'], line_scale=70)
    # Concateno todas las tablas en un dataframe
    df = pd.concat([t.df for t in tables])
    # Exportar archivo
    df.to_excel(f"./copia_local/Reporte de Donatarias Autorizadas/crudo-{hojas}.xlsx")
    # Confirmar transformación de errores
    confirmar_c_err("Se exportó el archivo crudo en la carpeta Reporte de Donatarias Autorizadas. Por favor le pedimos que se fije si todas las columnas tienen nombre  y en caso contrarios le pediremos que las borre y guarde el archivo (salvo que se trate de la última columna y el archivo haya sido leído incorrectamente, en cuyo caso habrá que desplazar los valores de dichos registros a la izquierda y guardarlo nuevamente).  Si ya los corrigió presione 'L', sino para terminar la ejecución del codigo presione 'E'.")
    # Leer nuevo archivo
    df = pd.read_excel(f"./copia_local/Reporte de Donatarias Autorizadas/crudo-{hojas}.xlsx")
    # Obtener y asignar headers
    headers = get_headers_from_dataframe(df, denominacion)
    df.columns = headers
    df = df[[x for x in df.columns.tolist() if 'TOTAL' not in x.upper()]]
    new_headers = get_new_headers(df.columns.tolist()[2:], MAP_CAMPOS)
    df.rename(new_headers, axis='columns', inplace=True)
    # Eliminar Fila 'Total General'
    df = df.loc[~df["RFC"].astype(str).str.startswith("TOTAL GENERAL"),:]

    # Eliminar las filas que son repetición de headers por cambio de entidad federativa
    df = df[df["RFC"] != "RFC"]

    # Eliminar todas las filas vacias
    df = df.dropna(subset=["RFC"])
    df = df[df["RFC"].astype(bool)] #?

    # Agregar las columnas de categoria y entidad federativa
    df["CATEGORIA"] = np.nan
    df["ENTIDAD FEDERATIVA"] = np.nan
    # Definir REGEX
    regex = r'[A-Z]{3}\d+'
    
    # Nueva columna revisar
    df["Revisar"] = "No"
    
    # Eliminar columna extra
    df.drop("Unnamed: 0", inplace = True, axis=1) if "Unnamed: 0" in df.columns else None
    
    # Filtrar y distribuir celdas bug
    df.loc[df[df.columns[3]].astype(str).apply(lambda x: True if re.findall(regex, x, flags=re.S) else False)] = df.loc[df[df.columns[3]].astype(str).apply(lambda x: True if re.findall(regex, x, flags=re.S) else False)].apply(lambda x: distribuir_celda_bug(x, len(df.columns)), axis=1)
    
    # Filtrar y distribuir segundo tipo de celdas bug (rfc-r_social bug)
    df.loc[(df[df.columns[1]].astype(str).apply(lambda x: True if re.findall(regex, x, flags=re.S) else False))&(df["Revisar"]=="No")] = df.loc[(df[df.columns[1]].astype(str).apply(lambda x: True if re.findall(regex, x, flags=re.S) else False))&(df["Revisar"]=="No")].apply(lambda x: distribuir_rfc_r_social(x), axis = 1)
    
    # Eliminar columna extra si vuelve a aparecer
    df.drop("Unnamed: 0", inplace = True, axis=1) if "Unnamed: 0" in df.columns else None
    
    # Set categorías y entidades
    set_categorias_entidades(df, anio)

    # Reemplazar valores de la columna categoría según el diccionario (esto se hace ahora para poder abarcar el filtro de la línea que sigue)
    df = df.replace({"CATEGORIA":DICT_CAT})
    
    # Eliminar categorías
    df = df.loc[~((df["RFC"] == df[df.columns[4]]) & (df["CATEGORIA"].apply(lambda x: len(x.split("\n"))) == 1)),:]
  
    # Eliminar 'TOTAL {entidad}' en celdas
    df = df.loc[~df["RFC"].astype(str).str.startswith("TOTAL "),:]
    
    # Llenar c/NaN
    df = df.replace("-","")
    
    return df