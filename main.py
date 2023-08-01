# Importar
import os   
import json
from gui import seleccionar_nombre_archivo_gui, cargar_archivo_gui, pantalla_carga_gui, seleccionar_año_gui, pantalla_finalizacion_gui,seleccionar_rangos_gui, seleccionar_denominacion_orgs
from transformar import transformar_itr, transformar_rda, transformar_sat
from cargar import cargar_sat, cargar_rda, cargar_itr, check_año_informe
from aux_funcs import confirmar_c_err
import pandas as pd

# Seleccionar archivo a cargar
OPCION = seleccionar_nombre_archivo_gui()

# Crear los directorios necesarios
if not os.path.exists("./copia_local"):
    os.mkdir("./copia_local")
    
# Informe de transparencia
if OPCION == "Informe de transparencia":
    # Crear los directorios necesarios
    if not os.path.exists("./copia_local/Informe de transparencia"):
        os.mkdir("./copia_local/Informe de transparencia")
    # Obtención de path
    filepath = cargar_archivo_gui(OPCION)
    # Obtención de año
    año = seleccionar_año_gui(OPCION)
    # Check año del informe en la base
    check_año_informe(año, "itr", "anio_informe")
    # Pantalla de carga
    pantalla_carga_gui()
    # Leer DF
    xls = pd.read_excel(filepath, sheet_name=None) 
    # Cargar de diccionarios
    with open("diccionarios.json", encoding='utf-8-sig') as f:
        DICCIONARIOS = json.load(f)[OPCION]
    # Transformación del df
    df, df_orgs = transformar_itr(xls, DICCIONARIOS, año)
    # Cargar a la base
    cargar_itr(xls, df, df_orgs, año)
    # Exportar
    df.to_excel(f"./copia_local/{OPCION}/{OPCION}-{año}.xlsx")
    df_orgs.to_excel(f"./copia_local/{OPCION}/{OPCION}-{año}-orgs.xlsx")
    # Pantalla finalización
    pantalla_finalizacion_gui(OPCION, año)


# Reporte de Donatarias Autorizadas (Rangos de prueba: 2022- [8,197],[200,382],[386,530], 2021- [8,180],[183,379],[383,566]
elif OPCION == "Reporte de Donatarias Autorizadas":
    # Crear los directorios necesarios
    if not os.path.exists("./copia_local/Reporte de Donatarias Autorizadas"):
        os.mkdir("./copia_local/Reporte de Donatarias Autorizadas")
    # Obtención de path
    filepath = cargar_archivo_gui(OPCION)   
    #filepath="./copia_local/Reporte de Donatarias Autorizadas/crudo-INGRESOS.xlsx"
    # Obtención de año
    año = seleccionar_año_gui(OPCION)
    # Check año del informe en la base
    check_año_informe(año, "rda", "anio_reporte")
    # Obtención de rangos
    rangos = seleccionar_rangos_gui(OPCION)
    # Obtención de denominación
    denominacion = seleccionar_denominacion_orgs(OPCION)
    # Pantalla de carga
    pantalla_carga_gui()
    # Cargar de diccionarios
    with open("diccionarios.json", encoding='utf-8-sig') as f:
        DICCIONARIOS = json.load(f)[OPCION]
    # Obtención y transformacion df's
    transformar_rda(filepath, rangos, DICCIONARIOS, denominacion, año)
    # Confirmar corrección de errores
    confirmar_c_err("Por favor corrija los errores que corresponden en los archivos exportados. RECUERDE luego de modificar los errores poner 'No' en la columna 'Revisar'. Si ya los corrigió presione 'L', sino para terminar la ejecución del codigo presione 'E'.")
    # Cargar 
    for key, rangos in rangos.items():
        if key=="-":
            continue
        # Leer archivos
        df = pd.read_excel(f"./copia_local/Reporte de Donatarias Autorizadas/check_{key}_RDA{año}.xlsx")
        # Filtrar errores si quedaron (revisar = Si)
        df = df.loc[df["Revisar"]=="No",:]
        # Filtrar columnas que no servirán para la carga
        df.drop([col for col in df.columns if (col not in DICCIONARIOS["MAP_CAMPOS"][key].values()) and (col not in ["rfc","r_social","entidad_fed","categoria", "anio_reporte"])] , axis = 1, inplace = True)
        # Cargar efectivamente
        cargar_rda(df, año, "rda")
        # Print
        print(f"Se cargó exitosamente la sección de {key}")
    # Pantalla finalización
    pantalla_finalizacion_gui(OPCION, año)

# Directorio SAT
elif OPCION == "Directorio SAT":
    # Crear los directorios necesarios
    if not os.path.exists("./copia_local/Directorio SAT"):
        os.mkdir("./copia_local/Directorio SAT")
    # Obtención de path
    filepath = cargar_archivo_gui(OPCION)
    # Obtención de año
    año = seleccionar_año_gui(OPCION)
    # Check año del informe en la base
    check_año_informe(año,"dir_sat","anio_directorio")
    # Pantalla de carga
    pantalla_carga_gui()
    # Cargar diccionarios
    with open("diccionarios.json", encoding='utf-8-sig') as f:
        DICCIONARIOS = json.load(f)[OPCION]
    # Leer DF
    df = pd.read_excel(filepath)
    # Transformación
    df = transformar_sat(df, DICCIONARIOS, año, filepath)
    # Cargar
    cargar_sat(df, año,"dir_sat")
    # Exportación
    df.to_excel(f"./copia_local/{OPCION}/{OPCION}-{año}.xlsx")
    # Pantalla finalización
    pantalla_finalizacion_gui(OPCION, año)
else:
    pass

    