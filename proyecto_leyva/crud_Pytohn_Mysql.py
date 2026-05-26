# =========================================================
# PROYECTO CRUD CON FLET + MYSQL
# =========================================================
#
# Este proyecto permite:
# - Guardar registros
# - Consultar registros
# - Actualizar registros
# - Eliminar registros
#
# Tecnologías utilizadas:
# - Python
# - Flet
# - MySQL


# IMPORTACIÓN DE LIBRERÍAS
# =========================================================

# Librería Flet para crear interfaces gráficas
import flet as ft

# Librería para conectar Python con MySQL
import mysql.connector

# Librería para funciones del sistema
import sys


# FUNCIÓN PRINCIPAL
# *******************************************

# page representa la ventana principal de la app
def main(page: ft.Page):

    # *** CONFIGURACIÓN DE LA VENTANA  ****

    # Título de la ventana
    page.title = "CRUD Usuarios MySQL"

    # Color de fondo de la ventana
    page.bgcolor = ft.Colors.LIME_100

    # Centrar contenido horizontalmente
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Centrar contenido verticalmente
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # CONEXIÓN A MYSQL
    # *******************************************

    try:

        # Conexión inicial al servidor MySQL
        # SIN indicar todavía la base de datos
        conn = mysql.connector.connect(

            host="localhost",   # Servidor Local MySQL
            user="root",        # Usuario MySQL
            password="admin"    # Contraseña MySQL
        )

        # cursor permite enviar instrucciones SQL
        cursor = conn.cursor()

        # Crear la base de datos si no existe
        cursor.execute(
            "CREATE DATABASE IF NOT EXISTS crud_flet"
        )

        # Seleccionar la base de datos
        cursor.execute(
            "USE crud_flet"
        )

        # Crear tabla si no existe
        cursor.execute("""

            CREATE TABLE IF NOT EXISTS usuarios2 (

                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100),
                correo VARCHAR(100),
                edad INT

            )

        """)

        # Guardar cambios en MySQL
        conn.commit()

        # Mensaje de conexión exitosa
        print("✅ Conexión exitosa a MySQL")

    # Captura errores de conexión
    except Exception as e:

        print("❌ Error de conexión")
        print(e)

        # Finaliza la función
        return

    # CONSTRUCCION DE LOS CAMPOS DE TEXTO
    # *******************************************

    # Campo ID
    id_usuario = ft.TextField(

        label="ID",
        width=250,

        # Solo lectura
        read_only=True,

        label_style=ft.TextStyle(color=ft.Colors.GREY_400)
    )

    # Campo Nombre
    nombre = ft.TextField(
        label="Nombre",
        # Cursor automático
        autofocus=True,
        width=250,
        label_style=ft.TextStyle(color=ft.Colors.GREY_400)
    )

    # Campo Correo
    correo = ft.TextField(label="Correo",width=250,label_style=ft.TextStyle(color=ft.Colors.GREY_400))

    # Campo Edad
    edad = ft.TextField(label="Edad", width=250,  label_style=ft.TextStyle(color=ft.Colors.GREY_400))

    # Texto para mensajes
    resultado = ft.Text()

    # CONTENEDOR PARA REGISTROS
    # *******************************************

    lista_datos = ft.Container(

        # Dentro habrá una columna
        content=ft.Column(

            # Activar scroll automático
            scroll=ft.ScrollMode.AUTO
        ),

        # Alto
        height=180,

        # Ancho
        width=350,

        # Fondo blanco
        bgcolor=ft.Colors.WHITE,

        # Bordes redondeados
        border_radius=10,

        # Espacio interno
        padding=5
    )

    # FUNCIÓN LIMPIAR
    # *******************************************

    def limpiar(e):

        # Limpiar campos
        id_usuario.value = ""
        nombre.value = ""
        correo.value = ""
        edad.value = ""

        # Limpiar mensajes
        resultado.value = ""

        # Colocar cursor en nombre
        nombre.focus()

        # Actualizar ventana
        page.update()


    # FUNCIÓN CONSULTAR
    # *******************************************

    def consultar(e):

        # Limpiar lista visual
        lista_datos.content.controls.clear()

        # Ejecutar consulta SQL
        cursor.execute(

            "SELECT id, nombre, correo, edad FROM usuarios2"
        )

        # Obtener registros
        registros = cursor.fetchall()

        # Recorrer registros
        for id_, nom, cor, ed in registros:

            # Función para seleccionar registros
            def seleccionar(
                e,
                id_=id_,
                nom=nom,
                cor=cor,
                ed=ed
            ):

                # Cargar datos en formulario
                id_usuario.value = str(id_)
                nombre.value = nom
                correo.value = cor
                edad.value = str(ed)

                # Mensaje
                resultado.value = f"Registro seleccionado ID: {id_}"
                resultado.color = "blue"

                page.update()

            # Agregar registro visual
            lista_datos.content.controls.append(

                ft.ListTile(

                    title=ft.Text(
                        f"{nom} ({ed})"
                    ),

                    subtitle=ft.Text(cor),

                    on_click=seleccionar
                )
            )

        # Actualizar interfaz
        page.update()

    # FUNCIÓN GUARDAR
    # *******************************************

    def guardar(e):

        # Validar campos vacíos
        if not nombre.value or not correo.value or not edad.value:

            resultado.value = "⚠️ Campos obligatorios"
            resultado.color = "red"

            page.update()
            return

        # Validar edad numérica
        if not edad.value.isdigit():

            resultado.value = "⚠️ Edad inválida"
            resultado.color = "red"

            edad.value = ""
            edad.focus()

            page.update()
            return

        # Consulta INSERT
        sql = """

            INSERT INTO usuarios2
            (nombre, correo, edad)

            VALUES (%s, %s, %s)

        """

        # Valores a insertar
        valores = (

            nombre.value,
            correo.value,
            edad.value
        )

        # Ejecutar consulta
        cursor.execute(sql, valores)

        # Guardar cambios
        conn.commit()

        # Mensaje éxito
        resultado.value = "✅ Registro guardado"
        resultado.color = "green"

        # Limpiar formulario
        limpiar(None)

        # Actualizar lista
        consultar(None)

        page.update()

    # FUNCIÓN ACTUALIZAR
    # *******************************************

    def actualizar(e):

        # Validar selección
        if not id_usuario.value:

            resultado.value = "⚠️ Selecciona un registro"
            resultado.color = "red"

            page.update()
            return

        # Consulta UPDATE
        sql = """

            UPDATE usuarios2

            SET
                nombre=%s,
                correo=%s,
                edad=%s

            WHERE id=%s

        """
       
        # Valores actualización
        valores = (

            nombre.value,
            correo.value,
            edad.value,
            id_usuario.value
        )

        # Ejecutar actualización
        cursor.execute(sql, valores)

        # Guardar cambios
        conn.commit()

        # Mensaje
        resultado.value = "✏️ Registro actualizado"
        resultado.color = "blue"

        # Actualizar lista
        consultar(None)

        page.update()

    # FUNCIÓN ELIMINAR
    # *******************************************

    def eliminar(e):

        # Validar selección
        if not id_usuario.value:

            resultado.value = "⚠️ Selecciona un registro"
            resultado.color = "red"

            page.update()
            return

        # Consulta DELETE
        sql = """

            DELETE FROM usuarios2
            WHERE id=%s

        """

        # Valor ID
        valores = (id_usuario.value,)

        # Ejecutar eliminación
        cursor.execute(sql, valores)

        # Guardar cambios
        conn.commit()

        # Verificar eliminación
        if cursor.rowcount > 0:

            resultado.value = "🗑️ Registro eliminado"
            resultado.color = "red"

            limpiar(None)
            consultar(None)

        else:

            resultado.value = "⚠️ Registro no encontrado"
            resultado.color = "orange"

        page.update()

    # FUNCIÓN SALIR
    # *******************************************

    def salir(e):

        # Cerrar cursor
        cursor.close()

        # Cerrar conexión MySQL
        conn.close()

        # Cerrar aplicación
        sys.exit()


    # CONTRUCCION DE BOTONES
    # *******************************************

    btn_guardar = ft.ElevatedButton(

        "Guardar",
        on_click=guardar,
        width=100
    )

    btn_consultar = ft.ElevatedButton(

        "Consultar",
        on_click=consultar,
        width=110
    )

    btn_actualizar = ft.ElevatedButton(

        "Actualizar",
        on_click=actualizar,
        width=115
    )

    btn_eliminar = ft.ElevatedButton(

        "Eliminar",
        on_click=eliminar,
        width=105
    )

    btn_limpiar = ft.ElevatedButton(

        "Limpiar",
        on_click=limpiar,
        width=100
    )

    btn_salir = ft.ElevatedButton(

        "Salir",
        on_click=salir,
        width=100,

        bgcolor="red",
        color="white"
    )

    # FILAS PARA LA UBICACION DEL MENU DE BOTONES
    # *******************************************

    fila1 = ft.Row(
        [
            btn_guardar,
            btn_consultar,
            btn_actualizar
        ],
        alignment=ft.MainAxisAlignment.CENTER #Centrado de Botones de la Fila1
    )
    fila2 = ft.Row(
        [
            btn_eliminar,
            btn_limpiar,
            btn_salir
        ],
        alignment=ft.MainAxisAlignment.CENTER # Centrado de Botones de la fila2
    )

    # INTERFAZ PRINCIPAL (FORMULARIO)
    # *******************************************

    page.add(
        ft.Container(
            content=ft.Column(
                [
                    # Título del Formulario
                    ft.Text(
                        "CRUD USUARIOS MYSQL",
                        size=22,
                        weight="bold",
                        color="black"
                    ),

                    # Campos a capturar
                    id_usuario,
                    nombre,
                    correo,
                    edad,

                    # Botones de opciones
                    fila1,
                    fila2,

                    # Mensajes de resultados
                    resultado,

                    # Lista con registros
                    lista_datos
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10
            ),
            width=420,
            padding=20,
            bgcolor=ft.Colors.GREY_100,
            border_radius=15
        )
    )

    # CONSULTAR AL INICIAR
    # *******************************************

    consultar(None)


# EJECUTAR APLICACIÓN
# *******************************************

ft.run(main)