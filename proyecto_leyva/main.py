import flet as ft
import database


def main(page: ft.Page):
    page.title = "Proyecto PAEC: Vida Saludable"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#e5f3ff"
    page.scroll = ft.ScrollMode.AUTO

    def build_home_view():

        header = ft.Container(
            content=ft.Row([
                ft.Icon(ft.icons.Icons.FAVORITE, color="#ffd54f", size=40),
                ft.Column([
                    ft.Text("Proyecto PAEC", size=34, weight=ft.FontWeight.BOLD, color="#ffffff"),
                    ft.Text("Vida Saludable", size=20, color="#e7f3ff"),
                    ft.Text("Energía y concentración para tu vida escolar.", size=12, color="#dbe9ff")
                ], tight=True, spacing=4)
            ], alignment=ft.MainAxisAlignment.START, spacing=16),
            padding=24,
            bgcolor="#206fb6",
            border_radius=22
        )

        def card(icon, title_text, body_text):
            return ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(icon, color="#206fb6", size=24),
                        ft.Text(title_text, size=16, weight=ft.FontWeight.BOLD, color="#1f4f9c")
                    ], spacing=8, alignment=ft.MainAxisAlignment.START),
                    ft.Text(body_text, size=13, color="#444444")
                ], tight=True, spacing=10),
                padding=18,
                margin=0,
                bgcolor="#ffffff",
                border_radius=18,
                expand=True
            )

        cards = ft.Row([
            card(ft.icons.Icons.EGG, "Alimentación", "Frutas, verduras y proteína para rendir mejor."),
            card(ft.icons.Icons.FITNESS_CENTER, "Actividad", "Ejercicio diario para más energía y memoria."),
            card(ft.icons.Icons.BEDTIME, "Descanso", "Dormir bien ayuda a tu salud y rendimiento.")
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=12)

        history_button = ft.Button("Conciencia Histórica", icon=ft.icons.Icons.HISTORY, on_click=lambda e: navigate_to("/history"), bgcolor="#ffb703", color="#1f1f1f")
        chemistry_button = ft.Button("Reacciones Químicas", icon=ft.icons.Icons.SCIENCE, on_click=lambda e: navigate_to("/chemistry"), bgcolor="#fb8500", color="#ffffff")
        bmi_button = ft.Button("Calcular mi IMC", icon=ft.icons.Icons.FAVORITE, on_click=lambda e: navigate_to("/bmi"), bgcolor="#023047", color="#ffffff")

        home_col = ft.Column([
            header,
            ft.Divider(height=10),
            cards,
            ft.Row([history_button, chemistry_button, bmi_button], alignment=ft.MainAxisAlignment.CENTER, spacing=16)
        ], spacing=18)

        return ft.View(scroll=ft.ScrollMode.AUTO, controls=[ft.Container(content=home_col, padding=24, bgcolor="#f0f8ff")])

    def build_history_view():
        back_button = ft.Button("Volver", icon=ft.icons.Icons.ARROW_BACK, on_click=lambda e: navigate_to("/"), bgcolor="#206fb6", color="#ffffff")
        history_col = ft.Column([
            ft.Row([
                ft.Icon(ft.icons.Icons.HISTORY, color="#206fb6", size=32),
                ft.Text("Conciencia Histórica", size=24, weight=ft.FontWeight.BOLD, color="#2b7cff")
            ], alignment=ft.MainAxisAlignment.START, spacing=12),
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
        back_button = ft.Button("Volver", icon=ft.icons.Icons.ARROW_BACK, on_click=lambda e: navigate_to("/"), bgcolor="#206fb6", color="#ffffff")
        chem_col = ft.Column([
            ft.Row([
                ft.Icon(ft.icons.Icons.SCIENCE, color="#206fb6", size=32),
                ft.Text("Reacciones Químicas", size=24, weight=ft.FontWeight.BOLD, color="#2b7cff")
            ], alignment=ft.MainAxisAlignment.START, spacing=12),
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
                database.save_bmi(weight, height, imc_rounded, category)
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
    route_change(page.route or "/")


if __name__ == "__main__":
    database.init_db()
    ft.run(main)
