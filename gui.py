# Importar
from tkinter import * 
import tkinter as tk
from tkinter import filedialog
import warnings
import time
from PIL import Image, ImageTk
import ast
# Filtro de Warning para el usuario
warnings.filterwarnings("ignore", message="Workbook contains no default style")

def leer_path(win, OPCION):
    """
    Función para obtener el filepath del archivo
    """
    global filepath
    print(OPCION)
    if OPCION == "Informe de transparencia":
        filepath = filedialog.askopenfilename(title="Seleccionar archivo", filetypes=(("Excel files","*.xlsx"),))
    elif OPCION == "Directorio SAT":
        filepath = filedialog.askopenfilename(title="Seleccionar archivo", filetypes=(("Excel files","*.xls"),))
    else:
        filepath = filedialog.askopenfilename(title="Seleccionar archivo", filetypes=(("pdf file","*.pdf"),))
    if not filepath:
        print("Error, no se encontró/seleccionó ningún archivo")    
    else:
        print("Se seleccionó correctamente el archivo")
        win.destroy()


def guardar_opcion(opcion_ingresada, win):
    """
    Función que se ejecutará cuando se seleccione una opción para guardarla
    """
    global opcion
    opcion = opcion_ingresada
    win.destroy()


def guardar_año(entry, win):
    """
    Función que se ejecuta al tocar el boton "Aceptar", la cual guarda el año (entry.get())
    """
    global año
    año = entry
    win.destroy() if año.isnumeric()==True and len(año)==4 and 2014<int(año)<2024 else print("ERROR: solo se puede ingresar valores numéricos")

def guardar_denominacion(entry, win):
    """
    Función que se ejecuta al tocar el boton "Aceptar", y guarda la denominación
    """
    global denominacion
    denominacion = entry
    win.destroy() if denominacion else print("ERROR: solo se puede ingresar valores numéricos") #TODO: Verificar que el input sea correcto



def guardar_rangos(entrys, win):
    """
    Función que se ejecuta al tocar el boton "Aceptar", la cual guarda los rangos
    """
    global rangos
    rangos = {"gastos":entrys[1],"donativos":entrys[0],"ingresos":entrys[2]}
    for key, rango in rangos.items():
        if rango == "-":
            continue 
        result = ast.literal_eval(rango)
        if len(result) != 2 or result[0] >= result[1]:
            print("Error en la sintaxis del rango. Pruebe de nuevo")
            raise ValueError
        else:
            if int(result[0]) and int(result[1]):
                continue
    win.destroy()


def seleccionar_nombre_archivo_gui():
    """
    Función que crea la ventana visual para seleccionar el nombre del archivo fuente a cargar
    """
    # Crea una nueva ventana
    win = tk.Tk()
    win.geometry("700x400")
    win.config(bg="#F0F0F0")
    win.title("Carga de archivos")
    # Crea una barra de menú
    menubar = tk.Menu(win)
    # Crear variable de control
    opcion_seleccionada = StringVar()
    # Crea un menú "Opciones"
    opciones_menu = tk.Menu(menubar, tearoff=0)
    # Agrega las opciones al menú "Opciones"
    opciones_menu.add_command(label="Informe de transparencia", command=lambda: guardar_opcion("Informe de transparencia", win))
    opciones_menu.add_command(label="Directorio SAT", command=lambda: guardar_opcion("Directorio SAT", win))
    opciones_menu.add_command(label="Reporte de Donatarias Autorizadas", command=lambda: guardar_opcion("Reporte de Donatarias Autorizadas", win))

    # Agrega el menú "Seleccionar..." a la barra de menú
    menubar.add_cascade(label="Seleccionar...", menu=opciones_menu)

    #Agrego título
    mensaje_1 = tk.Message(win, text="¡Bienvenido!", font='Arial 20', fg='#2D2E2E', bg="#F0F0F0", width = 500, pady=35, justify="center")
    mensaje_1.pack()
    #Agrego mensaje
    mensaje_2 = tk.Message(win, text="Por favor, seleccione el tipo de archivo que desea subir.", font='Arial 18', fg='#2D2E2E', bg="#F0F0F0", width = 500, pady=0)
    mensaje_2.pack()
    # Carga la imagen
    imagen = Image.open("images/zigla.png")
    # Crea un objeto ImageTk para mostrar la imagen en el widget Label
    imagen_tk = ImageTk.PhotoImage(imagen)
    # Crea un widget Label y muestra la imagen
    etiqueta_imagen = tk.Label(win, image=imagen_tk)
    etiqueta_imagen.pack()
    # Configura la barra de menú de la ventana principal
    win.config(menu=menubar)
    win.mainloop()
    return opcion


def cargar_archivo_gui(OPCION):
    """
    Función que crea la ventana visual para subir el archivo y devuelve el DF o lo que corresponda
    """
    #Creación de la ventana
    win=tk.Tk()
    #Personalización
    win.title(f"Carga de {OPCION}")
    win.geometry("700x250")
    win.config(bg="#f2f3f1")
    #Creación del mensaje
    mensaje = tk.Message(win, text="Por favor, busque el archivo en su computadora.", font='Arial 18', fg='#2D2E2E', bg="#f2f3f1", width = 500, pady=35, justify="center")
    mensaje.pack()
    # Crear botón para abrir el diálogo y seleccionar el archivo
    button = tk.Button(win, text="Buscar...", pady=10, font='Arial 14', bg='#0077B5', fg='#FFFFFF', command=lambda:leer_path(win, OPCION))
    button.pack(pady=10)
    win.mainloop()
    #Devuelvo filepath
    return filepath

def seleccionar_año_gui(OPCION):
    """
    Función que crea la interfaz gráfica para que el usuario ingrese el valor del año del informe
    """
    # Crear la ventana principal
    win = tk.Tk()
    win.geometry("700x250")
    win.title(f"Carga de {OPCION}")
    win.configure(bg="#f2f3f1")

    # Crear etiqueta para ingresar el año
    year_label = tk.Label(win, text=f"Ingrese el año del {OPCION}:", font='Arial 14', fg='#2D2E2E', bg="#f2f3f1")
    year_label.pack(pady=10)

    # Crear cuadro de texto para ingresar el año
    year_entry = tk.Entry(win, width=5, font='Arial 12')
    year_entry.pack(pady=5)

    # Crear botón para obtener el año ingresado,  personalización
    year_button = tk.Button(win, text="Aceptar", font='Arial 12 bold', bg='#0077B5', fg='#FFFFFF', pady=10, command=lambda:guardar_año(year_entry.get(),win))
    year_button.pack(pady=10)

    # Iniciar el bucle de la ventana principal
    win.mainloop()
    return año

def seleccionar_rangos_gui(OPCION):
    """
    Función que crea la interfaz gráfica para ingresar el rango en el caso del RDA
    """
    # Crear la ventana principal
    win = tk.Tk()
    win.geometry("1000x450")
    win.title(f"Carga de {OPCION}")
    win.configure(bg="#f2f3f1")

    # Título
    titulo_label = tk.Label(win, text=f"Ingrese los rangos de hojas correspondientes a cada parte del informe, si no corresponde coloque dos '-'", font='Arial 14', fg='#2D2E2E', bg="#f2f3f1")
    titulo_label.pack(pady=10)
    
    # Ejemplo
    ej_label = tk.Label(win, text=f"Por ejemplo: [8,197]", font='Arial 10', fg='#2D2E2E', bg="#f2f3f1")
    ej_label.pack(pady=10)

    # Crear etiqueta para ingresar rango de donativos
    donativos_label = tk.Label(win, text=f"Donativos", font='Arial 10 bold', fg='#2D2E2E', bg="#f2f3f1")
    donativos_label.pack(pady=10)

    # Crear cuadro de texto para ingresar el rango de donativos
    donativos_entry = tk.Entry(win, width=7, font='Arial 12')
    donativos_entry.pack(pady=10)

    # Crear etiqueta para ingresar el rango de ingresos
    ingresos_label = tk.Label(win, text=f"Ingresos", font='Arial 10 bold', fg='#2D2E2E', bg="#f2f3f1")
    ingresos_label.pack(pady=10)

    # Crear cuadro de texto para ingresar el rango de ingresos
    ingresos_entry = tk.Entry(win, width=7, font='Arial 12')
    ingresos_entry.pack(pady=10)

    # Crear etiqueta para ingresar el rango de gastos
    gastos_label = tk.Label(win, text=f"Gastos", font='Arial 10 bold', fg='#2D2E2E', bg="#f2f3f1")
    gastos_label.pack(pady=10)

    # Crear cuadro de texto para ingresar el rango de gastos
    gastos_entry = tk.Entry(win, width=7, font='Arial 12')
    gastos_entry.pack(pady=10)

    # Crear botón para obtener todos los datos y cerrar
    check_button = tk.Button(win, text="Aceptar", font='Arial 12 bold', bg='#0077B5', fg='#FFFFFF', pady=10, command=lambda:guardar_rangos([x.get() for x in [donativos_entry, gastos_entry, ingresos_entry]],win))
    check_button.pack(pady=10)

    # Iniciar el bucle de la ventana principal
    win.mainloop()
    return rangos


def seleccionar_denominacion_orgs(OPCION):
    """
    Función que crea la interfaz gráfica que busca obtener el dato de la denominación de orgs
    """
    # Crear la ventana principal
    win = tk.Tk()
    win.geometry("1250x250")
    win.title(f"Carga de {OPCION}")
    win.configure(bg="#f2f3f1")

    # Crear etiqueta para ingresar el año
    denominacion_label = tk.Label(win, text=f"Especifique cómo se denomina en la tabla a las organizaciones, respetando EXACTAMENTE la forma en que está escrito en el {OPCION}:", font='Arial 12', fg='#2D2E2E', bg="#f2f3f1")
    denominacion_label.pack(pady=10)

    # Crear cuadro de texto para ingresar el año
    denominacion_entry = tk.Entry(win, width=5, font='Arial 12')
    denominacion_entry.pack(pady=5)

    # Crear botón para obtener el año ingresado,  personalización
    denominacion_button = tk.Button(win, text="Aceptar", font='Arial 12 bold', bg='#0077B5', fg='#FFFFFF', pady=10, command=lambda:guardar_denominacion(denominacion_entry.get(),win))
    denominacion_button.pack(pady=10)

    # Iniciar el bucle de la ventana principal
    win.mainloop()
    return denominacion

def pantalla_carga_gui():
    """
    Función que crea la interfaz gráfica para avisar que se estará cargando el archivo a la base
    """
    # Crear la ventana principal
    win = tk.Tk()
    win.geometry("700x370")
    win.title("Proceso de carga")
    win.configure(bg="#f0f0f0")
    #Creación del mensaje 1
    mensaje = tk.Message(win, text=f"Cargando...por favor aguarde. ", font='Arial 20', fg='#2D2E2E', bg="#f0f0f0", width = 500, pady=35, justify="center")
    mensaje.pack()
    #Creación del segundo mensaje
    mensaje_2 = tk.Message(win, text=f"Mientras el archivo esté siendo cargado, la pestaña permanecerá temporalmente cerrada. ", font='Arial 14', fg='#4c4d4d', bg="#f0f0f0", width = 500, pady=10, justify="center")
    mensaje_2.pack()

    # Carga la imagen
    imagen = Image.open("images/carga.png")
    imagen = imagen.resize((140,140), Image.ANTIALIAS)
    # Crea un objeto ImageTk para mostrar la imagen en el widget Label
    imagen_tk = ImageTk.PhotoImage(imagen)
    # Crea un widget Label y muestra la imagen
    etiqueta_imagen = tk.Label(win, image=imagen_tk)
    etiqueta_imagen.pack()
    win.after(3000,lambda:win.destroy())
    win.mainloop()
        
def pantalla_finalizacion_gui(OPCION, año):
    """
    Función que crea la interfaz gráfica para avisar que el proceso ha finalizado y se desarrolló correctamente
    """
    # Crear la ventana principal
    win = tk.Tk()
    win.geometry("700x500")
    win.title("Éxito")
    win.configure(bg="#f0f0f0")
    #Creación del mensaje
    mensaje = tk.Message(win, text=f"¡Se cargó el {OPCION} {año} con éxito! .", font='Arial 20', fg='#2D2E2E', bg="#f0f0f0", width = 500, pady=35, justify="center")
    mensaje.pack()
    # Carga la imagen
    imagen = Image.open("images/exito.png")
    # Crea un objeto ImageTk para mostrar la imagen en el widget Label
    imagen_tk = ImageTk.PhotoImage(imagen)
    # Crea un widget Label y muestra la imagen
    etiqueta_imagen = tk.Label(win, image=imagen_tk)
    etiqueta_imagen.pack()
    win.mainloop()

