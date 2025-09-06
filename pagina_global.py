from shiny import App, Inputs, Outputs, Session, reactive, render, req, ui
from shinywidgets import output_widget, render_widget

from shiny import ui, render
import pandas as pd
from shinywidgets import render_plotly
import plotly.graph_objects as go
import tournament

# ===============================
# 📌 Datos de ranking e histórico de partidos
# ===============================
ranking_data = pd.read_feather('ranking.ftr')
historico = pd.read_excel('RankingPadel.xlsx', skiprows = 2).iloc[:,1:].dropna()

# ===============================
# 🎨 Podio Top 3
# ===============================
top3 = ranking_data.sort_values("Rating", ascending=False).head(3).reset_index(drop=True)
colores = ["#FFD700", "#C0C0C0", "#CD7F32"]

def podio_component():

    cards = []
    for i, row in top3.iterrows():
        print(row['Palistas'])
        print(f"podio_{row['Palistas'].lower()}")
        cards.append(
            ui.div(
                ui.h3(f"{['🥇','🥈','🥉'][i]} {i+1}° {row['Palistas']}"),
                ui.output_image(f"podio_{row['Palistas'].lower()}", inline=True),
                ui.p(f"Rating: {round(row['Rating'],1)}"),
                style=f"text-align:center; background:{colores[i]}; padding:10px; border-radius:10px; width:150px;"
            )
        )
    
    return ui.div(
        ui.h2("🏆 Podio Top 3"),
        ui.div(*cards, style="display:flex; justify-content:space-around;"),
        style="margin-bottom:30px;"
    )

# ===============================
# 📊 Gráfico opcional del Top 3
# ===============================
def plot_podio():
    top3 = ranking_data.sort_values("Rating", ascending=False).head(3)
    fig = go.Figure(
        go.Bar(
            x=top3["Palistas"],
            y=top3["Rating"],
            marker_color=["#FFD700", "#C0C0C0", "#CD7F32"],
            text=top3["Rating"],
            textposition="outside"
        )
    )
    fig.update_layout(title="Top 3 Ranking", yaxis_title="Rating")
    widget =  go.FigureWidget(fig)
    return widget

# ===============================
# 🖥 UI de la página Home
# ===============================
page_ui = ui.navset_card_underline(
    ui.nav_panel("Ranking general", 
        podio_component(),
        # output_widget("podio_plot"),
        ui.h3("📋 Ranking completo"),
        ui.output_table("tabla_ranking")
    ),
    ui.nav_panel('Histórico Partidos',
        ui.output_table("tabla_historico")),
    ui.nav_panel('Simulador Torneos', tournament.page_ui),
)

# ===============================
# ⚙️ Lógica Server
# ===============================
def page_server(input, output, session):
    @output
    @render_widget
    def podio_plot():
        return plot_podio()
    
    @output(id=f"podio_{top3.loc[0, 'Palistas'].lower()}")
    @render.image
    def _(output_id=f"podio_{top3.loc[0, 'Palistas'].lower()}"):
        return {
            "src": f"fotos/{top3.loc[0, 'Palistas'].lower()}.jpeg",
            "width": "90",
            }
    
    @output(id=f"podio_{top3.loc[1, 'Palistas'].lower()}")
    @render.image
    def _(output_id=f"podio_{top3.loc[1, 'Palistas'].lower()}"):
        return {
            "src": f"fotos/{top3.loc[1, 'Palistas'].lower()}.jpeg",
            "width": "90",
            }
    
    @output(id=f"podio_{top3.loc[2, 'Palistas'].lower()}")
    @render.image
    def _(output_id=f"podio_{top3.loc[2, 'Palistas'].lower()}"):
        return {
            "src": f"fotos/{top3.loc[2, 'Palistas'].lower()}.jpeg",
            "width": "90",
            }

    @output
    @render.table
    def tabla_ranking():
        db = ranking_data.filter(regex = 'Pal|juga|gana|Ratin|empata|perd').reset_index(drop=True).reset_index().rename(columns = {'index' : 'Ranking'})
        db['Ranking'] = [f"# {i+1}" for i in db.Ranking]
        # Supongamos que tus columnas se llaman exactamente así:
        porcentaje_cols = ["% partidos ganados", "% partidos empatados", "% partidos perdidos", "% sets ganados", "% juegos ganados"]

        return (
            db.style     
            # Formatear Rating con un solo decimal
            .format({"Rating": "{:.1f}".format,
                     "% partidos ganados": "{:.1f}%".format,
                     "% partidos empatados": "{:.1f}%".format,
                     "% partidos perdidos": "{:.1f}%".format,
                      "% sets ganados": "{:.1f}%".format,
                       "% juegos ganados": "{:.1f}%".format})
            # Colorear las tres primeras filas
            .apply(lambda x: ["background-color: #FFD700"] + ["background-color: #C0C0C0"] + ["background-color: #CD7F32"] + [""] * (len(x)-3), axis=0)
            # Mantener los atributos de la tabla y ocultar el índice
            .set_table_attributes('class="dataframe shiny-table table w-auto"')
            .hide(axis="index"))

    
    @output
    @render.table
    def tabla_historico():
        return historico.style.set_table_attributes(
                    'class="dataframe shiny-table table w-auto"'
                )\
                .hide(axis="index")
    
    tournament.page_server(input, output, session)

