from __future__ import annotations

import html
import http.cookies
import secrets
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from string import Template
from urllib.parse import parse_qs, urlparse

import database

HOST = "127.0.0.1"
PORT = 8000
SESSIONS: dict[str, int] = {}
BASE_PLANTILLAS = Path(__file__).with_name("plantillas")


def obtener_analisis_imc(imc: float) -> dict[str, str]:
    if imc < 18.5:
        return {
            "category": "Bajo peso",
            "recommendation": "Aumenta tu ingesta calórica con alimentos nutritivos y equilibrados. Consulta a un nutricionista para un plan personalizado.",
            "exercise": "Incluye ejercicios de fuerza como levantamiento de pesas ligeras para ganar masa muscular, combinados con alimentación rica en proteínas.",
        }
    if imc < 25:
        return {
            "category": "Peso normal o saludable",
            "recommendation": "Mantén una dieta equilibrada con porciones moderadas y actividad física regular. Continúa con hábitos saludables.",
            "exercise": "Practica caminatas diarias, natación, yoga o cualquier actividad que disfrutes para mantener la forma.",
        }
    if imc < 30:
        return {
            "category": "Sobrepeso",
            "recommendation": "Reduce el consumo de calorías, aumenta la ingesta de verduras y frutas, y combina con ejercicio regular.",
            "exercise": "Camina al menos 45 minutos diarios, practica ciclismo o danza para quemar calorías extra.",
        }
    if imc < 35:
        return {
            "category": "Obesidad grado I",
            "recommendation": "Consulta a un médico para un plan de pérdida de peso. Adopta una dieta baja en calorías y ejercicio supervisado.",
            "exercise": "Ejercicios aeróbicos moderados como caminar rápido o nadar, bajo supervisión si es necesario.",
        }
    if imc < 40:
        return {
            "category": "Obesidad grado II",
            "recommendation": "Busca tratamiento médico integral, incluyendo dieta estricta y posible intervención médica.",
            "exercise": "Actividades de bajo impacto como nadar o usar máquina elíptica para evitar lesiones.",
        }
    return {
        "category": "Obesidad grado III (obesidad mórbida)",
        "recommendation": "Consulta inmediatamente a un especialista. Puede requerir cirugía bariátrica y seguimiento médico estricto.",
        "exercise": "Ejercicios adaptados y de bajo impacto bajo estricta supervisión médica.",
    }


def obtener_id_usuario_por_cookie(cabecera_cookie: str | None) -> int | None:
    if not cabecera_cookie:
        return None
    cookie = http.cookies.SimpleCookie()
    cookie.load(cabecera_cookie)
    cookie_sesion = cookie.get("session_id")
    if not cookie_sesion:
        return None
    return SESSIONS.get(cookie_sesion.value)


def crear_sesion(user_id: int) -> str:
    session_id = secrets.token_urlsafe(24)
    SESSIONS[session_id] = user_id
    return session_id


def destruir_sesion(session_id: str | None) -> None:
    if session_id and session_id in SESSIONS:
        del SESSIONS[session_id]


def texto_seguro(value: object) -> str:
    return html.escape("" if value is None else str(value))


def cargar_plantilla(nombre: str, **datos: object) -> str:
    ruta = BASE_PLANTILLAS / nombre
    contenido = ruta.read_text(encoding="utf-8")
    return Template(contenido).safe_substitute({k: str(v) for k, v in datos.items()})


def enlaces_navegacion(usuario: dict | None) -> str:
    if usuario:
        return """
            <a href="/">Inicio</a>
            <a href="/history">Conciencia histórica</a>
            <a href="/chemistry">Reacciones químicas</a>
            <a href="/bmi">IMC</a>
            <form method="post" action="/logout" style="display:inline;">
                <button type="submit" class="nav-button">Salir</button>
            </form>
        """
    return """
        <a href="/login">Iniciar sesión</a>
        <a href="/register">Registrarse</a>
    """


def renderizar_pagina(titulo: str, contenido: str, usuario: dict | None = None, mensaje: str = "", tipo_mensaje: str = "success") -> str:
    mensaje_html = ""
    if mensaje:
        mensaje_html = f'<div class="message {tipo_mensaje}">{texto_seguro(mensaje)}</div>'

    banner_usuario = ""
    if usuario:
        banner_usuario = f'<div class="user-banner">Sesión activa como <strong>{texto_seguro(usuario["username"])}</strong></div>'

    return cargar_plantilla(
        "base.html",
        titulo=texto_seguro(titulo),
        enlaces_nav=enlaces_navegacion(usuario),
        mensaje_html=mensaje_html,
        banner_usuario=banner_usuario,
        contenido=contenido,
    )


def renderizar_inicio_sesion(mensaje: str = "", tipo_mensaje: str = "error") -> str:
    contenido = cargar_plantilla("iniciar_sesion.html")
    return renderizar_pagina("Iniciar sesión", contenido, None, mensaje, tipo_mensaje)


def renderizar_registro(mensaje: str = "", tipo_mensaje: str = "error") -> str:
    contenido = cargar_plantilla("registro.html")
    return renderizar_pagina("Registro", contenido, None, mensaje, tipo_mensaje)


def renderizar_inicio(usuario: dict[str, object]) -> str:
    contenido = cargar_plantilla(
        "inicio.html",
        usuario=texto_seguro(usuario["username"]),
    )
    return renderizar_pagina("Inicio", contenido, usuario)


def renderizar_historia(usuario: dict[str, object] | None) -> str:
    contenido = cargar_plantilla("conciencia_historica.html")
    return renderizar_pagina("Conciencia histórica", contenido, usuario)


def renderizar_quimica(usuario: dict[str, object]) -> str:
    contenido = cargar_plantilla("reacciones_quimicas.html")
    return renderizar_pagina("Reacciones químicas", contenido, usuario)


def renderizar_imc(usuario: dict[str, object], mensaje: str = "", tipo_mensaje: str = "error", resultado_html: str = "") -> str:
    contenido = cargar_plantilla(
        "imc.html",
        resultado_html=resultado_html if resultado_html else "<p>Ingresa tus datos y presiona calcular.</p>",
    )
    return renderizar_pagina("IMC", contenido, usuario, mensaje, tipo_mensaje)


def renderizar_historial(usuario: dict[str, object]) -> str:
    filas = database.get_history(int(usuario["id"]))
    if not filas:
        contenido = cargar_plantilla("historial_vacio.html")
        return renderizar_pagina("Historial", contenido, usuario)

    filas_html = "".join(
        f"""
        <tr>
            <td>{texto_seguro(fila["date"])}</td>
            <td>{texto_seguro(fila["weight"])}</td>
            <td>{texto_seguro(fila["height"])}</td>
            <td>{texto_seguro(fila["imc"])}</td>
            <td>{texto_seguro(fila["category"])}</td>
        </tr>
        """
        for fila in filas
    )
    contenido = cargar_plantilla(
        "historial.html",
        filas_historial=filas_html,
    )
    return renderizar_pagina("Historial", contenido, usuario)


def renderizar_resultado_imc(imc: float, analisis: dict[str, str]) -> str:
    return cargar_plantilla(
        "resultado_imc.html",
        imc=f"{imc:.2f}",
        categoria=texto_seguro(analisis["category"]),
        recomendacion=texto_seguro(analisis["recommendation"]),
        ejercicios=texto_seguro(analisis["exercise"]),
    )


class ManejadorSolicitudes(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path
        usuario = self.usuario_actual()

        if path == "/":
            if usuario:
                self.responder_html(renderizar_inicio(usuario))
            else:
                self.redirigir("/login")
            return

        if path == "/login":
            if usuario:
                self.redirigir("/")
            else:
                self.responder_html(renderizar_inicio_sesion())
            return

        if path == "/register":
            if usuario:
                self.redirigir("/")
            else:
                self.responder_html(renderizar_registro())
            return

        if path == "/history":
            self.responder_html(renderizar_historia(usuario))
            return

        if path == "/chemistry":
            if not usuario:
                self.redirigir("/login")
            else:
                self.responder_html(renderizar_quimica(usuario))
            return

        if path == "/bmi":
            if not usuario:
                self.redirigir("/login")
            else:
                self.responder_html(renderizar_imc(usuario))
            return

        self.send_error(404, "Página no encontrada")

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path
        usuario = self.usuario_actual()
        formulario = self.leer_formulario()

        if path == "/login":
            username = formulario.get("username", [""])[0].strip()
            password = formulario.get("password", [""])[0]
            if not username or not password:
                self.responder_html(renderizar_inicio_sesion("Completa todos los campos"), status=400)
                return

            user_id = database.authenticate_user(username, password)
            if not user_id:
                self.responder_html(renderizar_inicio_sesion("Usuario o contraseña incorrectos"), status=401)
                return

            session_id = crear_sesion(user_id)
            self.responder_redireccion("/", extra_headers=[("Set-Cookie", f"session_id={session_id}; HttpOnly; Path=/; SameSite=Lax")])
            return

        if path == "/register":
            username = formulario.get("username", [""])[0].strip()
            email = formulario.get("email", [""])[0].strip()
            password = formulario.get("password", [""])[0]
            confirm = formulario.get("confirm", [""])[0]

            if not username or not email or not password or not confirm:
                self.responder_html(renderizar_registro("Completa todos los campos"), status=400)
                return

            if password != confirm:
                self.responder_html(renderizar_registro("Las contraseñas no coinciden"), status=400)
                return

            if not database.create_user(username, email, password):
                self.responder_html(renderizar_registro("El usuario o correo ya existe"), status=409)
                return

            self.responder_redireccion("/login", mensaje="Cuenta creada correctamente. Inicia sesión.")
            return

        if path == "/logout":
            cookie_header = self.headers.get("Cookie")
            session_id = None
            if cookie_header:
                cookie = http.cookies.SimpleCookie()
                cookie.load(cookie_header)
                session = cookie.get("session_id")
                if session:
                    session_id = session.value
            destruir_sesion(session_id)
            self.responder_redireccion("/login", extra_headers=[("Set-Cookie", "session_id=; Max-Age=0; Path=/; HttpOnly; SameSite=Lax")])
            return

        if path == "/bmi":
            if not usuario:
                self.redirigir("/login")
                return

            weight_raw = formulario.get("weight", [""])[0].strip().replace(",", ".")
            height_raw = formulario.get("height", [""])[0].strip().replace(",", ".")

            try:
                if not weight_raw or not height_raw:
                    self.responder_html(renderizar_imc(usuario, "Por favor, completa todos los campos"), status=400)
                    return

                weight = float(weight_raw)
                height = float(height_raw)

                if weight <= 0 or height <= 0:
                    self.responder_html(renderizar_imc(usuario, "El peso y la estatura deben ser mayores a 0"), status=400)
                    return

                imc = weight / (height ** 2)
                imc_redondeado = round(imc, 2)
                analisis = obtener_analisis_imc(imc)
                database.save_bmi(int(usuario["id"]), weight, height, imc_redondeado, analisis["category"])
                resultado_html = renderizar_resultado_imc(imc_redondeado, analisis)
                self.responder_html(renderizar_imc(usuario, "IMC calculado y guardado correctamente", "success", resultado_html))
                return

            except ValueError:
                self.responder_html(renderizar_imc(usuario, "Por favor, ingresa valores numéricos válidos"), status=400)
                return

        self.send_error(404, "Ruta no encontrada")

    def usuario_actual(self) -> dict[str, object] | None:
        user_id = obtener_id_usuario_por_cookie(self.headers.get("Cookie"))
        if user_id is None:
            return None
        usuario = database.get_user(user_id)
        return usuario if usuario else None

    def leer_formulario(self) -> dict[str, list[str]]:
        content_length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(content_length).decode("utf-8")
        return parse_qs(body)

    def responder_html(self, html_text: str, status: int = 200) -> None:
        encoded = html_text.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def responder_redireccion(self, location: str, mensaje: str = "", extra_headers: list[tuple[str, str]] | None = None) -> None:
        self.send_response(303)
        self.send_header("Location", location)
        if extra_headers:
            for key, value in extra_headers:
                self.send_header(key, value)
        self.end_headers()

    def redirigir(self, location: str) -> None:
        self.send_response(302)
        self.send_header("Location", location)
        self.end_headers()

    def log_message(self, format: str, *args: object) -> None:
        return


def ejecutar() -> None:
    database.init_db()
    server = ThreadingHTTPServer((HOST, PORT), ManejadorSolicitudes)
    print(f"Servidor iniciado en http://{HOST}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido")
    finally:
        server.server_close()


if __name__ == "__main__":
    ejecutar()
