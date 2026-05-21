# Proyecto PAEC: Vida Saludable

## Información del Proyecto

- **Grupo**: [Especificar grupo]
- **Especialidad**: [Especificar especialidad]
- **Nombre del Proyecto**: Proyecto PAEC: Vida Saludable
- **Integrantes del Equipo**:
  - Mariela Leyva Vázquez (Desarrollador principal, Diseñador de interfaz, Investigador)
- **Roles Asignados**:
  - Mariela Leyva Vázquez: Desarrollo del código en Python con Flet, diseño de la interfaz, integración de base de datos, investigación de contenido.

## Objetivo

Desarrollar una interfaz gráfica en lenguaje Python utilizando el Framework Flet, conectando con una base de datos SQLite, que muestre información sobre cambios necesarios para una vida saludable en hábitos alimenticios, actividad física y descanso, así como su impacto en el desempeño académico. La aplicación incluye contenido de las asignaturas de conciencia histórica y reacciones químicas, y una calculadora de Índice de Masa Corporal (IMC) con recomendaciones personalizadas.

## Funcionamiento

La aplicación presenta información educativa sobre vida saludable organizada en secciones temáticas. Los usuarios pueden navegar por el contenido y acceder a una calculadora de IMC que solicita peso y estatura, calcula el IMC, determina la categoría de peso y proporciona recomendaciones específicas de alimentación, beneficios de vida saludable y ejercicios recomendados basados en el resultado.

Los datos de los cálculos de IMC se almacenan en una base de datos SQLite para registro histórico.

## Impacto Social

Este proyecto promueve la conciencia sobre la importancia de la salud en la vida diaria, especialmente entre estudiantes, conectando hábitos saludables con el rendimiento académico. Al integrar conocimientos de historia y química, fomenta una comprensión interdisciplinaria. La calculadora de IMC con recomendaciones personalizadas puede motivar cambios positivos en el estilo de vida, contribuyendo a una sociedad más saludable y productiva.

## Reflexión como Alumnos

Como estudiantes, este proyecto nos ha permitido aplicar conocimientos técnicos en programación y bases de datos para abordar un tema relevante como la salud. Hemos aprendido la importancia de integrar diferentes disciplinas (historia, química, salud) en soluciones tecnológicas. Desarrollar esta aplicación nos ha hecho reflexionar sobre nuestros propios hábitos y la responsabilidad de promover información precisa y útil. Creemos que proyectos como este no solo cumplen requisitos académicos, sino que pueden tener un impacto real en la comunidad estudiantil al fomentar estilos de vida saludables desde temprana edad.

## Instalación y Ejecución

1. Asegúrate de tener `uv` instalado.
2. Clona o descarga el proyecto.
3. Ejecuta `uv sync` para instalar dependencias.
4. Ejecuta `uv run main.py` para iniciar la aplicación.


## Tecnologías Utilizadas

- **Python**: Lenguaje de programación principal del proyecto.
- **SQLite**: Base de datos ligera y embebida para almacenar usuarios e historiales de IMC.
- **uv**: Gestor de entornos virtuales y dependencias para Python.

## Explicación de Librerías y Funciones

### Librerías utilizadas

- `html`, `http.cookies`, `secrets`, `http.server`, `urllib.parse`: Módulos estándar de Python para manejo de HTML, cookies, generación de tokens seguros, servidor HTTP y parseo de URLs y formularios.
- `hashlib`: Para el hash seguro de contraseñas.
- `os`, `pathlib.Path`: Manejo de rutas y archivos en el sistema operativo.
- `sqlite3`: Conexión y operaciones con la base de datos SQLite.
- `contextlib.closing`: Asegura el cierre correcto de conexiones a la base de datos.
- `datetime`: Para registrar fechas y horas de creación y registros.
- `typing`: Tipado estático y anotaciones para mayor claridad y robustez.

### Funciones y clases principales

#### Archivo `database.py`

- **_connect()**: Abre una conexión a la base de datos SQLite y configura el formato de filas como diccionario.
- **init_db()**: Inicializa la base de datos y crea las tablas necesarias (`users` y `bmi_history`) si no existen.
- **_hash_password(password)**: Genera un hash SHA-256 de la contraseña para almacenarla de forma segura.
- **create_user(username, email, password)**: Crea un nuevo usuario en la base de datos, almacenando el hash de la contraseña y la fecha de creación.
- **authenticate_user(username, password)**: Verifica si el usuario y contraseña coinciden con los almacenados en la base de datos y retorna el ID del usuario si es correcto.
- **get_user(user_id)**: Recupera la información de un usuario por su ID.
- **save_bmi(user_id, weight, height, imc, category)**: Guarda un registro de IMC calculado para un usuario, incluyendo peso, estatura, IMC, categoría y fecha.
- **get_history(user_id, limit)**: Obtiene el historial de cálculos de IMC de un usuario, ordenados por fecha.

#### Archivo `main.py`

- **get_bmi_analysis(imc)**: Analiza el valor de IMC y retorna la categoría, recomendaciones y ejercicios sugeridos.
- **get_user_id_from_cookie(cookie_header)**: Extrae el ID de usuario de la cookie de sesión.
- **create_session(user_id)**: Crea una nueva sesión para el usuario y genera un identificador seguro.
- **destroy_session(session_id)**: Elimina la sesión del usuario al cerrar sesión.
- **safe_text(value)**: Escapa caracteres especiales para evitar inyección de HTML.
- **page_shell(title, body, ...)**: Genera la estructura HTML base de todas las páginas, incluyendo navegación y mensajes.
- **render_login, render_register, render_home, render_history, render_chemistry, render_bmi, render_history_page, render_bmi_result**: Funciones que generan el HTML para cada sección/página de la aplicación.
- **RequestHandler (clase)**: Hereda de `BaseHTTPRequestHandler` y gestiona todas las rutas HTTP (GET y POST), el flujo de autenticación, registro, cálculo y guardado de IMC, y navegación entre páginas.
- **run()**: Inicializa la base de datos y arranca el servidor web en el host y puerto definidos.

Cada función está diseñada para separar responsabilidades: la lógica de negocio y acceso a datos está en `database.py`, mientras que la presentación y el manejo de rutas HTTP están en `main.py`.