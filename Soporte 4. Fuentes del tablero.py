import dash
from dash import dcc  # dash core components
from dash import html # dash html components
from dash.dependencies import Input, Output
import psycopg2
from dotenv import load_dotenv # pip install python-dotenv
import os
import psycopg2
import pandas.io.sql as sqlio
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

env_path="C:\\Users\\gutil\\OneDrive - Universidad de los andes\\Escritorio\\Ingenieria Industrial\\2024-01\\Analitica Computacional Para la Toma de Decisiones\\Proyecto\\Proyecto 2\\env\\app.env"

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


tab2_layout = html.Div([

    ]
)


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

app.layout = html.Div(children=[
    html.H1(children='Analisis Area de Riesgo', style=titulo_style),

    dcc.Tabs(id='tabs', value='tab1', style= tab_style, children=[
        dcc.Tab(label='Analisis Descriptivo', value = 'tab1', children= [tab1_layout]),
        dcc.Tab(label='Modelo Predictivo', value = 'tab2', children=[tab2_layout])
    ]),
])



if __name__ == '__main__':
    app.run_server(debug=True, port=8040)


