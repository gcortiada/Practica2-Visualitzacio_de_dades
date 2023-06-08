# Importem les llibreries necessaries.
import pandas as pd
import dash
from dash import dcc
from dash import html
import plotly.graph_objs as go
import os
import numpy as np

# Get current directory.
#current_directory = os.getcwd()


# Llegim les dades preprocessades.
#df = pd.read_csv(os.path.join(current_directory, 'DespesaCentresEducatiusConcertatsCatalunya_Preprocessed.csv'), sep = ",")
df = pd.read_csv('./DespesaCentresEducatiusConcertatsCatalunya_Preprocessed.csv', sep = ",")

# Llegim el dataset convertint algunes columnes a rows.
#df_melted = pd.read_csv(os.path.join(current_directory, 'DespesaCentresEducatiusConcertatsCatalunya_Preprocessed_Melted.csv'), sep = ",")
df_melted = pd.read_csv('./DespesaCentresEducatiusConcertatsCatalunya_Preprocessed_Melted.csv', sep = ",")


# Duem a terme la iniciació de la aplicació Dash.
app = dash.Dash(__name__)




# LAYOUT.
# Configurem el layout de la pàgina web.
app.layout = html.Div(children=[
    html.H1('Anàlisi sobre els Centres Educatius Concertats (2017-2022)', style = {'text-align': 'center'}),
    html.Div('Entenem els Centres Educatius Concertats de Catalunya a partir de l\'anàlisi del nombre de professors, despeses, nòmines i comarques on hi ha més Centres Educatius Concertats, al llarg dels últims anys.'),
    html.Br(),
    html.Div(['Dataset Principal amb la informació de cada Centre Educatiu Concertat de Catalunya:']), 
    html.A('Dataset Principal', href = 'https://analisi.transparenciacatalunya.cat/Educaci-/Concerts-educatius-Unitat-alumnes-dotaci-de-planti/8spq-9nx7'),
    html.Div('Generalitat de Catalunya. Departament d’Educació. Dades Obertes Catalunya, Concerts educatius: Unitat, alumnes, dotació de plantilla i despesa (Darrere Actualització: 6 de març de 2023).'),
    html.Br(),
    html.Div(['Dataset Principal amb la informació de cada Centre Educatiu Concertat de Catalunya:']), 
    html.A('Dataset Secundari', href = 'https://analisi.transparenciacatalunya.cat/Sector-P-blic/Dades-generals-dels-ens-locals-de-Catalunya/6nei-4b44'),
    html.Div('Generalitat de Catalunya. Departament de Presidència. Dades Obertes Catalunya, Dades generals dels ens local de Catalunya (Darrere Actualització: 11 de maig de 2023).'),
    html.Br(),
    html.A('Llicència oberta de les dades.', href = 'https://governobert.gencat.cat/ca/dades_obertes/llicencia-oberta-informacio-catalunya/'),
    html.H2('Evolució del nombre de professors de cada Centre Educatiu Concertat a Catalunya.'),
    html.H4('Selecció del Curs Escolar:'),
    dcc.Dropdown(
        id = 'seleccio_any',
        options = [{'label': year, 'value': year} for year in df['Curs escolar'].unique()],
        value = df['Curs escolar'].max(),
        clearable = False
    ),
    dcc.Graph(id = 'plot_nombre_professors'),
    dcc.Graph(id = 'plot_evolucio_nombre_professors'),
    html.H2('Evolució de les despeses segons la selecció efectuada.'),
    html.H4('Selecció entre Municipi, Comarca o Provincia:'),
    dcc.Dropdown(
        id = 'filtrar_municipi_comarca_provincia',
        options = [
            {'label': 'Municipi', 'value': 'MUNICIPI'},
            {'label': 'Comarca', 'value': 'COMARCA'},
            {'label': 'Provincia', 'value': 'PROVINCIA'}
        ],
        value = 'MUNICIPI',
        clearable = False
    ),
    dcc.Graph(id = 'plot_despeses'),
    dcc.Graph(id = 'plot_despeses_cens'),
    html.H2('Top Comarques/Provincies amb més Centres Educatius Concertats.'),
    html.H4('Selecció entre Comarca o Provincia:'),
    dcc.Dropdown(
        id = 'seleccio_comarca_provincia',
        options = [
            {'label': 'Comarca', 'value': 'COMARCA'},
            {'label': 'Provincia', 'value': 'PROVINCIA'}
        ],
        value = 'COMARCA',
        clearable = False
    ),
    dcc.Graph(id = 'plot_top_centres_educatius_concertats'),
    html.H2('En quin Centre Educatiu Concertat cobren més els professors?'),
    html.H4('Selecció entre Centre, Comarca o Provincia:'),
    dcc.Dropdown(
        id = 'seleccio_centre_comarca_municipi',
        options = [
	    {'label': 'Centre', 'value': 'Nom_centre'},
            {'label': 'Comarca', 'value': 'COMARCA'},
            {'label': 'Provincia', 'value': 'PROVINCIA'}
        ],
        value = 'Nom_centre',
        clearable = False
    ),
    dcc.Graph(id = 'plot_top_nomines_professors'),
    html.Div([
        html.Label('Buscar:'),
        dcc.Input(id = 'buscar_nom_centre', type = 'text', value = 'Fax', debounce = True)
    ]),
    html.Div(id = 'filtrar_centre_educatiu'),
    html.H2('Quin es el nombre d\'alumnes que cursen Batxillerat, ESO i Primaria a un Centre Educatiu Concertat per Comarca?'),
    dcc.Graph(id = 'histogram_alumnes_comarca')
])





# CALLBACKs
# Definim la funció callback per representar l'evolució del nombre de professors de cada Centr Educatiu Concertat.
@app.callback(
    dash.dependencies.Output('plot_nombre_professors', 'figure'),
    [dash.dependencies.Input('seleccio_any', 'value')]
)
def plot_nombre_professors(selected_year):
    # Filtrem les dades per any.
    filtered_data = df[df['Curs escolar'] == selected_year]

    # Ordenem 
    sorted_data = filtered_data.sort_values('Dotació plantilla', ascending = False) 

    data = []

    # Obtenim les dades a visualitzar.
    for center in sorted_data['Nom_centre'].unique():
        data.append(
            go.Bar(
                x = [center],
                y = sorted_data[sorted_data['Nom_centre'] == center]['Dotació plantilla'],
                name = center
            )
        )

    # Definim el layout del gràfic.
    layout = go.Layout(
        title = 'Evolució del Nombre de Professors per cada Centre Educatiu Concertat',
        yaxis = dict(title = 'Nombre de Professors'),
        barmode = 'group'
    )

    # Retornem les dades i el layout.
    return {'data': data, 'layout': layout}


# Definim la funció callback de l'evolució del nombre de professors al llarg dels últims cursos.
@app.callback(
    dash.dependencies.Output('plot_evolucio_nombre_professors', 'figure'),
    [dash.dependencies.Input('plot_nombre_professors', 'clickData')]
)
def plot_evolucio_nombre_professors(clickData):
    # Es revisa si el clickData es None.
    if clickData is None:
        # Si es None, es retorna el plot esta en blanc.
        return go.Figure()

    # Sino, es selecciona el punt (centre) seleccionat en el gràfic anterior.
    selected_centre = clickData['points'][0]['x']

    # S'obtenen les dades del centre seleccionat.
    selected_data = df[df['Nom_centre'] == selected_centre][0:5]

    # Obtenim les dades en forma de Scatterplot.
    data = go.Scatter(
        x = selected_data['Curs escolar'],
        y = selected_data['Dotació plantilla'],
        mode = 'lines+markers',
        name = selected_centre
    )
    
    # Obtenim el layout del gràfic.
    layout = go.Layout(
        title = f'Evolució del Nombre de Professors pel Centre: {selected_centre}',
        xaxis = dict(title = 'Curs escolar'),
        yaxis = dict(title = 'Nombre de Professors', range = [0, max(df['Dotació plantilla'])])
    )
    
    # Retornem les dades i el layout.
    return {'data': [data], 'layout': layout}



# Definim la funció callback del gràfic de despeses.
@app.callback(
    dash.dependencies.Output('plot_despeses', 'figure'),
    [dash.dependencies.Input('seleccio_any', 'value'), dash.dependencies.Input('filtrar_municipi_comarca_provincia', 'value')]
)
def plot_despeses(selected_year, filter_value):
    # Filtrem per any seleccionat.
    filtered_data_year = df_melted[df_melted['Curs escolar'] == selected_year]

    # Filtrem per Municipi, Comarca o Provincia seleccionada.
    filtered_data = filtered_data_year[filtered_data_year['variable'] == filter_value]
    
    # Calculem el total de despeses.
    filtered_data['Total Despeses'] = filtered_data['Nòmina del personal del centre'] + filtered_data['Seg.Social'] + filtered_data['Despeses de funcionament']

    # Agrupem les variables per calcular la suma de Municipi, Comarca o Provincia.
    filtered_data_despeses = filtered_data.groupby(['variable', 'value'])['Total Despeses'].sum().reset_index()

    # Ordenem les dades.
    sorted_data = filtered_data_despeses.sort_values('Total Despeses', ascending=False)
    
    data = []
    
    # Obtenim les dades de despeses ordenades en forma de gràfic de Barres.
    for municipi in sorted_data['value']:
        data.append(
            go.Bar(
                x = [municipi],
                y = sorted_data[sorted_data['value'] == municipi]['Total Despeses'],
                name = municipi
            )
        )
    
    # Obtenim el layout del gràfic.
    layout = go.Layout(
        title = 'Despeses per Centre Educatiu Concertat (en funció de la Selecció de Municipi, comarca o Provincia).',
        yaxis = dict(title = 'Despeses'),
        barmode = 'group'
    )
    
    # Retornem les dades i el layout.
    return {'data': data, 'layout': layout}



# Definim la funció callback pel gràfic de despeses per Cens.
@app.callback(
    dash.dependencies.Output('plot_despeses_cens', 'figure'),
    [dash.dependencies.Input('seleccio_any', 'value'), dash.dependencies.Input('filtrar_municipi_comarca_provincia', 'value')]
)
def plot_despeses_per_cens(selected_year, filter_value):
    # Filtrem per any seleccionat.
    filtered_data_year = df_melted[df_melted['Curs escolar'] == selected_year]

    # Filtrem per Municipi, Comarca o Provincia seleccionada.
    filtered_data = filtered_data_year[filtered_data_year['variable'] == filter_value]
    
    # Calculem el total de despeses.
    filtered_data['Total Despeses'] = filtered_data['Nòmina del personal del centre'] + filtered_data['Seg.Social'] + filtered_data['Despeses de funcionament']

    # Obtenim l'agrupació del 'CENS'.
    filtered_data_cens = filtered_data.groupby(['variable', 'value'])['CENS'].sum().reset_index()

    # Agrupem les variables per calcular la suma de Municipi, Comarca o Provincia.
    filtered_data_despeses = filtered_data.groupby(['variable', 'value'])['Total Despeses'].sum().reset_index()

    # Obtenim la proporció de Despeses x Cens.
    filtered_data_despeses['Proporcio Despeses Cens'] = filtered_data_despeses['Total Despeses']/filtered_data_cens['CENS']

    # Ordenem les dades.
    sorted_data = filtered_data_despeses.sort_values('Proporcio Despeses Cens', ascending = False)
    
    data = []

    # Obtenim les dades de despeses per Cens ordenades.
    for municipi in sorted_data['value']:
        data.append(
            go.Bar(
                x = [municipi],
                y = sorted_data[sorted_data['value'] == municipi]['Proporcio Despeses Cens'],
                name = municipi
            )
        )

    # Obtenim el layout del gràfic.
    layout = go.Layout(
        title = 'Proporció de Despeses per Centre Educatiu Concertat (en funció del Cens de cada població i la selecció de Municipi, Comarca o Provincia)',
        yaxis = dict(title = 'Despeses'),
        barmode = 'group'
    )
    
    # Retornem les dades i el layout.
    return {'data': data, 'layout': layout}



# Definim la funció callback pel grafic de Comarques/Provincies amb més Centres Educatius Concertats.
@app.callback(
    dash.dependencies.Output('plot_top_centres_educatius_concertats', 'figure'),
    [dash.dependencies.Input('seleccio_any', 'value'), dash.dependencies.Input('seleccio_comarca_provincia', 'value')]
)
def plot_comarques_amb_mes_centres(selected_year, filter_value):
    # Filtrem per any seleccionat.
    filtered_data_year = df[df['Curs escolar'] == selected_year]
    
    # Agrupem les dades per Comarca/Provincia (la selecció), i duem a terme un count.
    grouped_data = filtered_data_year.groupby(filter_value).size().reset_index(name = 'Count')
    
    # Ordenem les dades ordenades.
    sorted_data = grouped_data.sort_values('Count', ascending = False)

    # Obtenim les dades.
    data = [
        go.Bar(
            x = sorted_data[filter_value],
            y = sorted_data['Count']
        )
    ]
    
    # Obtenim el Layout.
    layout = go.Layout(
        title = f'Centres Eductaius Concertats per {filter_value}',
        yaxis = dict(title = 'Número de Centres educatius Concertats.')
    )
    
    # Retornem les dades i el layout.
    return {'data': data, 'layout': layout}


# Definim la funció callback pel grafic de en quin centre cobren més els professors.
@app.callback(
    dash.dependencies.Output('plot_top_nomines_professors', 'figure'),
    [dash.dependencies.Input('seleccio_any', 'value'), dash.dependencies.Input('seleccio_centre_comarca_municipi', 'value')]
)
def plot_nomines_professors(selected_year, filter_value):
    # Filtrem per any seleccionat.
    filtered_data_year = df[df['Curs escolar'] == selected_year]
    
    # Agrupem les dades per Comarca/Provincia (la selecció), i duem a terme un count.
    grouped_data = filtered_data_year.groupby(filter_value).sum().reset_index()
    
    # Obtenim la 'Nomina x Professor'.
    grouped_data['Nomina x Professor'] = grouped_data['Nòmina del personal del centre']/grouped_data['Dotació plantilla']

    # Ordenem les dades ordenades.
    sorted_data = grouped_data.sort_values('Nomina x Professor', ascending = False)

    # Obtenim les dades.
    data = [
        go.Bar(
            x = sorted_data[filter_value],
            y = sorted_data['Nomina x Professor']
        )
    ]
    
    # Obtenim el Layout.
    layout = go.Layout(
        title = f'Nòmines dels Professors per {filter_value}',
        yaxis = dict(title = 'Nòmines dels Professors')
    )
    
    # Retornem les dades i el layout.
    return {'data': data, 'layout': layout}


# Definim la funció de callback que ens permetra filtrar pel Centre Educatiu Concertat.
@app.callback(
    dash.dependencies.Output('filtrar_centre_educatiu', 'children'),
    [dash.dependencies.Input('seleccio_any', 'value'), dash.dependencies.Input('seleccio_centre_comarca_municipi', 'value'), dash.dependencies.Input('buscar_nom_centre', 'value')]
)
def update_graph_value(selected_year, filter_value, search_value):
    # Filtrem per any seleccionat.
    filtered_data_year = df[df['Curs escolar'] == selected_year]
    
    # Agrupem les dades per Comarca/Provincia (la selecció), i duem a terme un count.
    grouped_data = filtered_data_year.groupby(filter_value).sum().reset_index()
    
    # Obtenim la 'Nomina x Professor'.
    grouped_data['Nomina x Professor'] = grouped_data['Nòmina del personal del centre']/grouped_data['Dotació plantilla']

    # Definim un try.
    try:
	# Obtenim el valor de 'Nomina x Professor' del valor buscat.
        valor_ = list(grouped_data[grouped_data[filter_value] == search_value]['Nomina x Professor'])[0]

        valor = f"Nòmina Mitjana dels Professors a '{search_value}': {valor_}"
    # Si obtenim un error.
    except:
        # Retornem que no hem pogut obtenir el valor.
        valor = "No s'ha trobat el valor."

    # Retornem el valor obtingut.
    return valor


# Definim una funció callback que ens permeti comparar alumnes cursant Batxillerat, ESO i Primaria.
@app.callback(
    dash.dependencies.Output('histogram_alumnes_comarca', 'figure'),
    [dash.dependencies.Input('seleccio_any', 'value')]
)
def plot_alumnes_comarca_histogram(selected_year):
    # Filtrem les dades per any.
    filtered_data = df[(df['Curs escolar'] == selected_year)]
    
    # Obtenim els valors per cada Comarca, sumant els valors d'Alumnes.
    df_sum = filtered_data.groupby('COMARCA')['Alumnes - BATX', 'Alumnes - PRI', 'Alumnes - ESO'].sum().reset_index()

    # Creem el llistat de dades.
    data_list = list()

    # S'iteren totes les columnes necessaries.
    for column in ['Alumnes - BATX', 'Alumnes - PRI', 'Alumnes - ESO']:
        # Es preparen les dades per tal d'obtenir el gràfioc de barres.
        data = go.Bar(
                x = list(df_sum['COMARCA']),
                y = list(df_sum[column]),
                name = column,
                opacity = 0.75
            )
        # Afegim data al llistat.
        data_list.append(data)

    # Definim el Layout pel gràfic de barres.
    layout = go.Layout(
        barmode = 'stack',
        title = 'Gràfic de Barres d\'Alumnes per Comarca (en funció de Primària, ESO o Batxillerat).',
        xaxis = dict(title = 'Comarca'),
        yaxis = dict(title = 'Alumnes')
    )

    # Retornem les dades i el layout.
    return {'data': data_list, 'layout': layout}

'''
# Definim una funció callback per tal de comparar alumnes cursant Batxillerat, ESO i Primaria amb un Heatmap.
@app.callback(
    dash.dependencies.Output('heatmap_alumnes_comarca', 'figure'),
    [dash.dependencies.Input('seleccio_any', 'value')]
)
def plot_alumnes_comarca_heatmap(selected_year):
    # Filtrem les dades per any.
    filtered_data = df[(df['Curs escolar'] == selected_year)]
    
    # Obtenim els valors per cada Comarca, sumant els valors d'Alumnes.
    df_sum = filtered_data.groupby('COMARCA')['Alumnes - BATX', 'Alumnes - PRI', 'Alumnes - ESO'].sum().reset_index()

    # Se obtienen los valores de las columnas que queremos.
    valores = list(df_sum[['Alumnes - BATX', 'Alumnes - PRI', 'Alumnes - ESO']].values)

    # Es preparen les dades per tal d'obtenir el Heatmap.
    data = go.Heatmap(
            x = list(df_sum['COMARCA']),
            y = ['Alumnes - BATX', 'Alumnes - PRI', 'Alumnes - ESO'],
            z = valores,
            colorscale = 'Viridis'
        )

    # Definim el Layout del Heatmap.
    layout = go.Layout(
        barmode = 'stack',
        title = 'Heatmap d\'Alumnes per Comarca (en funció de Primària, ESO o Batxillerat).',
        xaxis = dict(title = 'Comarca'),
        yaxis = dict(title = 'Alumnes')
    )

    # Retornem les dades i el layout.
    return {'data': [data], 'layout': layout}
'''


# Si es el main.
if __name__ == '__main__':
    # Inicia l'execució de l'aplicació.
    app.run_server(debug = True)











