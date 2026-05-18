import flet as ft
import database


def main(page: ft.Page):
    page.title = "Proyecto PAEC: Vida Saludable"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.AUTO

    # --- Content pieces reused in home view
    title = ft.Text("Proyecto PAEC: Vida Saludable", size=24, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)

    intro = ft.Text(
        "Fundamento: Vida saludable: Comprender los cambios necesarios para llevar una vida saludable: cambios en hábitos alimenticios, actividad física y descanso, así como el beneficio e impacto en el desempeño académico de los alumnos.\n\n"
        "Propósito: Comprender que cambios son necesarios para llevar a cabo una vida saludable, añadir algunas recomendaciones en la alimentación, actividad física y descanso, y definir como benefician estos cambios en el desempeño académico.\n\n"
        "Objetivo: Desarrollar una Interfaz gráfica en lenguaje Python, utilizando el Framework Flet, conectando con base de datos, en la que se muestre la información generada en las asignaturas de conciencia histórica y reacciones químicas.",
        size=14
    )

    diet_title = ft.Text("Hábitos Alimenticios", size=18, weight=ft.FontWeight.BOLD)
    diet_text = ft.Text(
        "Cambios necesarios: Adoptar una dieta equilibrada rica en frutas, verduras, proteínas magras y granos enteros. Reducir el consumo de azúcares procesados y grasas saturadas.\n"
        "Recomendaciones: Desayunar completo, comer porciones moderadas, hidratarse bien."
    )

    exercise_title = ft.Text("Actividad Física", size=18, weight=ft.FontWeight.BOLD)
    exercise_text = ft.Text(
        "Cambios necesarios: Incorporar al menos 30 minutos de actividad física moderada diaria.\n"
        "Recomendaciones: Caminar, correr, nadar, practicar deportes. Incluir ejercicios de fuerza 2-3 veces por semana."
    )

    rest_title = ft.Text("Descanso", size=18, weight=ft.FontWeight.BOLD)
    rest_text = ft.Text(
        "Cambios necesarios: Dormir 7-9 horas por noche, mantener rutinas de sueño consistentes.\n"
        "Recomendaciones: Evitar pantallas 1 hora antes de dormir, crear un ambiente tranquilo para dormir."
    )

    academic_title = ft.Text("Beneficio e Impacto en el Desempeño Académico", size=18, weight=ft.FontWeight.BOLD)
    academic_text = ft.Text(
        "Estos cambios mejoran la concentración, memoria, reducción del estrés y aumento de la energía, lo que resulta en mejor rendimiento escolar, asistencia y motivación."
    )

    hist_title = ft.Text("Conciencia Histórica", size=18, weight=ft.FontWeight.BOLD)
    hist_text = ft.Text(
        "Comprender la historia nos permite valorar cómo las sociedades han evolucionado hacia estilos de vida más saludables, reconociendo la salud como un derecho fundamental adquirido a través del tiempo."
    )

    chem_title = ft.Text("Reacciones Químicas", size=18, weight=ft.FontWeight.BOLD)
    chem_text = ft.Text(
        "Las reacciones químicas en el cuerpo, como el metabolismo de nutrientes y la producción de energía, requieren una alimentación adecuada y descanso para funcionar óptimamente, impactando directamente en la salud general."
    )

    # --- Helpers to build views
    def build_home_view():
        bmi_button = ft.Button("Calcular mi IMC", on_click=lambda e: navigate_to("/bmi"))

        # Build a card-based layout using Flet controls (colors via hex codes)
        header = ft.Container(
            content=ft.Text("Proyecto PAEC: Vida Saludable", size=28, weight=ft.FontWeight.BOLD, color="#2b7cff"),
            padding=12,
            bgcolor="#ffffff",
            border_radius=8
        )

        def card(title_text, body_text):
            return ft.Container(
                content=ft.Column([
                    ft.Text(title_text, size=18, weight=ft.FontWeight.BOLD, color="#1f4f9c"),
                    ft.Text(body_text, size=13, color="#444444")
                ], tight=True, spacing=6),
                padding=12,
                margin=10,
                bgcolor="#ffffff",
                border_radius=8
            )

        cards = ft.Column([
            card("Fundamento", "Vida saludable: Comprender los cambios necesarios para llevar una vida saludable: cambios en hábitos alimenticios, actividad física y descanso, asín como el beneficio e impacto en el desempeño académico de los alumnos."),
            card("Propósito", "Comprender que cambios son necesarios para llevar a cabo una vida saludable, añadir algunas recomendaciones en la alimentación, actividad física y descanso, y definir como benefician estos cambios en el desempeño académico."),
            card("Objetivo", "Desarrollar una Interfaz gráfica en lenguaje Python, utilizando el Framework Flet, conectando con base de datos, en la que se muestre la información generada en las asignaturas de conciencia histórica y reacciones químicas."),
            card("Hábitos Alimenticios", "Adoptar una dieta equilibrada rica en frutas, verduras, proteínas magras y granos enteros. Reducir azúcares procesados y grasas saturadas. Recomendaciones: Desayunar completo, porciones moderadas, hidratarse bien."),
            card("Actividad Física", "Incorporar al menos 30 minutos de actividad física moderada diaria. Recomendaciones: Caminar, correr, nadar, practicar deportes. Incluir fuerza 2-3 veces por semana."),
            card("Descanso", "Dormir 7-9 horas por noche, mantener rutinas de sueño. Evitar pantallas 1 hora antes de dormir.")
        ])

        history_button = ft.Button("Conciencia Histórica", on_click=lambda e: navigate_to("/history"))
        chemistry_button = ft.Button("Reacciones Químicas", on_click=lambda e: navigate_to("/chemistry"))

        home_col = ft.Column([
            header,
            ft.Divider(height=10),
            cards,
            ft.Row([history_button, chemistry_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Row([bmi_button], alignment=ft.MainAxisAlignment.END)
        ], spacing=12)

        return ft.View(scroll=ft.ScrollMode.AUTO, controls=[ft.Container(content=home_col, padding=20, bgcolor="#f7fbff")])

    def build_history_view():
        back_button = ft.Button("Volver", on_click=lambda e: navigate_to("/"))
        history_col = ft.Column([
            ft.Text("Conciencia Histórica", size=24, weight=ft.FontWeight.BOLD, color="#2b7cff"),
            ft.Divider(),
            ft.Text(
                "Comprender la historia nos permite valorar cómo las sociedades han evolucionado hacia estilos de vida más saludables, reconociendo la salud como un derecho fundamental adquirido a través del tiempo.",
                size=14,
                color="#444444"
            ),
            ft.Divider(),
            back_button
        ], spacing=12)
        return ft.View(scroll=ft.ScrollMode.AUTO, controls=[ft.Container(content=history_col, padding=20, bgcolor="#f7fbff")])

    def build_chem_view():
        back_button = ft.Button("Volver", on_click=lambda e: navigate_to("/"))
        chem_col = ft.Column([
            ft.Text("Reacciones Químicas", size=24, weight=ft.FontWeight.BOLD, color="#2b7cff"),
            ft.Divider(),
            ft.Text(
                "Las reacciones químicas en el cuerpo, como el metabolismo de nutrientes y la producción de energía, requieren una alimentación adecuada y descanso para funcionar óptimamente, impactando directamente en la salud general.",
                size=14,
                color="#444444"
            ),
            ft.Divider(),
            back_button
        ], spacing=12)
        return ft.View(scroll=ft.ScrollMode.AUTO, controls=[ft.Container(content=chem_col, padding=20, bgcolor="#f7fbff")])

    def build_bmi_view():
        weight_field = ft.TextField(label="Peso (kg)", width=200)
        height_field = ft.TextField(label="Estatura (m)", width=200)
        result_container = ft.Container()

        def calculate_imc(e):
            try:
                weight = float(weight_field.value)
                height = float(height_field.value)
                if height <= 0:
                    raise ValueError
                imc = weight / (height ** 2)
                imc_rounded = round(imc, 2)

                if imc < 18.5:
                    category = "Bajo peso"
                    rec = "Aumenta tu ingesta calórica con alimentos nutritivos y equilibrados. Consulta a un nutricionista para un plan personalizado."
                    exercises = "Incluye ejercicios de fuerza como levantamiento de pesas ligeras para ganar masa muscular, combinados con alimentación rica en proteínas."
                elif imc < 25:
                    category = "Peso normal o saludable"
                    rec = "Mantén una dieta equilibrada con porciones moderadas y actividad física regular. Continúa con hábitos saludables."
                    exercises = "Practica caminatas diarias, natación, yoga o cualquier actividad que disfrutes para mantener la forma."
                elif imc < 30:
                    category = "Sobrepeso"
                    rec = "Reduce el consumo de calorías, aumenta el intake de verduras y frutas, y combina con ejercicio regular."
                    exercises = "Camina al menos 45 minutos diarios, practica ciclismo o danza para quemar calorías extra."
                elif imc < 35:
                    category = "Obesidad grado I"
                    rec = "Consulta a un médico para un plan de pérdida de peso. Adopta una dieta baja en calorías y ejercicio supervisado."
                    exercises = "Ejercicios aeróbicos moderados como caminar rápido o nadar, bajo supervisión si es necesario."
                elif imc < 40:
                    category = "Obesidad grado II"
                    rec = "Busca tratamiento médico integral, incluyendo dieta estricta y posible intervención médica."
                    exercises = "Actividades de bajo impacto como nadar o usar máquina elíptica para evitar lesiones."
                else:
                    category = "Obesidad grado III (obesidad mórbida)"
                    rec = "Consulta inmediatamente a un especialista. Puede requerir cirugía bariátrica y seguimiento médico estricto."
                    exercises = "Ejercicios adaptados y de bajo impacto bajo estricta supervisión médica."

                benefits = "Beneficios de llevar una vida saludable: Mejor salud cardiovascular, aumento de energía, reducción de estrés, mejora en la concentración y rendimiento académico."

                # Save to DB
                database.save_bmi(weight, height, imc_rounded, category)

                # Show result in the result container
                result_container.content = ft.Column([
                    ft.Text(f"IMC calculado: {imc_rounded}", size=16, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Categoría: {category}", size=14),
                    ft.Text(f"Recomendaciones: {rec}", size=12),
                    ft.Text(f"Ejercicios recomendados: {exercises}", size=12),
                    ft.Text(f"{benefits}", size=12),
                    ft.Text("Nota: El IMC no siempre refleja la composición corporal exacta (ej. atletas con masa muscular).", size=10, italic=True)
                ], tight=True, spacing=8)
                page.update()

            except Exception:
                page.dialog = ft.AlertDialog(
                    title=ft.Text("Error"),
                    content=ft.Text("Por favor, ingresa valores numéricos válidos para peso y estatura."),
                    actions=[ft.TextButton("OK", on_click=lambda e: page.dialog.close())]
                )
                page.dialog.open = True
                page.update()

        back_button = ft.TextButton("Volver", on_click=lambda e: navigate_to("/"))

        bmi_col = ft.Column([
            ft.Text("Calculadora de IMC", size=20, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            weight_field,
            height_field,
            ft.Button("Calcular IMC", on_click=calculate_imc),
            ft.Divider(),
            result_container,
            ft.Divider(),
            back_button
        ], spacing=12)

        return ft.View(scroll=ft.ScrollMode.AUTO, controls=[ft.Container(content=bmi_col, padding=20)])

    # --- Routing: show different views depending on route
    def route_change(route):
        page.views.clear()
        if page.route == "/" or page.route == "":
            page.views.append(build_home_view())
        elif page.route == "/bmi":
            page.views.append(build_bmi_view())
        elif page.route == "/history":
            page.views.append(build_history_view())
        elif page.route == "/chemistry":
            page.views.append(build_chem_view())
        page.update()

    def navigate_to(route):
        page.route = route
        route_change(route)

    page.on_route_change = route_change
    # inicializar vista
    route_change(page.route or "/")


if __name__ == "__main__":
    database.init_db()
    ft.run(main)
