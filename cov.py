import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash()

'''app.layout =html.Div([
    html.H1("Mapa"),
    html.Iframe(id="map",srcDoc=open("covid_por_mpio.html",encoding="utf8").read(),width="100%",height="600")
        
    ])
'''
if __name__ == '__main__':
    
    app.run_server()

