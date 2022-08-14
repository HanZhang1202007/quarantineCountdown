from re import S
import dash
from dash import dcc
from dash import html
from dash import dash_table
from dash import ctx
import dash_bootstrap_components as dbc
import pandas as pd
import datetime as dt
from dash.dependencies import Input, Output


df_food = pd.DataFrame(data={'snack': ['brownie','jelly', 'instant coffee', 'americano','nuts', 'chocolate', 'water'], 'amount': [4, 4, 6, 1, 1, 4, 9]},  index=[0,1,2,3,4,5,6])

app = dash.Dash(
    external_stylesheets=[dbc.themes.MINTY]
)

LEAVE = dt.datetime.strptime('2022-08-18', '%Y-%m-%d')
LEAVE = LEAVE.replace(hour=15)

app.title = 'Quarantine Count'

app.layout = html.Div([ 
    html.Header("surviving quarantine: I'M THE BEST HUMAN/ GENIUS"),
    html.Br(),
    html.Div(id='countdown-text'),
    dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0
        ),
    html.Br(),
    html.H3('Snack Tracker'),
    dbc.Row([
        dbc.Col(
            dbc.Card([
            dbc.CardImg(src='https://assetcdn.buhlergroup.com/rendition/874601345621/6f9ed36161454232ab1f9cd3c31d3c4f/-FJPG-TwebHeader_1x1-S1024x1024', 
                top=True, style={'width':'100%', 'height': '120px', 'object-fit': 'cover'}),
            dbc.CardBody(html.Div([dcc.Dropdown(id='dropdown', options=df_food.snack.values.tolist(), value=df_food.snack.values.tolist()[0])])),
            dbc.Row([dbc.Col(dbc.Button('increase', className='btn-secondary' ,id='increase-button', n_clicks=0, style={'text-align':'center'}), width=4) , 
                dbc.Col(dbc.Button('decrease', id='decrease-button', n_clicks=0, style={'text-align':'center'}),width=4),
                dbc.Col(dbc.Button('reset', className='btn-warning', id='reset-button', n_clicks=0, style={'text-align':'center'}),width=4)],
            justify="center"),
        ], style={'text-align':'center'}),width=4),
        dbc.Col(html.Div(id='table', style={'width': '50%', 'margin-left': 'auto', 'margin-right': 'auto'}),width=8)
    ], justify='center'),
    # html.Div([dateTable]),

], style={'text-align':'center', 'margin':'5%'})

@app.callback(Output('countdown-text', 'children'),
              Input('interval-component', 'n_intervals'))
def update_metrics(n):
    countdown = LEAVE - dt.datetime.now()
    countdownText = 'COUNTDOWN: '+str(countdown)
    return [html.H1(countdownText)]

@app.callback(Output('table','children'),
            [Input('dropdown', 'value'),
            Input('increase-button', 'n_clicks'),
            Input('decrease-button', 'n_clicks'),
            Input('reset-button', 'n_clicks')])
def update_table(value, btn1, btn2, btn3):
    df_table = df_food.copy()
    button_id = ctx.triggered_id
    if button_id == 'increase-button':
        print('increased')
        df_table.loc[df_table['snack']==value,'amount'] += 1
    elif button_id == 'decrease-button':
        print('decreased')
        df_table.loc[df_table['snack']==value,'amount'] -= 1
    elif button_id == 'reset-button':
        print('reset')
        df_table.loc[df_table['snack']==value,'amount'] = df_food.loc[df_food['snack']==value,'amount'] 
    else :
        print('nothing')
    
    return dash_table.DataTable(df_table.to_dict('records'), 
        style_cell={'textAlign': 'center', 'font-family':'Copperplate'},
        style_as_list_view=True)

# @app.callback(Output('table','children'),
#             [Input('dropdown', 'value'),
#             Input('decrease-button', 'n_clicks')])
# def update_table(value, n_clicks):
#     df_table = df_food.copy()
#     if n_clicks >0:
#         print('decreased')
#         df_table.loc[df_table['food']==value,'amount'] -= 1
    
#     return dash_table.DataTable(df_table.to_dict('records'), 
#         style_cell={'textAlign': 'center', 'font':'Helvetica'},
#         style_as_list_view=True)

# @app.callback(Output('table','children'),
#             [Input('dropdown', 'value'),
#             Input('reset-button', 'n_clicks')])
# def update_table(value, n_clicks):
#     df_table = df_food.copy()
#     if n_clicks >0:
#         print('reset')
#         df_table.loc[df_table['food']==value,'amount'] = df_food.loc[df_table['food']==value,'amount'] 
    
#     return dash_table.DataTable(df_table.to_dict('records'), 
#         style_cell={'textAlign': 'center', 'font':'Helvetica'},
#         style_as_list_view=True)


if __name__ == "__main__":
    app.run_server()

