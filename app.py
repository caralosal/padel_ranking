# Librería de la app web
from shiny import App, Inputs, Outputs, Session, reactive, render, req, ui
from shinywidgets import output_widget, render_widget
from padelista import Padelista
import tournament
import pagina_global 

import os
print(os.listdir())
# Instancia de cada jugador de padel
carlos = Padelista('Carlos', 'fotos/carlos.jpeg')
mini = Padelista('Mini', 'fotos/mini.jpeg')
damian = Padelista('Damian', 'fotos/damian.jpeg')
ismael = Padelista('Ismael', 'fotos/ismael.jpeg')
jota = Padelista('Jota', 'fotos/jota.jpeg')
dani = Padelista('Dani', 'fotos/dani.jpeg')
jorge = Padelista('Jorge', 'fotos/jorge.jpeg')
ruben = Padelista('Ruben', 'fotos/ruben.jpeg')

# User interface de todo lo que se quiere visualizar
app_ui = ui.page_navbar(
    ui.nav_panel('Ranking', pagina_global.page_ui),
    ui.nav_panel("Carlos", carlos.create_ui()),
    ui.nav_panel("Mini", mini.create_ui()),
    ui.nav_panel("Damian", damian.create_ui()),
    ui.nav_panel("Ismael", ismael.create_ui()),
    ui.nav_panel("Jota", jota.create_ui()),
    ui.nav_panel("Dani", dani.create_ui()),
    ui.nav_panel("Jorge", jorge.create_ui()),
    ui.nav_panel("Ruben", ruben.create_ui()),

)

# Servidor con las funcionalidades de cada apartado
def server(input, output, session):
    # Aquí llamas a los servers de cada página
    pagina_global.page_server(input, output, session)
    carlos.page_server(input, output, session)
    mini.page_server(input, output, session)
    damian.page_server(input, output, session)
    ismael.page_server(input, output, session)
    jota.page_server(input, output, session)
    dani.page_server(input, output, session)
    jorge.page_server(input, output, session)
    ruben.page_server(input, output, session)
    

# Ejecución de la aplicación
app = App(app_ui, server)
app.run()