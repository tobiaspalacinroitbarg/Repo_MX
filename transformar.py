# Importar
import pandas as pd
import uuid
from aux_funcs import get_headers_from_dataframe, get_table_from_pdf, get_new_headers, clear_merged_values
import ast
pd.options.mode.chained_assignment = None 

def transformar_itr(xls, diccionarios, año):
    """
    Función que transforma ITR y devuelve el DataFrame limpio junto con un sub - DataFrame de organizaciones.
    """
    # Rellenar NaN values en todas las hojas
    for x in xls.keys():
        try:
            xls[x]["Razón social"] = xls[x]["Razón social"].fillna("EMPTY_NAME")
        except:
            continue
    # Mergear 'Carátula' y 'Generales'
    df = xls['Carátula'].merge(xls['Generales'], how='left', on=['Rfc', 'Razón social', 'Folio'])
    # Mergear 'Nómina'
    df = df.merge(xls['Nómina'], how='left', on=['Rfc', 'Razón social', 'Folio'])
    # Reemplazar Entidades Federativas
    df.replace({'Entidad federativa':diccionarios["ENTIDAD_FEDERATIVA"]}, inplace=True)
    # Rellenar NaN values
    for column in ['Misión','Valores','Url']:
        df[column].fillna('', inplace=True)

    # Limpieza de campos
    # Sacar espacios a valores de 'Actividad' y 'Actividades adicionales'
    df['Actividad'] = df['Actividad'].str.strip()
    df['Actividades adicionales'] = df['Actividades adicionales'].apply(lambda x: ','.join([element.strip() for element in x.split(',')]) if pd.isna(x)==False else '')
    # Creación de nueva columna temporal que tendrá el primer elemento de 'Actividades adicionales'
    df['Primera actividad adicional'] = df['Actividades adicionales']
    df['Primera actividad adicional'] = df['Primera actividad adicional'].apply(lambda x: x.split(',',1)[0] if pd.isna(x)==False else '')
    # Creación de 'Categoría principal', variable que tendrá la Actividad si aparece y sino la Primera actividad adicional
    df['Categoría principal'] = ''
    df['Categoría principal'] = df.apply(lambda x: x['Actividad'] if x['Primera actividad adicional'] == '' else x['Primera actividad adicional'], axis=1)
    # Creación de columna 'Rubros autorizados' y su limpieza
    df['Rubros autorizados']  = ''
    df['Rubros autorizados']  = df.apply(lambda x: x['Actividad'] if x['Actividades adicionales'] == '' else f"{x['Actividad']},{x['Actividades adicionales']}", axis=1)
    for key, value in diccionarios["RUBROS"].items():
        df['Rubros autorizados'] = df['Rubros autorizados'].apply(lambda x: ','.join([value if element.strip()==key else element for element in x.split(',')]))
    df['Rubros autorizados'] = df['Rubros autorizados'].str.replace(',',';')
    # Creación de variable binaria que se define a partir de si la organización aparece (con su RFC) en la hoja de 'Actividades legislación'
    df['Actividades legislativas'] = df.apply(lambda x: True if x['Rfc'] in pd.unique(xls['Actividades legislación']['Rfc']) else False, axis=1)
    # Reemplazar valores de la columna 'Categoría principal' con el diccionario correspondiente
    df = df.replace({'Categoría principal':diccionarios["ACTIVIDADES"]})
    # Transformar columna 'Autorización extranjero' a Bool
    df.loc[df["Autorización extranjero"]=="Si","Autorización extranjero"] = True
    df.loc[df["Autorización extranjero"]=="No","Autorización extranjero"] = False
    # Creación del DataFrame de las organizaciones
    df_orgs = df[['Rfc','Razón social']]
    # Renombrar columnas igual a la base
    df_orgs.rename({'Rfc':'rfc','Razón social':'r_social'}, axis='columns', inplace=True)
    # Eliminar las que no tienen r_social
    df_orgs = df_orgs.loc[df_orgs["r_social"].isna()==False, :]

    # Modificaciones finales del DataFrame principal
    # Eliminar las columnas no deseadas para evitar problemas en la carga
    df.drop(["Folio","Razón social","Fecha de envío","Desconcentrada","Activo diferido","Número CP","Rubro","Actividad","Actividades adicionales","Activo circulante","Activo fijo","Dictamina","Rfc CP","Nombre CP","Primera actividad adicional"], axis='columns', inplace = True)
    # Rellenar campos vacíos
    df.fillna("NaN",inplace=True)
    # Aplicar columna de tipo uuid a cada fila del informe
    df["id"] = df.apply(lambda x: str(uuid.uuid4()), axis=1)
    # Definir variable anio_informe al año que ingresó el usuario
    df["anio_informe"] = año
    # Renombrar todas las columnas para poder cargarlas como corresponde a la base
    df.rename(diccionarios["COLUMNAS"]['Transparencia - principal'], axis='columns', inplace = True)
    # Return df's
    return df, df_orgs

def transformar_rda(filepath, rangos, diccionario, denominacion, año):
    """
     Función que transforma RDA y devuelve el DataFrame limpio
    """
    dataframes = dict()
    for key, rango in rangos.items():
        if rango == '-':
            continue
        else:
            print(f"Obteniendo datos de {key} evaluando el rango de páginas {rango}")
            df = get_table_from_pdf(filepath, ast.literal_eval(rango), diccionario["MAP_CAMPOS"][key], diccionario["DICT_CATEGORIAS_ESPECIALES"],denominacion, año)
            df = df.replace({"ENTIDAD FEDERATIVA":diccionario["DICT_ENTIDADES_FED"]})
            df.reset_index(inplace=True, drop=True)
                    
            # Revisión de errores en la columna de entidad federativa
            for entidad in pd.unique(df['ENTIDAD FEDERATIVA']):
                if entidad not in list(diccionario["DICT_ENTIDADES_FED"].values()):
                    print(f"Existen valores que no corresponden a una entidad federativa ({entidad})")

            df.reset_index(inplace=True, drop=True)
            df["Revisar"].fillna("No",inplace=True)
            df[denominacion].fillna("",inplace=True)
            df["RFC"].fillna("",inplace=True)
            for index, row in df.iterrows():
                if len(row["RFC"]) > 12 and (len(row[denominacion]) == 0 or row[denominacion].strip() == ''):
                    df.loc[index,denominacion] = row["RFC"][13:]
                    df.loc[index,"RFC"] = row["RFC"][:12]
            # Renombrar columnas estáticas
            df.rename({"RFC":"rfc", denominacion:"r_social","ENTIDAD FEDERATIVA":"entidad_fed","CATEGORIA":"categoria"},inplace=True, axis=1)
            # Crear columna anio_informe
            df["anio_reporte"] = int(año)
            # Limpieza de datos y columnas de totales/subtotales
            for column in df.columns[2:-4]:
                df[column]=df[column].astype(str).str.replace(',', '')
                df[column]=df[column].astype(str).str.replace("nan","")
                df[column] = df[column].fillna(0)
            df["categoria"] = df["categoria"].astype(str).str.upper()
            df["entidad_fed"] = df["entidad_fed"].astype(str).str.upper()
            
                #df[column] = df[column].apply(lambda x: clearMergedValues(x))
            dataframes[key] = df[[x for x in df.columns if 'TOTAL' not in x.upper()]]
            # Generación de archivos xlsx para revisión manual 
            dataframes[key].to_excel(f"./copia_local/Reporte de Donatarias Autorizadas/check_{key}_RDA{año}.xlsx") 
            # Imprimir
            print(f"Se ha exportado el archivo check_{key}_RDA{año}.xlsx a la carpeta ./copia_local/Reporte de Donatarias Autorizadas")
            # Return
            return
        
def transformar_sat(df, diccionarios, año, filepath):
    """
     Función que transforma el Dir. SAT y devuelve el DataFrame transformado
    """
    # Generar filtro para buscar la fila que empieza con ENTIDAD FEDERATIVA
    filas_filtradas = df[df.apply(lambda x: x.astype(str).str.startswith('ENTIDAD FEDERATIVA')).any(axis=1)]
    if not filas_filtradas.empty:
        skip_rows = filas_filtradas.index[0] + 1
    else:
        skip_rows = 0
    # Volver a leer df con las primeras filas skipeadas
    df = pd.read_excel(filepath, skiprows = skip_rows)
    # Quedarse solo con esas columnas
    df = df[[column for column in df.columns if column in list(diccionarios["COLUMNAS"].keys())]]  
    # Renombrar columnas
    df = df.rename(diccionarios["COLUMNAS"], axis='columns')
    # Renombrar valores de rubros
    df.replace({'rubro_aut':diccionarios["RUBROS"]}, inplace = True)
    # Crear columna anio directorio y tipo de registro
    df["anio_directorio"] = año
    #df['RecordType'] = '0125f000000QPUdAAO'
    # Eliminar columnas
    df.drop([col for col in list(df.columns) if str(col).startswith("Unnamed")], axis=1, inplace=True)
    # Filtrar para que tengan distintos RFC's
    df.drop_duplicates(subset='rfc', keep="first", inplace = True)
    # Convertir columna oficio a datetime y manejar errores
    df['f_oficio'] = pd.to_datetime(df['f_oficio'], errors='coerce')    
    # Convertir los objetos datetime a cadenas de texto en el formato deseado
    df['f_oficio'] = df['f_oficio'].dt.strftime('%Y-%m-%d')
    # Eliminar registros vacíos
    df = df[df["rfc"].notna()]
    # Transformación de columnas que serán cargadas como texto para prevenir errores de tipo
    df["rfc"]= df["rfc"].astype(str)
    df["entidad_fed"] = df["entidad_fed"].astype(str)
    df["rep_legales"] = df["rep_legales"].astype(str)
    df["domicilio"] = df["domicilio"].astype(str)
    df["f_oficio"] = df["f_oficio"].astype(str)
    df["oficio"] = df["oficio"].astype(str)
    df["telefono"] = df["telefono"].astype(str) 
    df["correo_electronico"] =  df["correo_electronico"].astype(str)
    df["r_social"] = df["r_social"].astype(str)
    return df
