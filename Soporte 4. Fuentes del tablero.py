
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import psycopg2
from dotenv import load_dotenv
import os
import pandas.io.sql as sqlio
import plotly.express as px
import joblib

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

env_path = "C:\\Users\\gutil\\OneDrive - Universidad de los andes\\Escritorio\\Ingenieria Industrial\\2024-01\\Analitica Computacional Para la Toma de Decisiones\\Proyecto\\Proyecto 2\\env\\app.env"

# load env 
load_dotenv(dotenv_path=env_path)
# extract env variables
USER=os.getenv('USER')
PASSWORD=os.getenv('PASSWORD')
HOST=os.getenv('HOST')
PORT=os.getenv('PORT')
DBNAME=os.getenv('DBNAME')

print(DBNAME)
print(USER)
print(PASSWORD)
print(HOST)
print(PORT)

titulo_style = {
    'font-family': 'Jomolhari',
    'font-style': 'normal',
    'font-weight': '400',
    'font-size': '40px',
    'line-height': '51px',
    'color': '#000000',
    'width': '1440px',
    'height': '70px',
    'left': '0px',
    'top': '0px',
    'text-align': 'center'
}

tab_style = {
    'font-family': 'Jomolhari',
    'font-size': '20px',
}

engine = psycopg2.connect(
    dbname=DBNAME,
    user=USER,
    password=PASSWORD,
    host=HOST,
    port=PORT
)

cursor = engine.cursor()

# Primera consulta
query = """
SELECT
    SUM(CASE WHEN default_payment_next_month = 1 THEN 1 ELSE 0 END) / CAST(COUNT(*) AS FLOAT) * 100 AS Default_Percentage,
    SUM(CASE WHEN default_payment_next_month = 0 THEN 1 ELSE 0 END) / CAST(COUNT(*) AS FLOAT) * 100 AS No_Default_Percentage
FROM 
    prodq1

;"""
df = sqlio.read_sql_query(query, engine)
df

y1 = df['default_percentage'].tolist()
y2 = df['no_default_percentage'].tolist()
y1 = y1[0]
y2 = round(y2[0],2)

porcentaje_default = html.Span(
    f'{y1}%', style={'color': 'red', 'font-size': '72px'})

porcentaje_no_default = html.Span(
    f'{y2}%', style={'color': 'blue', 'font-size': '72px'})


texto_default = html.Span(
    'La cantidad de personas que hacen default es de ', style={'color': 'black', 'font-size': '20px'})

texto_no_default = html.Span(
    'La cantidad de personas que hacen no default es de ', style={'color': 'black', 'font-size': '20px'})



# Segunda Consulta

query = """
SELECT 
    pay_0,pay_2,pay_3,pay_4,pay_5,pay_6,
    default_payment_next_month
FROM prodq1

;"""
df = sqlio.read_sql_query(query, engine)
df

lista = df['pay_0'].tolist() + \
        df['pay_2'].tolist() + \
        df['pay_3'].tolist() + \
        df['pay_4'].tolist() + \
        df['pay_5'].tolist() + \
        df['pay_6'].tolist()

lista1 = df['default_payment_next_month'].tolist() + \
         df['default_payment_next_month'].tolist() + \
         df['default_payment_next_month'].tolist() + \
         df['default_payment_next_month'].tolist() + \
         df['default_payment_next_month'].tolist() + \
         df['default_payment_next_month'].tolist()

unicos = set(lista)

dic = {valor: 0 for valor in unicos}
dic_no = {valor: 0 for valor in unicos}


for i in range(0, len(lista)):
    retraso = lista[i]
    default = lista1[i]
    if default == 1:
        dic[retraso] += 1
    else:
        dic_no[retraso] += 1

x = list(dic.keys())

y1 = list(dic.values())
y2 = list(dic_no.values())


gr1 = px.bar(x=x, y=[y2,y1], barmode = 'group')

gr1.update_layout(
    legend = {'title': '', 'itemsizing': 'constant', 'tracegroupgap': 0},
    xaxis_title = 'Meses de Retraso en el Pago del Credito', yaxis_title = '',
    xaxis={'showgrid': False, 'showline': False, 'showticklabels': True},
    yaxis={'showgrid': False, 'showline': False, 'showticklabels': False,},
    plot_bgcolor='rgba(0,0,0,0)'
)


gr1.data[0].name = 'No Default'
gr1.data[1].name = 'Default'


app = dash.Dash(__name__)

tab1_layout = html.Div([

    html.Div([
        html.Div('Proporcion de Default Dentro de los Datos', style={'textAlign': 'center', 'font-size':'30px', 'margin': '20px', 'font-weight': 'bold'})
    ]),

    html.Div([
        html.Div(texto_default, style={'textAlign': 'left', 'flex': 1}),
        html.Div(texto_no_default, style={'textAlign': 'right', 'flex': 1})
    ], style={'display': 'flex', 'justifyContent': 'space-between', 'margin': '20px'}),

    html.Div([
        html.Div(porcentaje_default, style={'textAlign': 'left', 'flex': 1}),
        html.Div(porcentaje_no_default, style={'textAlign': 'right', 'flex': 1})
    ], style={'display': 'flex', 'justifyContent': 'space-between', 'margin': '20px'}),

    # Grafico 1
    html.Div([
        html.H3('Porcentaje de Personas Que Cometen o No Default Segun Aspectos Sociodemograficos', style={'font-size': '30px', 'textAlign': 'center'}),
        html.H3('Seleccione un Aspecto Sociodemografico', style={'font-weight': 'normal', 'textAlign': 'center'}),
        html.Div([dcc.Dropdown(id='aspecto', value='education',
                  options=['education', 'sex', 'marriage'],
                  style={'width': '33%', 'margin': 'auto'})]),
        
        dcc.Graph(
            id='bar-chart',
            style={'width': '80%', 'margin': 'auto'}
        )
    ], style={'textAlign': 'center'}),

    # Grafico 2
    html.Div([
        html.H3('Retraso de Meses Dentro del Pago del Prestamo', style={'font-weight': 'bold', 'font-size': '30px', 'textAlign': 'center'}),
        dcc.Graph(
            figure=gr1,
            style={'width': '80%', 'margin': 'auto'}
        )
    ], style={'textAlign': 'center'})
])

@app.callback(
    Output(component_id='bar-chart', component_property='figure'),
    Input(component_id='aspecto', component_property='value')
)

def update_output_grafico(aspecto):

    # Tercera consulta, interactiva

    query = """
    SELECT
        {aspecto},
        SUM(CASE WHEN default_payment_next_month = 1 THEN 1 ELSE 0 END) / CAST(COUNT(*) AS FLOAT) * 100 AS Default_Percentage,
        SUM(CASE WHEN default_payment_next_month = 0 THEN 1 ELSE 0 END) / CAST(COUNT(*) AS FLOAT) * 100 AS No_Default_Percentage
    FROM
        prodq1
    WHERE
        {aspecto} in (1,2,3,4)
    GROUP BY
        {aspecto}
    ORDER BY
        {aspecto} ASC;

    """
    query = query.format(aspecto=aspecto)
    df = sqlio.read_sql_query(query, engine)
    df

    cat = df.columns[0]

    if cat == 'education':
        x = ['Graduate School', 'University', 'High School', 'Others']
    elif cat == 'sex':
        x = ['Male', 'Female']
    elif cat == 'marriage':
        x  = ['Married', 'Single', 'Others']

    titulo = cat.capitalize()

    y1 = df['default_percentage'].tolist()
    y2 = df['no_default_percentage'].tolist()

    gr = px.bar(x=x, y=[y2, y1], barmode='group',
                # title='Porcentaje de Personas Que Cometen o No Default',
                category_orders={'x': x},
                labels = {'y0': 'No Default', 'y1':'Default'})
    gr.update_layout(
        legend={'title': '','itemsizing': 'constant', 'tracegroupgap': 0}, xaxis_title = titulo,
        yaxis_title = 'Porcentaje',
        xaxis={'showgrid': False, 'showline': False, 'showticklabels': True},
        yaxis={'showgrid': False, 'showline': False, 'showticklabels': True, 'range': [0, 100]},
        plot_bgcolor='rgba(0,0,0,0)'
    )

    gr.data[0].name = 'No Default'
    gr.data[1].name = 'Default'

    return gr



#############################################################################################################
#################################### Modelo Predictivo#######################################################
#############################################################################################################



script_dir = os.path.dirname(os.path.abspath(__file__))
modelo_dir = os.path.join(script_dir, 'modelo')
modelo_path = os.path.join(modelo_dir, 'modelo.pkl')
model = joblib.load(modelo_path)

tab2_layout = html.Div([

    ##################### GRUPO 1
    html.Div([
        html.Div([
            html.Div([
                html.Div('Seleccione a qué genero pertenece', style={'font-size':'20px', 'font-weight': 'normal', 'textAlign': 'center'}),
            ], style={'margin': '20px'}),
            html.Div([
                dcc.Dropdown(id='sexo', value='Genero', options=['Male', 'Female'], style ={'width': '450px'})
            ], style={'margin': '20px'}),
        ], style={'display': 'inline-block'}),

        html.Div([
            html.Div([
                html.Div('Seleccione un grado de educación', style={'font-size':'20px', 'font-weight': 'normal', 'textAlign': 'center'}),
            ], style={'margin': '20px'}),
            html.Div([
                dcc.Dropdown(id='educacion', value='Nivel Educativo', options=['Graduate School', 'University', 'High School', 'Others'], style ={'width': '450px'})
            ], style={'margin': '20px'}),
        ], style={'display': 'inline-block'}),

        html.Div([
            html.Div([
                html.Div('Seleccione su estado civil', style={'font-size':'20px', 'font-weight': 'normal', 'textAlign': 'center'}),
            ], style={'margin': '20px'}),
            html.Div([
                dcc.Dropdown(id='estado_civil', value='Estado Civil', options=['Married', 'Single', 'Others'], style ={'width': '450px'})
            ], style={'margin': '20px'}),
        ], style={'display': 'inline-block'}),
    ], style={'display': 'flex', 'flexDirection': 'row'}),

    ##################### GRUPO 2

    html.Div([
        html.Div([
            html.Div([
                html.Div('Ingrese su edad', style={'font-size':'20px', 'font-weight': 'normal', 'textAlign': 'center'})
            ], style={'margin': '20px'}),
            html.Div([
                dcc.Input(id='edad', type='number', placeholder='Edad', style={'width': '450px', 'height': '25px', 'borderRadius': '5px', 'borderColor': '#CCCCCC'})
            ], style={'margin': '20px'}),
        ]),
        html.Div([
            html.Div([
                html.Div('Ingrese el valor del crédito', style={'font-size':'20px', 'font-weight': 'normal', 'textAlign': 'center'})
            ], style={'margin': '20px'}),
            html.Div([
                dcc.Input(id='valor_credito', type='number', placeholder='Valor Crédito', style={'width': '450px', 'height': '25px', 'borderRadius': '5px', 'borderColor': '#CCCCCC'})
            ], style={'margin': '20px'}),
        ]),

    ], style={'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'center'}),


    ##################### GRUPO 3

    html.Div([
        html.Div('Seleccione su historial de pago de los últimos seis meses', style={'font-size':'20px', 'font-weight': 'normal', 'textAlign': 'center'})
    ]),
    html.Br(),
    html.Div([
        dcc.Dropdown(id='pay1', value='Historial de Pago',
                     options=['Pago Anticipado', 'Pago a tiempo',
                              'Pago atrasado', '1 Mes de Retraso',
                              '2 Meses de Retraso', '3 Meses de Retraso',
                              '4 Meses de Retraso', '5 Meses de Retraso',
                              '6 Meses de Retraso', '7 Meses de Retraso',
                              '8 Meses de Retraso',
                              ],
                     style={'display': 'inline-block', 'width':'190px', 'margin-right': '30px'}
                     ),
        dcc.Dropdown(id='pay2', value='Historial de Pago',
                     options=['Pago Anticipado', 'Pago a tiempo',
                              'Pago atrasado', '1 Mes de Retraso',
                              '2 Meses de Retraso', '3 Meses de Retraso',
                              '4 Meses de Retraso', '5 Meses de Retraso',
                              '6 Meses de Retraso', '7 Meses de Retraso',
                              '8 Meses de Retraso',
                              ],
                     style={'display': 'inline-block', 'width':'190px', 'margin-right': '30px'}
                     ),
        dcc.Dropdown(id='pay3', value='Historial de Pago',
                     options=['Pago Anticipado', 'Pago a tiempo',
                              'Pago atrasado', '1 Mes de Retraso',
                              '2 Meses de Retraso', '3 Meses de Retraso',
                              '4 Meses de Retraso', '5 Meses de Retraso',
                              '6 Meses de Retraso', '7 Meses de Retraso',
                              '8 Meses de Retraso',
                              ],
                     style={'display': 'inline-block', 'width':'190px', 'margin-right': '30px'}
                     ),
        dcc.Dropdown(id='pay4', value='Historial de Pago',
                     options=['Pago Anticipado', 'Pago a tiempo',
                              'Pago atrasado', '1 Mes de Retraso',
                              '2 Meses de Retraso', '3 Meses de Retraso',
                              '4 Meses de Retraso', '5 Meses de Retraso',
                              '6 Meses de Retraso', '7 Meses de Retraso',
                              '8 Meses de Retraso',
                              ],
                     style={'display': 'inline-block', 'width':'190px', 'margin-right': '30px'}
                     ),
        dcc.Dropdown(id='pay5', value='Historial de Pago',
                     options=['Pago Anticipado', 'Pago a tiempo',
                              'Pago atrasado', '1 Mes de Retraso',
                              '2 Meses de Retraso', '3 Meses de Retraso',
                              '4 Meses de Retraso', '5 Meses de Retraso',
                              '6 Meses de Retraso', '7 Meses de Retraso',
                              '8 Meses de Retraso',
                              ],
                     style={'display': 'inline-block', 'width':'190px', 'margin-right': '30px'}
                     ),
        dcc.Dropdown(id='pay6', value='Historial de Pago',
                     options=['Pago Anticipado', 'Pago a tiempo',
                              'Pago atrasado', '1 Mes de Retraso',
                              '2 Meses de Retraso', '3 Meses de Retraso',
                              '4 Meses de Retraso', '5 Meses de Retraso',
                              '6 Meses de Retraso', '7 Meses de Retraso',
                              '8 Meses de Retraso',
                              ],
                     style={'display': 'inline-block', 'width':'190px', 'margin-right': '30px'}
                     ), 
    ], style={'textAlign': 'center'}),
    html.Br(),


    ##################### GRUPO 4

    html.Div([
        html.Div('Ingrese el estado de cuenta del monto de la factura de los ultimos seis meses', style={'font-size':'20px', 'font-weight': 'normal', 'textAlign': 'center'})
    ]),
    html.Br(),
    html.Div([
        dcc.Input(id = 'bill1', type='number', placeholder='Cantidad de la Cuenta', style={'display': 'inline-block', 'width':'180px', 'margin-right': '30px', 'height': '25px', 'borderRadius': '5px', 'borderColor': '#CCCCCC'}),
        dcc.Input(id = 'bill2', type='number', placeholder='Cantidad de la Cuenta', style={'display': 'inline-block', 'width':'180px', 'margin-right': '30px', 'height': '25px', 'borderRadius': '5px', 'borderColor': '#CCCCCC'}),
        dcc.Input(id = 'bill3', type='number', placeholder='Cantidad de la Cuenta', style={'display': 'inline-block', 'width':'180px', 'margin-right': '30px', 'height': '25px', 'borderRadius': '5px', 'borderColor': '#CCCCCC'}),
        dcc.Input(id = 'bill4', type='number', placeholder='Cantidad de la Cuenta', style={'display': 'inline-block', 'width':'180px', 'margin-right': '30px', 'height': '25px', 'borderRadius': '5px', 'borderColor': '#CCCCCC'}),
        dcc.Input(id = 'bill5', type='number', placeholder='Cantidad de la Cuenta', style={'display': 'inline-block', 'width':'180px', 'margin-right': '30px', 'height': '25px', 'borderRadius': '5px', 'borderColor': '#CCCCCC'}),
        dcc.Input(id = 'bill6', type='number', placeholder='Cantidad de la Cuenta', style={'display': 'inline-block', 'width':'180px', 'margin-right': '30px', 'height': '25px', 'borderRadius': '5px', 'borderColor': '#CCCCCC'}),
    ], style={'textAlign': 'center'}),
    html.Br(),

    ##################### GRUPO 5

    html.Div([
        html.Div('Ingrese la cantidad de los pagos previos realizados en los ultimos seis meses', style={'font-size':'20px', 'font-weight': 'normal', 'textAlign': 'center'})
    ]),
    html.Br(),
    html.Div([
        dcc.Input(id = 'paya1', type='number', placeholder='Cantidad Pago Previo', style={'display': 'inline-block', 'width':'180px', 'margin-right': '30px', 'height': '25px', 'borderRadius': '5px', 'borderColor': '#CCCCCC'}),
        dcc.Input(id = 'paya2', type='number', placeholder='Cantidad Pago Previo', style={'display': 'inline-block', 'width':'180px', 'margin-right': '30px', 'height': '25px', 'borderRadius': '5px', 'borderColor': '#CCCCCC'}),
        dcc.Input(id = 'paya3', type='number', placeholder='Cantidad Pago Previo', style={'display': 'inline-block', 'width':'180px', 'margin-right': '30px', 'height': '25px', 'borderRadius': '5px', 'borderColor': '#CCCCCC'}),
        dcc.Input(id = 'paya4', type='number', placeholder='Cantidad Pago Previo', style={'display': 'inline-block', 'width':'180px', 'margin-right': '30px', 'height': '25px', 'borderRadius': '5px', 'borderColor': '#CCCCCC'}),
        dcc.Input(id = 'paya5', type='number', placeholder='Cantidad Pago Previo', style={'display': 'inline-block', 'width':'180px', 'margin-right': '30px', 'height': '25px', 'borderRadius': '5px', 'borderColor': '#CCCCCC'}),
        dcc.Input(id = 'paya6', type='number', placeholder='Cantidad Pago Previo', style={'display': 'inline-block', 'width':'180px', 'margin-right': '30px', 'height': '25px', 'borderRadius': '5px', 'borderColor': '#CCCCCC'}),
    ], style={'textAlign': 'center'}),
    html.Br(),
    html.Br(),

    html.Div(
        dcc.Graph(
            id='resultado_del_modelo'
        )
    )

])



def validar_valor(valor):
    if valor is None or valor == '':
        return None

    try:
        valor = float(valor)
    except ValueError:
        return None

    return valor

def validar_seleccion(seleccion, opciones):
    if seleccion not in opciones:
        return None

    return seleccion

@app.callback(
    Output(component_id='resultado_del_modelo', component_property= 'figure'),
    [Input(component_id='valor_credito', component_property='value'),
     Input(component_id='sexo', component_property='value'),
     Input(component_id='educacion', component_property='value'),
     Input(component_id='estado_civil', component_property='value'),
     Input(component_id='edad', component_property='value'),
     Input(component_id='pay1', component_property='value'),
     Input(component_id='pay2', component_property='value'),
     Input(component_id='pay3', component_property='value'),
     Input(component_id='pay4', component_property='value'),
     Input(component_id='pay5', component_property='value'),
     Input(component_id='pay6', component_property='value'),
     Input(component_id='bill1', component_property='value'),
     Input(component_id='bill2', component_property='value'),
     Input(component_id='bill3', component_property='value'),
     Input(component_id='bill4', component_property='value'),
     Input(component_id='bill5', component_property='value'),
     Input(component_id='bill6', component_property='value'),
     Input(component_id='paya1', component_property='value'),
     Input(component_id='paya2', component_property='value'),
     Input(component_id='paya3', component_property='value'),
     Input(component_id='paya4', component_property='value'),
     Input(component_id='paya5', component_property='value'),
     Input(component_id='paya6', component_property='value')]
)
def resultados_modelo(valor_credito, sexo, educacion, estado_civil,edad,
                      pay1,pay2,pay3,pay4,pay5,pay6,bill1,bill2,bill3,
                      bill4,bill5,bill6,paya1,paya2,paya3,paya4,paya5,paya6):
    
    valor_credito = validar_valor(valor_credito)
    edad = validar_valor(edad)
    bill1 = validar_valor(bill1)
    bill2 = validar_valor(bill2)
    bill3 = validar_valor(bill3)
    bill4 = validar_valor(bill4)
    bill5 = validar_valor(bill5)
    bill6 = validar_valor(bill6)
    paya1 = validar_valor(paya1)
    paya2 = validar_valor(paya2)
    paya3 = validar_valor(paya3)
    paya4 = validar_valor(paya4)
    paya5 = validar_valor(paya5)
    paya6 = validar_valor(paya6)

    opciones_sexo = ['Male', 'Female']
    opciones_educacion = ['Graduate School', 'University', 'High School', 'Others']
    opciones_estado_civil = ['Married', 'Single', 'Others']
    opciones_hist_pagos = ['Pago Anticipado', 'Pago a tiempo', 'Pago atrasado', 
                           '1 Mes de Retraso', '2 Meses de Retraso', '3 Meses de Retraso',
                           '4 Meses de Retraso', '5 Meses de Retraso', '6 Meses de Retraso',
                           '7 Meses de Retraso', '8 Meses de Retraso']

    sexo = validar_seleccion(sexo, opciones_sexo)
    educacion = validar_seleccion(educacion, opciones_educacion)
    estado_civil = validar_seleccion(estado_civil, opciones_estado_civil)
    pay1 = validar_seleccion(pay1, opciones_hist_pagos)
    pay2 = validar_seleccion(pay2, opciones_hist_pagos)
    pay3 = validar_seleccion(pay3, opciones_hist_pagos)
    pay4 = validar_seleccion(pay4, opciones_hist_pagos)
    pay5 = validar_seleccion(pay5, opciones_hist_pagos)
    pay6 = validar_seleccion(pay6, opciones_hist_pagos)

    if None in (valor_credito, sexo, educacion, estado_civil, edad, 
                pay6, pay5, pay4, pay3, pay2, pay1,
                bill6, bill5, bill4, bill3, bill2, bill1,
                paya6, paya5, paya4, paya3, paya2, paya1):
        string = "Por favor, ingrese valores válidos en todos los campos."
        fig = px.scatter()
        fig.update_layout(
            showlegend=False,
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            annotations=[
                dict(
                    x=0.5,
                    y=0.5,
                    xref="paper",
                    yref="paper",
                    text=string,
                    font=dict(size=50, color='black', family='Jomolhari'),
                    showarrow=False,
                )
            ],
            plot_bgcolor='white',
            margin = dict(t=0, b=10, l=10, r=10),
            height = 130
        )


        
        return fig

    generos =  {'Male': 1, 'Female': 2}
    grados = {'Graduate School': 1, 'University': 2, 'High School': 3,'Others':4}
    estados = {'Married':1, 'Single': 2, 'Others': 3}
    hist_pagos = {'Pago Anticipado': -2, 'Pago a tiempo': -1, 'Pago atrasado': 0,
                  '1 Mes de Retraso': 1,'2 Meses de Retraso': 2, '3 Meses de Retraso': 3,
                  '4 Meses de Retraso': 4, '5 Meses de Retraso': 5,'6 Meses de Retraso': 6,
                  '7 Meses de Retraso': 7, '8 Meses de Retraso': 8,}
    
    sexo = generos[sexo]
    educacion = grados[educacion]
    estado_civil = estados[estado_civil]
    pay1 = hist_pagos[pay1]
    pay2 = hist_pagos[pay2]
    pay3 = hist_pagos[pay3]
    pay4 = hist_pagos[pay4]
    pay5 = hist_pagos[pay5]
    pay6 = hist_pagos[pay6]

    Xnew = [[valor_credito, sexo, educacion, estado_civil,edad,
                      pay1,pay2,pay3,pay4,pay5,pay6,bill1,bill2,bill3,
                      bill4,bill5,bill6,paya1,paya2,paya3,paya4,paya5,paya6]]
    
    ypred = model.predict(Xnew)  
    prediccion = ypred[0]
    prediccion = int(prediccion)
    if prediccion == 0:
        string = 'No Default'
        background_color = 'blue'
    elif prediccion == 1:
        string = 'Default'
        background_color = 'red'

    fig = px.scatter()
    fig.update_layout(
        showlegend=False,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        annotations=[
            dict(
                x=0.5,
                y=0.5,
                xref="paper",
                yref="paper",
                text=string,
                font=dict(size=70, color='black', family='Jomolhari'),
                showarrow=False,
            )
        ],
        plot_bgcolor=background_color,
        margin = dict(t=0, b=10, l=10, r=10),
        height = 130
    )


    return fig




app.layout = html.Div(children=[
    html.H1(children='Analisis Area de Riesgo', style=titulo_style),

    dcc.Tabs(id='tabs', value='tab1', style= tab_style, children=[
        dcc.Tab(label='Analisis Descriptivo', value = 'tab1', children= [tab1_layout]),
        dcc.Tab(label='Modelo Predictivo', value = 'tab2', children=[tab2_layout])
    ]),
])


if __name__ == '__main__':
    app.run_server(debug=True, port=8040)




