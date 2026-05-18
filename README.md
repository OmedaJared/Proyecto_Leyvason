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

- Python
- Flet (Framework para interfaces gráficas)
- SQLite (Base de datos)
- uv (Gestor de paquetes y entornos virtuales)