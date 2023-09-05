# Importar
import psycopg2
from psycopg2.extras import execute_values
import pandas as pd
from pandas.api.types import is_numeric_dtype
import json
import numpy as np
from aux_funcs import crear_query

# Conexión
conn = psycopg2.connect(
    host="localhost",
    database="ZIGLA_DB",
    user="postgres",
    password="asd123"
)
# Creación del cursor
cursor = conn.cursor()


def insertar_orgs(df):
    """
    Función que inserta organizaciones NUEVAS a la base al pasarle un df 
    """
    # Creación de queries
    upload_query = "INSERT INTO org (rfc, r_social) VALUES %s"
    get_query = "SELECT rfc, r_social from org" 
    # Creación de la lista de tuplas del df_org
    df_values = [(d['rfc'], d['r_social']) for d in df.to_dict('records')]
    # Eliminar nan's de la lista de tuplas del df_org
    df_values = [value for value in df_values if value[0] not in ["nan","NaN",np.nan]]
    # Ejecutar query de obtención de datos
    cursor.execute(get_query)
    # Obtener lista de tuplas de db_values
    db_values = cursor.fetchall()
    # lista de tuplas de RFCS
    lista_rfcs = [db_value[0] for db_value in db_values]
    # Crear nueva lista de valores que no están presentes en la lista de RFCS
    new_df_values = [df_value for df_value in df_values if df_value[0] not in lista_rfcs]
    if new_df_values:
        # Ejecutar query de carga de datos
        execute_values(cursor, upload_query, new_df_values)
    # Imprimir por consola repetidos para el usuario
    print(f"Se van a agregar {len(new_df_values)} registros, y se encontraron {len(df_values)-len(new_df_values)} organizaciones repetidas.")
    conn.commit()

def insertar_informe_base(df, table):
    """
    Función que inserta un informe a la base
    """
    # Pasar df a un dict {columna:registro}
    data = df.to_dict('records')
    # Obtener columnas
    columns = list(data[0].keys())
    # Obtener valores
    values =[tuple(d.values()) for d in data]
    # Definir la consulta
    query = f"INSERT INTO {table} ({','.join(columns)}) VALUES %s"
    # Ejecutar y cargar datos
    execute_values(cursor, query, values)
    # Guardar
    conn.commit()
    # Imprimir por consola
    print("Se insertó el informe principal")
    # Return
    return

def check_año_informe(año, table, column):
    """
    Función que se fija si existe un informe del mismo año en la base para no evitar subirlo dos veces
    """
    # Correr consulta (¿Existe algún informe con el mismo año que el ingresado por el usuario?)
    cursor.execute(f"SELECT * FROM public.{table} WHERE {column} = {año}")
    # Si no es vacío, o sea existe:
    if cursor.fetchall() != []:
        variable = input(f"Ya existen datos para {año}. Verifique que se trate del archivo correspondiente. Presione la letra 'S' si desea continuar igual ")
        if variable.lower() == "s":
            return
        else:
            exit()

def actualizar_orgs(df, año, informe, key=0):
    """
    Función que actualiza los datos de la tabla org si es necesario
    """
    # Armar lista de rfc's
    subidos_rfc = df["rfc"].to_list()
    # Limpiar rfcs vacíos
    subidos_rfc = [str(value) for value in subidos_rfc if value not in ["nan","NaN",np.nan]]
    # Ejecución de consulta (agarrar todos los rfc's, y los valores de la col. ult_anio_x de las organizaciones cuyos informes fueron cargados recientemente, filtrando por sus rfc's)
    cursor.execute(f"SELECT rfc, r_social, ult_anio_itr, ult_anio_rda, ult_anio_sat FROM public.org WHERE rfc in {tuple(subidos_rfc)}")
    # Creación de un df de los datos provenientes de la base
    df_orgs_db = pd.DataFrame(cursor.fetchall(), columns=['rfc', 'r_social', 'ult_anio_itr','ult_anio_rda','ult_anio_sat'])
    # Rellenar valores vacíos
    df_orgs_db.fillna({"ult_anio_itr":0,"ult_anio_rda":0,"ult_anio_sat":0},inplace=True)
    # Filtrar por las orgs que quiero actualizar itr>rda>sat
    if informe == "itr" and len(df_orgs_db)>0:
        # Filtro 1
        df_orgs_db_1 = df_orgs_db.loc[((df_orgs_db["ult_anio_itr"] < int(año)) | (df_orgs_db["ult_anio_itr"] == 0)) & ((df_orgs_db["ult_anio_sat"] <= int(año)) | (df_orgs_db["ult_anio_sat"] == 0)) & ((df_orgs_db["ult_anio_rda"] <= int(año)) | (df_orgs_db["ult_anio_rda"] == 0)), :]
        # Filtro 2
        df_orgs_db_2 = df_orgs_db.loc[(df_orgs_db["ult_anio_itr"]<int(año))|(df_orgs_db["ult_anio_itr"] == 0),:]
        # Asignar año a columna correspondiente
        df_orgs_db_1["ult_anio_itr"] = int(año)   
        df_orgs_db_2["ult_anio_itr"] = int(año) 
        # Creación de otros df con datos provenientes del itr_ppal que se cargarán a la tabla org
        df_orgs_aux_1 = df[["rfc","categoria_ppal","entidad_fed","rubros_aut"]]
        df_orgs_aux_2 = df[["rfc","mision","vision","web"]]
        # Renombrar las columnas distintas en la base
        df_orgs_aux_1.rename({'rubros_aut':'rubro_aut', 'categoria_ppal':'categoria'}, axis='columns', inplace=True)
    elif informe == "rda" and len(df_orgs_db)>0:
        # Filtro 1
        df_orgs_db_1 = df_orgs_db.loc[((df_orgs_db["ult_anio_itr"]<int(año)) | (df_orgs_db["ult_anio_itr"] == 0))&((df_orgs_db["ult_anio_sat"]<=int(año)) | (df_orgs_db["ult_anio_sat"] == 0))&((df_orgs_db["ult_anio_rda"]<int(año)) | (df_orgs_db["ult_anio_rda"] == 0)), :]
        # Filtro 2
        df_orgs_db_2 = df_orgs_db.loc[(df_orgs_db["ult_anio_rda"]<int(año))|(df_orgs_db["ult_anio_rda"] == 0),:]
        # Asignar año
        df_orgs_db_1["ult_anio_rda"] = int(año)
        df_orgs_db_2["ult_anio_rda"] = int(año)
        # Cols a agregar
        df_orgs_aux_1 = df[["rfc","entidad_fed","categoria"]]
        df_orgs_aux_2 = False
    elif informe == "dir_sat" and len(df_orgs_db)>0:
        # Filtro
        df_orgs_db_1 = df_orgs_db.loc[((df_orgs_db["ult_anio_itr"]<int(año)) |(df_orgs_db["ult_anio_itr"] == 0))&((df_orgs_db["ult_anio_sat"]<int(año)) | (df_orgs_db["ult_anio_sat"] == 0))&((df_orgs_db["ult_anio_rda"]<int(año)) | (df_orgs_db["ult_anio_rda"] == 0)), :]
        # Filtro 2
        df_orgs_db_2 = df_orgs_db.loc[(df_orgs_db["ult_anio_sat"]<int(año))|(df_orgs_db["ult_anio_sat"] == 0),:]
        # Crear columna ult_anio_sat
        df_orgs_db_1["ult_anio_sat"] = int(año)
        df_orgs_db_2["ult_anio_sat"] = int(año)
        # Crear DF's aux
        df_orgs_aux_1 = df[["rfc","entidad_fed","rubro_aut"]]
        df_orgs_aux_2 = df[["rfc","domicilio","rep_legales","oficio","f_oficio","telefono","correo_electronico"]]
    # Si no hay organizaciones para actualizar, que regrese
    else:
        print("No hay información para actualizar de las organizaciones")
        return False
    # Realizar merge
    df_orgs_final_1 = df_orgs_aux_1.merge(df_orgs_db_1, on=['rfc'], how='inner')
    df_orgs_final_2 = df_orgs_aux_2.merge(df_orgs_db_2, on=['rfc'], how='inner')
    # Imprimir datos sobre actualización de org
    print(f"Se van a actualizar los datos en común de {len(df_orgs_final_1)} organizaciones")
    # Definir consulta a realizar
    consulta, tupla_valores = crear_query(df_orgs_final_1) 
    # Ejecutar query
    cursor.execute(consulta, tupla_valores)
     # Guardar
    conn.commit()
    if informe != "rda":
        # Imprimir datos sobre actualización de org
        print(f"Se van a actualizar los datos únicos de {informe} de {len(df_orgs_final_2)} organizaciones")
        # Definir consulta a realizar
        consulta, tupla_valores = crear_query(df_orgs_final_2) 
        # Ejecutar query
        cursor.execute(consulta, tupla_valores)
        # Guardar
        conn.commit()
    # Avisar por consola
    print("Se terminó la actualización de orgs.")
    # Return
    return


def cargar_aux(df, objeto, anio, count_gastos=0):
    """
    Función auxiliar que carga las tablas asociadas al itr.
    Para ello:
    1- Llena NaN values
    2- Elimina columna rfc
    3- Hace rename de columnas de acuerdo al objeto
    """
    # Cargar de diccionarios
    with open("diccionarios.json", encoding='utf-8-sig') as f:
        DICCIONARIOS = json.load(f)["Informe de transparencia"]
    # Iterar por columnas
    for columna in list(df.columns):
        value = 0
        if is_numeric_dtype(df[columna]) == False:
            value = ''
        # Rellenar valores NaN
        df.loc[:,columna] = df[columna].fillna(value)
        if columna == 'Rfc':
            # Eliminar columna Rfc
            df.drop('Rfc',axis=1,inplace=True)
    # Renombrar columnas
    df_final = df.rename(DICCIONARIOS["COLUMNAS"][objeto], axis='columns')
    # Guardar una copia local  en formato .xlsx
    if objeto == "Gastos":
        # Exportar el chunk
        df_final.to_excel('./copia_local/Informe de transparencia/tabla_{}_{}_{}.xlsx'.format(objeto, anio, count_gastos))
    else:
        # Exportar objeto
        df_final.to_excel('./copia_local/Informe de transparencia/tabla_{}_{}.xlsx'.format(objeto, anio))
    # Cargar a la base
    # Obtener nombre de la tabla como está en la base
    nombre_tabla = DICCIONARIOS["NOMBRES_BD"][objeto]
    # Pasar df a un dict {columna:registro}
    data = df_final.to_dict('records')
    # Obtener columnas
    columns = list(data[0].keys())
    # Obtener valores
    values =[tuple(d.values()) for d in data]
    # Definir la consulta 
    query = f"INSERT INTO {nombre_tabla} ({','.join(columns)}) VALUES %s"
    # Ejecutar y cargar datos
    execute_values(cursor, query, values)
    # Guardar
    conn.commit()
    # Print
    if objeto == "Gastos":
        print("Se ha cargado un chunk (10k de registros) de Gastos")
    else:
        print(f"Se ha cargado {objeto}")

def cargar_tablas_asociadas(xls, subidos_itr, año):
    """
    Función que carga las tablas asociadas al informe ppal
    """
    # Cargar de diccionarios
    with open("diccionarios.json", encoding='utf-8-sig') as f:
        DICCIONARIOS = json.load(f)["Informe de transparencia"]
    # Armado de DF de subidos_itr para merge
    df_subidos_itr = pd.DataFrame(subidos_itr)
    df_subidos_itr.columns = ["Rfc","Informe de transparencia"]
    
    # Órgano de gobierno
    df_organo_gob = xls["Órgano de gobierno"].merge(df_subidos_itr, on=['Rfc'], how='inner')
    df_organo_gob.drop([col for col in list(df_organo_gob.columns) if col not in (['Rfc'] + list(DICCIONARIOS["COLUMNAS"]['Órgano de gobierno'].keys()))], axis=1, inplace=True)
    cargar_aux(df_organo_gob, "Órgano de gobierno", año)
    
    # Gastos
    df_gastos = xls["Gastos"].merge(df_subidos_itr, on=['Rfc'], how='inner')
    df_gastos.rename({'Monto nacional admin':'Monto nacional administrativo','Monto extranjero admin':'Monto extranjero administrativo'}, axis='columns', inplace=True)
    df_gastos.drop([col for col in list(df_gastos.columns) if col not in (['Rfc'] + list(DICCIONARIOS["COLUMNAS"]['Gastos'].keys()))], axis=1, inplace=True)
    df_gastos.drop_duplicates(subset=["id_itr","concepto"], inplace=True)
    # Inicializar count
    count = 0
    for chunk in [df_gastos.iloc[x:x+10000,:] for x in range(0, len(df_gastos), 10000)]:
        count+=1
        cargar_aux(chunk, 'Gastos', año, str(count))
    
    # Sector beneficiado
    df_sector_benef = xls['Sector beneficiado'].rename({'Id de donativo especie':'ID del donativo en especie'}, axis='columns')
    df_sector_benef = df_sector_benef.merge(df_subidos_itr, on=['Rfc'], how='inner')
    df_sector_benef.drop([col for col in list(df_sector_benef.columns) if col not in (['Rfc'] + list(DICCIONARIOS["COLUMNAS"]['Sector beneficiado'].keys()))], axis=1, inplace=True)
    cargar_aux(df_sector_benef, "Sector beneficiado", año)
    
    # Ingreso donativos recibidos
    df_ingreso_donativos = xls['Ingreso por donativos'].melt(id_vars=['Rfc', 'Donante'], value_vars=['Monto efectivo','Monto especie'], var_name='Tipo de registro' ,value_name='Monto')
    df_ingreso_donativos = df_ingreso_donativos[df_ingreso_donativos['Monto']!=0]
    df_ingreso_donativos['Tipo de registro'].replace({'Monto efectivo':'0125f000000Qm9bAAC', 'Monto especie':'0125f000000Qm9gAAC'}, inplace=True)
    df_ingreso_donativos = df_ingreso_donativos.merge(df_subidos_itr, on=['Rfc'], how='inner')
    df_ingreso_donativos.drop([col for col in list(df_ingreso_donativos.columns) if col not in (['Rfc'] + list(DICCIONARIOS["COLUMNAS"]['Ingreso por donativos'].keys()))], axis=1, inplace=True)
    cargar_aux(df_ingreso_donativos, "Ingreso por donativos", año)
    
    # Necesidades atendidas 
    df_necesidades_atend = xls['Destino de donativos'].merge(df_subidos_itr, on=['Rfc'], how='inner')
    df_necesidades_atend.rename({'Número de beneficiados':'Necesidades atendidas'}, axis='columns', inplace=True)
    df_necesidades_atend.drop([col for col in list(df_necesidades_atend.columns) if col not in (['Rfc'] + list(DICCIONARIOS["COLUMNAS"]['Destino de donativos'].keys()))], axis=1, inplace=True)
    df_necesidades_atend.replace({'Entidad federativa':DICCIONARIOS["ENTIDAD_FEDERATIVA"]}, inplace=True)
    cargar_aux(df_necesidades_atend,'Destino de donativos', año)
    
    # Transmisión de patrimonio
    df_transm_patrimonio = xls['Transmisión de patrimonio'].merge(df_subidos_itr, on=['Rfc'], how='inner')
    df_transm_patrimonio.rename({"Rfc destinatario":"RFC de la donataria", "Rfc":"RFC del donante", 'Total':'Monto total'}, axis='columns', inplace=True)
    df_transm_patrimonio['RFC de la donataria'] = df_transm_patrimonio['RFC de la donataria'].replace({'XEXX010101000':'XEXX01010100', 'XAXX010101000':'XAXX01010100'})
    df_transm_patrimonio.drop([col for col in list(df_transm_patrimonio.columns) if col not in (['Rfc'] + list(DICCIONARIOS["COLUMNAS"]['Transmisión de patrimonio'].keys()))], axis=1, inplace=True)
    cargar_aux(df_transm_patrimonio,'Transmisión de patrimonio', año)
    
    # Donativos otorgados
    df_donativos_otorgados =  xls['Donativos otorgados'].merge(df_subidos_itr, on=['Rfc'], how='inner')
    df_donativos_otorgados.rename({"Rfc destinatario": "RFC de la donataria","Rfc":"RFC del donante", "Informe de transparencia":"Informe de transparencia asociado"}, axis='columns', inplace=True)
    df_donativos_otorgados['RFC de la donataria'] = df_donativos_otorgados['RFC de la donataria'].replace({'XEXX010101000':'XEXX01010100', 'XAXX010101000':'XAXX01010100'})
    df_donativos_otorgados.drop([col for col in list(df_donativos_otorgados.columns) if col not in (list(DICCIONARIOS["COLUMNAS"]['Donativos otorgados'].keys()))], axis=1, inplace=True)
    cargar_aux(df_donativos_otorgados,'Donativos otorgados', año)

    # Control de donativos
    df_control_donativos = xls['Control de donativos'].rename({'Id de donativo especie':'Id de donativo en especie'}, axis='columns')
    df_control_donativos = df_control_donativos.merge(df_subidos_itr, on=['Rfc'], how='inner')
    df_control_donativos['Fecha de destrucción'] = df_control_donativos['Fecha de destrucción'].apply(lambda x: x.split(" ")[0])
    df_control_donativos['Fecha de destrucción'] = pd.to_datetime(df_control_donativos['Fecha de destrucción'], format='%m/%d/%Y')
    df_control_donativos['Fecha de destrucción'] = df_control_donativos['Fecha de destrucción'].dt.strftime('%Y-%m-%d')
    df_control_donativos.drop([col for col in list(df_control_donativos.columns) if col not in (['Rfc'] + list(DICCIONARIOS["COLUMNAS"]['Control de donativos'].keys()))], axis=1, inplace=True)
    cargar_aux(df_control_donativos, 'Control de donativos', año)

    # Inversiones financieras
    df_inversiones_financieras = xls['Inversiones financieras'].merge(df_subidos_itr, on=['Rfc'], how='inner')
    df_inversiones_financieras.drop([col for col in list(df_inversiones_financieras.columns) if col not in (['Rfc'] + list(DICCIONARIOS["COLUMNAS"]['Inversiones financieras'].keys()))], axis=1, inplace=True)
    cargar_aux(df_inversiones_financieras, 'Inversiones financieras', año)

def cargar_itr(xls, df, df_org, año):
    """
    Función general que carga todo lo relacionado al itr a la base
    """
    # Insertar organizaciones nuevas
    insertar_orgs(df_org)
    # Insertar informe base
    insertar_informe_base(df,"itr")
    # Actualizar información de las organizaciones
    df_orgs_final = actualizar_orgs(df, año, "itr")
    # Cargar objetos asociados
    cargar_tablas_asociadas(xls, df[["rfc","id"]].to_dict(), año)
    #Return
    return df_orgs_final

def cargar_sat(df, año, opcion):
    """
    Función que carga el SAT, inserta datos de nuevas orgs provenientes del mismo y actualiza los datos en caso de que lo requiera.
    """
    # Insertar organizaciones nuevas
    insertar_orgs(df)
    # Insertar informe principal
    insertar_informe_base(df,opcion)
    # Actualizar organizaciones
    actualizar_orgs(df,año,opcion)

    
def cargar_rda(df, año, opcion):
    """
    Función que carga el RDA, inserta datos de nuevas orgs provenientes del mismo y actualiza los datos en caso de que lo requiera.
    """
    # Insertar organizaciones nuevas
    insertar_orgs(df)
    # Rellenar con 0 los NaN
    df.fillna(0, inplace = True)
    # Insertar informe principal, eliminando columnas que no están en la tabla primero 
    insertar_informe_base(df.drop(["r_social","entidad_fed","categoria"],axis = 1), opcion)
    # Actualizar organizaciones
    actualizar_orgs(df,año,opcion)
    # Return
    return
