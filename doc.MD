# Repositorio de Datos MX  |  Versión 1.0.0

El objetivo del código es cargar a una base de datos en PostgreSQL los distintos archivos brindados por el gobierno de México (Informe de Transparencia, Reporte de Donatarias Autorizadas y Directorio SAT).

### Cómo ejecutar

Previo a correr el código, se debe tener creada en PostgreSQL una base de datos con las tablas y columnas correspondientes. Para ello, se puede correr la consulta en SQL que está guardada en el archivo .PDF en la sección de 'Design', en el [Trello]([Trello](https://trello.com/b/JI2jQO1e/repo-sat-rda).). Una vez creada, se tienen que cambiar, dentro del archivo `cargar.py`, los parámetros de la conexión correspondientes a la base (database - username - password)

Luego, habiendo instalado las diferentes dependencias que figuran en el archivo `requirements.txt`, ya se pueden subir las bases previas al 2019 desde el archivo `cargar_leg.py`. Si ya están cargadas a la base, se puede ejecutar directamente el archivo `main.py`.  Se debe seleccionar el archivo a cargar y seguir las instrucciones, que varían dependiendo el archivo. Por lo general, se piden datos como el año del archivo a cargar, etc. 

**Obs:** Si se carga el Reporte de Donatarias Autorizadas, hay que tener cuidado con los rangos ingresados. Estos deben corresponder a los cuadros 3,6 y 9 del pdf (Donativos - Ingresos - Gastos).

### Fuentes

Directorio SAT: [Link](https://www.sat.gob.mx/consultas/27717/conoce-el-directorio-de-donatarias-autorizadas)

Informe de Transparencia: [Link](https://eu2-por-pro-don-net-cons.azurewebsites.net/Consulta/Acceso?ReturnUrl=%2FConsulta%2FTransparencia)

Reporte de Donatarias Autorizadas: [Link](https://www.gob.mx/shcp/documentos/reporte-de-donatarias-autorizadas-2022#:~:text=El%20Reporte%20de%20Donatarias%20Autorizadas%202022%20se%20publica%20en%20la,como%20a%20la%20Comisi%C3%B3n%20de)

---

Para ver más archivos, consultar en el [Trello](https://trello.com/b/JI2jQO1e/repo-sat-rda).
