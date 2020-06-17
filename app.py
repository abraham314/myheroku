import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
from dash.dependencies import Input, Output
import numpy as np

cr=pd.read_csv("cr.csv",parse_dates=True,index_col="FECHA_INGRESO")
ejxx=pd.read_csv("ejxx.csv",parse_dates=True,index_col="FECHA_INGRESO")

mgr_options = list(np.sort(cr["edo"].unique()))
mgr_options=["Pais"]+mgr_options
muns=["Nada"]+list(np.sort(ejxx["municipio_resx"].unique()))

app = dash.Dash()
server = app.server

app.layout = html.Div([
    
    html.Div([
    html.H1("Mapa"),
    html.Iframe(id="map",srcDoc=open("covid_por_mpio.html",encoding="utf8").read(),width="100%",height="600")
        
    ]),
        
    html.Div(
        [
            html.H2("Casos"),
            dcc.Dropdown(
                id="Manager",
                options=[{
                    'label': i,
                    'value': i
                } for i in mgr_options],
                value='Pais'),
        ],
        style={'width': '25%',
               'display': 'inline-block'}),
    
        html.Div(
        [
            html.H3("Casos Mpo."),
            dcc.Dropdown(
                id="Muns",
                options=[{
                    'label': i,
                    'value': i
                } for i in muns],
                value='Nada'),
        ],
        style={'width': '25%',
               'display': 'inline-block'}), 
    
    dcc.Graph(id='funnel-graph')   
])

@app.callback(Output('funnel-graph', 'figure'),[Input('Manager', 'value'),Input('Muns', 'value')])
def update_graph(Manager,Muns):
    if Muns=="Nada":
        

        if Manager == "Pais":

            df_plot = cr.copy()
            ax3=df_plot.groupby(df_plot.index)[["RESULTADO"]].sum()
            tr=go.Bar(x=ax3.index, y=ax3["RESULTADO"],marker=dict(color=ax3["RESULTADO"]))
        else:
            df_plot = cr[cr['edo'] == Manager]

            pv = pd.pivot_table(
                df_plot,
                index=df_plot.index,
                columns=["edo"],
                values=['RESULTADO'],
                #aggfunc=sum,
                fill_value=0)
        #    import plotly.graph_objs as go  
            tr=go.Bar(x=pv.index, y=pv[pv.columns[0]], name=Manager,marker=dict(color=pv[pv.columns[0]]))
    else:
        df_plot = ejxx[ejxx["municipio_resx"] == Muns]

        pv = pd.pivot_table(
                df_plot,
                index=df_plot.index,
                columns=["municipio_resx"],
                values=['RESULTADO'],
                #aggfunc=sum,
                fill_value=0)
        #    import plotly.graph_objs as go  
        tr=go.Bar(x=pv.index, y=pv[pv.columns[0]], name=Muns,marker=dict(color=pv[pv.columns[0]]))
        #Manager=Muns    
    return {
    'data': [tr],
    'layout':
    go.Layout(
        title='Curvas: {}'.format(Manager))}

if __name__ == '__main__':
    app.run_server(debug=True,use_reloader=False)

