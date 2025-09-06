import random
from shiny import ui, render, reactive
import plotly.graph_objects as go
from shinywidgets import output_widget, render_widget


# ===============================
# 🖥 UI de la página Torneo
# ===============================
page_ui = ui.page_fluid(
    ui.h2("🎾 Simulador de Torneo de Pádel"),

    ui.layout_columns(
        ui.panel_well(
            ui.h4("Cabezas de serie"),
            *[ui.input_text(f"cabeza{i}", f"Cabeza {i+1}", "") for i in range(4)]
        )
        ,
        ui.panel_well(
            ui.h4("No cabezas de serie"),
            *[ui.input_text(f"nocabeza{i}", f"No Cabeza {i+1}", "") for i in range(4)]
        ),
    ),

    ui.input_action_button("generar", "Generar Cuadro de Torneo", class_="btn btn-success"),

    output_widget("plot_bracket")
)

# ===============================
# ⚙️ Lógica del Servidor
# ===============================
def page_server(input, output, session):

    # Reactive para generar cuadro solo cuando se pulsa el botón
    @reactive.event(input.generar)
    def generar_torneo():
        # Obtener inputs como listas
        cabezas = [input[f"cabeza{i}"]() or f"Cabeza{i+1}" for i in range(4)]
        no_cabezas = [input[f"nocabeza{i}"]() or f"NoCabeza{i+1}" for i in range(4)]

        # Barajar y generar parejas
        random.shuffle(no_cabezas)
        parejas = list(zip(cabezas, no_cabezas))
        random.shuffle(parejas)

        # Crear partidos (semifinales)
        semifinales = [(parejas[0], parejas[1]), (parejas[2], parejas[3])]
        return semifinales

    # Renderizar el cuadro visual
    @output
    @render.ui
    def resultado_torneo():
        semifinales = generar_torneo()

        def pareja_str(p):
            return f"{p[0]} & {p[1]}"

        # Construir UI tipo cuadro
        cuadro = ui.div(
            ui.h3("🏆 Cuadro del Torneo"),
            ui.div(
                # Semifinal 1
                ui.panel_well(
                    ui.h4("Semifinal 1"),
                    ui.p(f"🔹 {pareja_str(semifinales[0][0])}"),
                    ui.p(f"🔸 vs"),
                    ui.p(f"🔹 {pareja_str(semifinales[0][1])}")
                ),
                # Semifinal 2
                ui.panel_well(
                    ui.h4("Semifinal 2"),
                    ui.p(f"🔹 {pareja_str(semifinales[1][0])}"),
                    ui.p(f"🔸 vs"),
                    ui.p(f"🔹 {pareja_str(semifinales[1][1])}")
                ),
                style="display:flex; justify-content:space-around; gap:20px;"
            ),
            ui.hr(),
            ui.h4("🏆 Final (Ganadores de Semifinales)"),
            ui.p("Por definir después de jugar las semifinales 😉"),
            style="margin-top:20px;"
        )
        return cuadro

    @output
    @render_widget
    def plot_bracket():

        semifinales = generar_torneo()

        fig = go.Figure()

        # Posiciones de las cajas (x0, x1, y0, y1)
        boxes = {
            "SF1_A": (0, 0.2, 0.8, 0.9),  # jugador 1 SF1
            "SF1_B": (0, 0.2, 0.6, 0.7),  # jugador 2 SF1
            "SF2_A": (0, 0.2, 0.4, 0.5),  # jugador 1 SF2
            "SF2_B": (0, 0.2, 0.2, 0.3),  # jugador 2 SF2
            "F1":    (0.4, 0.6, 0.7, 0.8), # ganador SF1
            "F2":    (0.4, 0.6, 0.3, 0.4), # ganador SF2
            "WIN":   (0.8, 1.0, 0.5, 0.6)  # campeón
        }

        # Colores
        color_box = "rgba(0,90,70,1)"
        color_text = "white"

        # Dibujar cajas y textos
        labels = {
            "SF1_A": f"{semifinales[0][0][0]} & {semifinales[0][0][1]}",
            "SF1_B": f"{semifinales[0][1][0]} & {semifinales[0][1][1]}",
            "SF2_A": f"{semifinales[1][0][0]} & {semifinales[1][0][1]}",
            "SF2_B": f"{semifinales[1][1][0]} & {semifinales[1][1][1]}",
            "F1": "Ganador SF1",
            "F2": "Ganador SF2",
            "WIN": "🏆 Campeón"
        }

        for key, (x0, x1, y0, y1) in boxes.items():
            # Caja
            fig.add_shape(type="rect", x0=x0, x1=x1, y0=y0, y1=y1,
                        line=dict(color="white"), fillcolor=color_box, layer="below")
            # Texto
            fig.add_trace(go.Scatter(
                x=[(x0+x1)/2], y=[(y0+y1)/2],
                text=[labels[key]], mode="text",
                textfont=dict(color=color_text, size=12),
                hoverinfo="skip"
            ))

        # Líneas de conexión
        connections = [
            ((0.2, 0.4), (0.85, 0.75)),  # SF1 → F1
            ((0.2, 0.4), (0.65, 0.75)),  # SF1 → F1
            ((0.2, 0.4), (0.45, 0.35)),  # SF2 → F2
            ((0.2, 0.4), (0.25, 0.35)),  # SF2 → F2
            ((0.6, 0.8), (0.75, 0.55)),  # F1 → WIN
            ((0.6, 0.8), (0.35, 0.55)),  # F2 → WIN
        ]
        for (x0, x1), (y0, y1) in connections:
            fig.add_shape(type="line", x0=x0, x1=x1, y0=y0, y1=y1, line=dict(color="black", width=2))

        # Layout
        fig.update_layout(
            xaxis=dict(showgrid=False, zeroline=False, visible=False, range=[-0.05, 1.05]),
            yaxis=dict(showgrid=False, zeroline=False, visible=False, range=[0, 1]),
            plot_bgcolor="rgba(230,240,220,1)",
            margin=dict(l=10, r=10, t=10, b=10),
            height=400
        )
        widget = go.FigureWidget(fig)
        return widget
