from __future__ import annotations

import html
import http.cookies
import secrets
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

import database

HOST = "127.0.0.1"
PORT = 8000

SESSIONS: dict[str, int] = {}


def get_bmi_analysis(imc: float) -> dict[str, str]:
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


def get_user_id_from_cookie(cookie_header: str | None) -> int | None:
    if not cookie_header:
        return None
    cookie = http.cookies.SimpleCookie()
    cookie.load(cookie_header)
    session_cookie = cookie.get("session_id")
    if not session_cookie:
        return None
    session_id = session_cookie.value
    return SESSIONS.get(session_id)


def create_session(user_id: int) -> str:
    session_id = secrets.token_urlsafe(24)
    SESSIONS[session_id] = user_id
    return session_id


def destroy_session(session_id: str | None) -> None:
    if session_id and session_id in SESSIONS:
        del SESSIONS[session_id]


def safe_text(value: object) -> str:
    return html.escape("" if value is None else str(value))


def page_shell(title: str, body: str, user: dict | None = None, message: str = "", message_type: str = "success") -> str:
    nav_links = ""
    if user:
        nav_links = f"""
            <a href="/">Inicio</a>
            <a href="/history">Historial</a>
            <a href="/chemistry">Reacciones químicas</a>
            <a href="/bmi">IMC</a>
            <form method="post" action="/logout" style="display:inline;">
                <button type="submit" class="nav-button">Salir</button>
            </form>
        """
    else:
        nav_links = """
            <a href="/login">Iniciar sesión</a>
            <a href="/register">Registrarse</a>
        """

    message_html = ""
    if message:
        message_html = f'<div class="message {message_type}">{safe_text(message)}</div>'

    user_banner = ""
    if user:
        user_banner = f'<div class="user-banner">Sesión activa como <strong>{safe_text(user["username"])}</strong></div>'

    return f"""<!doctype html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{safe_text(title)}</title>
    <style>
        :root {{
            --bg: #050505;
            --panel: #0f0f0f;
            --panel-2: #151515;
            --green: #39d353;
            --green-dark: #1f8f36;
            --green-soft: #b7f7c1;
            --text: #f3f3f3;
            --muted: #b8b8b8;
            --border: #2a2a2a;
            --danger: #ff5c5c;
            --shadow: 0 12px 0 #000;
        }}

        * {{
            box-sizing: border-box;
        }}

        body {{
            margin: 0;
            font-family: Arial, Helvetica, sans-serif;
            background:
                radial-gradient(circle at top, rgba(57, 211, 83, 0.16), transparent 30%),
                linear-gradient(180deg, #0b0b0b, #050505);
            color: var(--text);
            min-height: 100vh;
        }}

        a {{
            color: var(--green-soft);
            text-decoration: none;
        }}

        a:hover {{
            text-decoration: underline;
        }}

        .topbar {{
            position: sticky;
            top: 0;
            z-index: 10;
            background: rgba(5, 5, 5, 0.95);
            border-bottom: 3px solid var(--green-dark);
            backdrop-filter: blur(6px);
        }}

        .topbar-inner {{
            max-width: 1100px;
            margin: 0 auto;
            padding: 16px 20px;
            display: flex;
            gap: 14px;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
        }}

        .brand {{
            display: flex;
            align-items: center;
            gap: 12px;
            font-weight: 900;
            letter-spacing: 0.3px;
        }}

        .brand-badge {{
            width: 44px;
            height: 44px;
            border-radius: 12px;
            background: var(--green);
            border: 3px solid #000;
            box-shadow: var(--shadow);
            display: grid;
            place-items: center;
            color: #000;
            font-size: 24px;
        }}

        .nav {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            align-items: center;
        }}

        .nav a,
        .nav button,
        .button {{
            appearance: none;
            border: 3px solid #000;
            background: var(--green);
            color: #000;
            font-weight: 800;
            border-radius: 14px;
            padding: 12px 16px;
            box-shadow: var(--shadow);
            cursor: pointer;
            transition: transform 0.1s ease, filter 0.1s ease;
        }}

        .nav a:hover,
        .nav button:hover,
        .button:hover {{
            transform: translateY(2px);
            filter: brightness(1.05);
            text-decoration: none;
        }}

        .nav-button {{
            font: inherit;
        }}

        .container {{
            max-width: 1100px;
            margin: 0 auto;
            padding: 28px 20px 50px;
        }}

        .hero {{
            background: linear-gradient(180deg, #101010, #080808);
            border: 3px solid var(--green-dark);
            border-radius: 28px;
            padding: 28px;
            box-shadow: var(--shadow);
            margin-bottom: 22px;
        }}

        .hero h1 {{
            margin: 0 0 8px;
            font-size: clamp(2rem, 5vw, 3.4rem);
            line-height: 1.05;
        }}

        .hero p {{
            margin: 0;
            color: var(--muted);
            line-height: 1.6;
            max-width: 72ch;
        }}

        .grid {{
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 18px;
        }}

        .card {{
            background: var(--panel);
            border: 3px solid var(--green-dark);
            border-radius: 22px;
            padding: 20px;
            box-shadow: var(--shadow);
        }}

        .card h2,
        .card h3 {{
            margin-top: 0;
        }}

        .card p {{
            color: var(--muted);
            line-height: 1.6;
        }}

        .split {{
            display: grid;
            grid-template-columns: minmax(0, 1.05fr) minmax(280px, 0.95fr);
            gap: 18px;
        }}

        .form {{
            display: grid;
            gap: 14px;
        }}

        label {{
            display: grid;
            gap: 8px;
            font-weight: 700;
            color: var(--green-soft);
        }}

        input {{
            width: 100%;
            padding: 14px 15px;
            border-radius: 14px;
            border: 3px solid #000;
            background: #121212;
            color: var(--text);
            outline: none;
            box-shadow: inset 0 0 0 2px var(--border);
        }}

        input:focus {{
            border-color: var(--green);
            box-shadow: inset 0 0 0 2px var(--green-dark), 0 0 0 2px rgba(57, 211, 83, 0.18);
        }}

        .actions {{
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
            align-items: center;
        }}

        .message {{
            border: 3px solid #000;
            border-radius: 16px;
            padding: 14px 16px;
            margin: 0 0 18px;
            box-shadow: var(--shadow);
            font-weight: 700;
        }}

        .message.success {{
            background: #10341a;
            color: #d9ffe0;
            border-color: var(--green-dark);
        }}

        .message.error {{
            background: #3b1010;
            color: #ffd8d8;
            border-color: #8f1f1f;
        }}

        .user-banner {{
            margin-bottom: 18px;
            background: #121212;
            border-left: 6px solid var(--green);
            padding: 12px 14px;
            border-radius: 14px;
            color: var(--muted);
        }}

        .list {{
            display: grid;
            gap: 14px;
        }}

        .mini {{
            background: var(--panel-2);
            border: 2px solid var(--border);
            border-radius: 18px;
            padding: 16px;
        }}

        .mini strong {{
            color: var(--green-soft);
        }}

        .table-wrap {{
            overflow-x: auto;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            min-width: 760px;
        }}

        th, td {{
            border-bottom: 1px solid var(--border);
            padding: 12px 10px;
            text-align: left;
            vertical-align: top;
        }}

        th {{
            color: var(--green-soft);
            background: #121212;
        }}

        footer {{
            margin-top: 26px;
            padding-top: 18px;
            border-top: 1px solid var(--border);
            color: var(--muted);
            text-align: center;
        }}

        @media (max-width: 900px) {{
            .grid,
            .split {{
                grid-template-columns: 1fr;
            }}

            .topbar-inner {{
                justify-content: center;
            }}

            .brand {{
                width: 100%;
                justify-content: center;
            }}

            .nav {{
                justify-content: center;
            }}
        }}
    </style>
</head>
<body>
    <header class="topbar">
        <div class="topbar-inner">
            <div class="brand">
                <div class="brand-badge">♥</div>
                <div>
                    <div style="font-size: 1.1rem;">Proyecto PAEC</div>
                    <div style="font-size: 0.9rem; color: var(--muted);">Vida saludable</div>
                </div>
            </div>
            <nav class="nav">
                {nav_links}
            </nav>
        </div>
    </header>

    <main class="container">
        {message_html}
        {user_banner}
        {body}
        <footer>© 2024 Proyecto PAEC - Vida Saludable</footer>
    </main>
</body>
</html>"""


def render_login(message: str = "", message_type: str = "error") -> str:
    body = """
        <section class="hero">
            <h1>Iniciar sesión</h1>
            <p>Accede para consultar contenido educativo, guardar tu IMC y revisar tu historial.</p>
        </section>

        <section class="split">
            <div class="card">
                <h2>Bienvenido</h2>
                <p>Esta versión funciona con Python y HTML, sin Flet. El diseño usa negro y verde como colores principales.</p>
                <div class="list">
                    <div class="mini"><strong>Alimentación</strong><br>Hábitos para rendir mejor en la escuela.</div>
                    <div class="mini"><strong>Actividad física</strong><br>Movimiento diario y bienestar general.</div>
                    <div class="mini"><strong>Descanso</strong><br>Sueño y recuperación para aprender mejor.</div>
                </div>
            </div>

            <div class="card">
                <h2>Ingresar</h2>
                <form class="form" method="post" action="/login">
                    <label>Usuario
                        <input type="text" name="username" autocomplete="username" required>
                    </label>
                    <label>Contraseña
                        <input type="password" name="password" autocomplete="current-password" required>
                    </label>
                    <div class="actions">
                        <button class="button" type="submit">Entrar</button>
                        <a class="button" href="/register">Crear cuenta</a>
                    </div>
                </form>
            </div>
        </section>
    """
    return page_shell("Iniciar sesión", body, None, message, message_type)


def render_register(message: str = "", message_type: str = "error") -> str:
    body = """
        <section class="hero">
            <h1>Crear cuenta</h1>
            <p>Regístrate para guardar tu información y ver el historial de IMC.</p>
        </section>

        <section class="card">
            <form class="form" method="post" action="/register">
                <label>Usuario
                    <input type="text" name="username" autocomplete="username" required>
                </label>
                <label>Correo
                    <input type="email" name="email" autocomplete="email" required>
                </label>
                <label>Contraseña
                    <input type="password" name="password" autocomplete="new-password" required>
                </label>
                <label>Confirmar contraseña
                    <input type="password" name="confirm" autocomplete="new-password" required>
                </label>
                <div class="actions">
                    <button class="button" type="submit">Registrarse</button>
                    <a class="button" href="/login">Ya tengo cuenta</a>
                </div>
            </form>
        </section>
    """
    return page_shell("Registro", body, None, message, message_type)


def render_home(user: dict[str, object]) -> str:
    body = f"""
        <section class="hero">
            <h1>Bienvenido, {safe_text(user["username"])}</h1>
            <p>Energía y concentración para tu vida escolar. Aquí encuentras contenido sobre salud, historia, química e IMC.</p>
        </section>

        <section class="grid">
            <article class="card">
                <h2>Alimentación</h2>
                <p>Frutas, verduras y proteína para rendir mejor.</p>
            </article>
            <article class="card">
                <h2>Actividad</h2>
                <p>Ejercicio diario para más energía y memoria.</p>
            </article>
            <article class="card">
                <h2>Descanso</h2>
                <p>Dormir bien ayuda a tu salud y rendimiento.</p>
            </article>
        </section>

        <section style="margin-top: 18px;" class="grid">
            <article class="card">
                <h3>Conciencia histórica</h3>
                <p>Comprender la historia nos permite valorar cómo las sociedades han evolucionado hacia estilos de vida más saludables.</p>
                <a class="button" href="/history">Ver sección</a>
            </article>
            <article class="card">
                <h3>Reacciones químicas</h3>
                <p>El metabolismo y la producción de energía dependen de una alimentación adecuada y descanso suficiente.</p>
                <a class="button" href="/chemistry">Ver sección</a>
            </article>
            <article class="card">
                <h3>Calculadora IMC</h3>
                <p>Calcula tu índice de masa corporal y recibe recomendaciones personalizadas.</p>
                <a class="button" href="/bmi">Calcular IMC</a>
            </article>
        </section>
    """
    return page_shell("Inicio", body, user)


def render_history(user: dict[str, object]) -> str:
    body = """
        <section class="hero">
            <h1>Conciencia histórica</h1>
            <p>Comprender la historia nos permite valorar cómo las sociedades han evolucionado hacia estilos de vida más saludables, reconociendo la salud como un derecho fundamental adquirido a través del tiempo.</p>
        </section>

        <section class="card">
            <p>La salud ha sido una preocupación constante en el desarrollo humano. Con el paso del tiempo, la educación, la higiene, la nutrición y la prevención de enfermedades se han convertido en pilares de una vida mejor.</p>
            <div class="actions">
                <a class="button" href="/">Volver al inicio</a>
            </div>
        </section>
    """
    return page_shell("Conciencia histórica", body, user)


def render_chemistry(user: dict[str, object]) -> str:
    body = """
        <section class="hero">
            <h1>Reacciones químicas</h1>
            <p>Las reacciones químicas en el cuerpo, como el metabolismo de nutrientes y la producción de energía, requieren una alimentación adecuada y descanso para funcionar óptimamente.</p>
        </section>

        <section class="card">
            <p>Los carbohidratos, las proteínas y las grasas participan en procesos metabólicos que permiten obtener energía. Dormir bien y comer de forma equilibrada favorece estos procesos y mejora la salud general.</p>
            <div class="actions">
                <a class="button" href="/">Volver al inicio</a>
            </div>
        </section>
    """
    return page_shell("Reacciones químicas", body, user)


def render_bmi(user: dict[str, object], message: str = "", message_type: str = "error", result_html: str = "") -> str:
    body = f"""
        <section class="hero">
            <h1>Calculadora de IMC</h1>
            <p>Ingresa tu peso y estatura para calcular tu índice de masa corporal y recibir recomendaciones.</p>
        </section>

        <section class="split">
            <div class="card">
                <h2>Datos</h2>
                <form class="form" method="post" action="/bmi">
                    <label>Peso (kg)
                        <input type="text" name="weight" inputmode="decimal" placeholder="Ej. 62.5" required>
                    </label>
                    <label>Estatura (m)
                        <input type="text" name="height" inputmode="decimal" placeholder="Ej. 1.68" required>
                    </label>
                    <div class="actions">
                        <button class="button" type="submit">Calcular IMC</button>
                        <a class="button" href="/">Volver al inicio</a>
                    </div>
                </form>
            </div>

            <div class="card">
                <h2>Resultado</h2>
                {result_html if result_html else "<p>Ingresa tus datos y presiona calcular.</p>"}
            </div>
        </section>
    """
    return page_shell("IMC", body, user, message, message_type)


def render_history_page(user: dict[str, object]) -> str:
    rows = database.get_history(int(user["id"]))
    if not rows:
        body = """
            <section class="hero">
                <h1>Historial de IMC</h1>
                <p>Aún no has calculado tu IMC.</p>
            </section>
            <section class="card">
                <p>Cuando calcules tu IMC, aquí aparecerán tus registros.</p>
                <div class="actions">
                    <a class="button" href="/bmi">Ir a la calculadora</a>
                </div>
            </section>
        """
        return page_shell("Historial", body, user)

    table_rows = "".join(
        f"""
        <tr>
            <td>{safe_text(row["date"])}</td>
            <td>{safe_text(row["weight"])}</td>
            <td>{safe_text(row["height"])}</td>
            <td>{safe_text(row["imc"])}</td>
            <td>{safe_text(row["category"])}</td>
        </tr>
        """
        for row in rows
    )

    body = f"""
        <section class="hero">
            <h1>Historial de IMC</h1>
            <p>Registros guardados de tus cálculos recientes.</p>
        </section>

        <section class="card table-wrap">
            <table>
                <thead>
                    <tr>
                        <th>Fecha</th>
                        <th>Peso (kg)</th>
                        <th>Estatura (m)</th>
                        <th>IMC</th>
                        <th>Categoría</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows}
                </tbody>
            </table>
        </section>
    """
    return page_shell("Historial", body, user)


def render_bmi_result(imc: float, analysis: dict[str, str]) -> str:
    return f"""
        <div class="list">
            <div class="mini"><strong>IMC calculado</strong><br>{imc:.2f}</div>
            <div class="mini"><strong>Categoría</strong><br>{safe_text(analysis["category"])}</div>
            <div class="mini"><strong>Recomendaciones</strong><br>{safe_text(analysis["recommendation"])}</div>
            <div class="mini"><strong>Ejercicios recomendados</strong><br>{safe_text(analysis["exercise"])}</div>
            <div class="mini"><strong>Beneficios de una vida saludable</strong><br>Mejor salud cardiovascular, más energía, menos estrés y mejor concentración.</div>
            <div class="mini"><strong>Nota</strong><br>El IMC no siempre refleja la composición corporal exacta, por ejemplo en atletas con mucha masa muscular.</div>
        </div>
    """


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path
        user = self.current_user()

        if path == "/":
            if user:
                self.respond_html(render_home(user))
            else:
                self.redirect("/login")
            return

        if path == "/login":
            if user:
                self.redirect("/")
            else:
                self.respond_html(render_login())
            return

        if path == "/register":
            if user:
                self.redirect("/")
            else:
                self.respond_html(render_register())
            return

        if path == "/history":
            if not user:
                self.redirect("/login")
            else:
                self.respond_html(render_history_page(user))
            return

        if path == "/chemistry":
            if not user:
                self.redirect("/login")
            else:
                self.respond_html(render_chemistry(user))
            return

        if path == "/bmi":
            if not user:
                self.redirect("/login")
            else:
                self.respond_html(render_bmi(user))
            return

        self.send_error(404, "Página no encontrada")

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path
        user = self.current_user()
        form = self.read_form()

        if path == "/login":
            username = form.get("username", [""])[0].strip()
            password = form.get("password", [""])[0]
            if not username or not password:
                self.respond_html(render_login("Completa todos los campos"), status=400)
                return

            user_id = database.authenticate_user(username, password)
            if not user_id:
                self.respond_html(render_login("Usuario o contraseña incorrectos"), status=401)
                return

            session_id = create_session(user_id)
            self.respond_redirect("/", extra_headers=[("Set-Cookie", f"session_id={session_id}; HttpOnly; Path=/; SameSite=Lax")])
            return

        if path == "/register":
            username = form.get("username", [""])[0].strip()
            email = form.get("email", [""])[0].strip()
            password = form.get("password", [""])[0]
            confirm = form.get("confirm", [""])[0]

            if not username or not email or not password or not confirm:
                self.respond_html(render_register("Completa todos los campos"), status=400)
                return

            if password != confirm:
                self.respond_html(render_register("Las contraseñas no coinciden"), status=400)
                return

            if not database.create_user(username, email, password):
                self.respond_html(render_register("El usuario o correo ya existe"), status=409)
                return

            self.respond_redirect("/login", message="Cuenta creada correctamente. Inicia sesión.")
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
            destroy_session(session_id)
            self.respond_redirect("/login", extra_headers=[("Set-Cookie", "session_id=; Max-Age=0; Path=/; HttpOnly; SameSite=Lax")])
            return

        if path == "/bmi":
            if not user:
                self.redirect("/login")
                return

            weight_raw = form.get("weight", [""])[0].strip().replace(",", ".")
            height_raw = form.get("height", [""])[0].strip().replace(",", ".")

            try:
                if not weight_raw or not height_raw:
                    self.respond_html(render_bmi(user, "Por favor, completa todos los campos"), status=400)
                    return

                weight = float(weight_raw)
                height = float(height_raw)

                if weight <= 0 or height <= 0:
                    self.respond_html(render_bmi(user, "El peso y la estatura deben ser mayores a 0"), status=400)
                    return

                imc = weight / (height ** 2)
                imc_rounded = round(imc, 2)
                analysis = get_bmi_analysis(imc)
                database.save_bmi(int(user["id"]), weight, height, imc_rounded, analysis["category"])
                result_html = render_bmi_result(imc_rounded, analysis)
                self.respond_html(render_bmi(user, "IMC calculado y guardado correctamente", "success", result_html))
                return

            except ValueError:
                self.respond_html(render_bmi(user, "Por favor, ingresa valores numéricos válidos"), status=400)
                return

        self.send_error(404, "Ruta no encontrada")

    def current_user(self) -> dict[str, object] | None:
        user_id = get_user_id_from_cookie(self.headers.get("Cookie"))
        if user_id is None:
            return None
        user = database.get_user(user_id)
        return user if user else None

    def read_form(self) -> dict[str, list[str]]:
        content_length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(content_length).decode("utf-8")
        return parse_qs(body)

    def respond_html(self, html_text: str, status: int = 200) -> None:
        encoded = html_text.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def respond_redirect(self, location: str, message: str = "", extra_headers: list[tuple[str, str]] | None = None) -> None:
        self.send_response(303)
        self.send_header("Location", location)
        if extra_headers:
            for key, value in extra_headers:
                self.send_header(key, value)
        self.end_headers()

    def redirect(self, location: str) -> None:
        self.send_response(302)
        self.send_header("Location", location)
        self.end_headers()

    def log_message(self, format: str, *args: object) -> None:
        return


def run() -> None:
    database.init_db()
    server = ThreadingHTTPServer((HOST, PORT), RequestHandler)
    print(f"Servidor iniciado en http://{HOST}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido")
    finally:
        server.server_close()


if __name__ == "__main__":
    run()
