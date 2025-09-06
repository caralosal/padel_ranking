from shiny import ui, render
from shiny import App, Inputs, Outputs, Session
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from shinywidgets import output_widget, render_widget

# ===============================
# 📌 Datos de ranking e histórico de partidos
# ===============================
ranking_data = pd.read_feather('ranking.ftr')
historico = pd.read_excel('RankingPadel.xlsx', skiprows = 2).iloc[:,1:].dropna()

emparejamientos = ranking_data.set_index('Palistas').filter(regex = 'Par')
enfrentamientos = ranking_data.set_index('Palistas').filter(regex = 'Contr')

def get_top_3_personas(palista, df):
    return [(paraja.replace('Pareja_', '').replace('Contrincante_', '').lower(), value) for paraja, value in zip(df.loc[palista].sort_values(ascending=False)[:3].index,
                                                         df.loc[palista].sort_values(ascending=False)[:3].values)]




class Padelista:
    def __init__(self, nombre, image, input = Inputs, output = Outputs, session = Session):
        self.nombre = nombre
        self.input = input
        self.output = output
        self.session = session
        self.image = image

    def create_ui(self):
        pag_general = ui.navset_card_underline(
            ui.nav_panel(
                self.nombre,
                ui.output_image(f"imagen_{self.nombre.lower()}")
                
                            )
        )
        
        return pag_general

    def page_server(self, input, output, session):
        top3_pareja = get_top_3_personas(self.nombre, emparejamientos)      
        top3_contrincante = get_top_3_personas(self.nombre, enfrentamientos)
        print(top3_contrincante)
        print(top3_pareja)
        @output(id=f"imagen_{self.nombre.lower()}")
        @render.image
        def _(output_id=f"imagen_{self.nombre.lower()}"):
            print(f"Mostrando imagen para {self.nombre}: {self.image}")
            return {
                "src": self.image,
                "width": "400px",
                "heigth" : "400px",
                "alt": f"Foto de {self.nombre}"
            }
