#!/usr/bin/python3

import flask
import dash
import pandas as pd
from dash import dash_table
from dash import html
import missing11


#########
# Serveur
server = flask.Flask(__name__)
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, server=server, title='Missing11 choice', external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True

df = pd.read_csv("missing11.csv")
df["URL"] = df["URL"].apply(lambda x: f'[{x}]({x})')

##############
### Layout
app.layout = html.Div(
    children=[
        html.H1('Tous les matchs de Missing 11 pour des moments de qualité entre collègues',className='logo'),
        html.Div([
            dash_table.DataTable(
                id='datatable-interactivity',
                columns=[
                    {"name": i, "id": i, "deletable": False, "selectable": True, "presentation": 'markdown'} for i in df.columns
                ],
                style_cell_conditional=[
                    {
                        'if': {'column_id': col},
                        'fontWeight': 'bold'
                    } for col in ['Team à trouver']
                ],
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(240, 240, 240)'
                    }
                ],
                data=df.to_dict('records'),
                # editable=True,
                filter_action="native",
                sort_action="native",
                sort_mode="multi",
                selected_columns=[],
                selected_rows=[],
                page_action="native",
                page_size= 3000,
            )
        ]),
        html.Div(
            children=[
                "Source : ", html.A("Github", href="https://github.com/tescrihuela/missing11"),
            ]
        )
    ]
)

######
# Main
if __name__ == '__main__':
    app.run_server(debug=True)

