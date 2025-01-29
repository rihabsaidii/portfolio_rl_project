# import os
# import json
# import numpy as np
# import pandas as pd
# import dash
# import dash_bootstrap_components as dbc
# from dash import dcc, html, Input, Output
# import plotly.express as px
# import plotly.graph_objects as go
# # from waitress import serve
#
# # Paths and Data Loading
# DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '', 'data'))
#
# # Load optimal weights
# optimal_weights_path = os.path.join(DATA_DIR, 'optimal_weights.json')
# if os.path.exists(optimal_weights_path):
#     with open(optimal_weights_path, 'r') as f:
#         optimal_weights = json.load(f)
# else:
#     raise FileNotFoundError(f"Le fichier {optimal_weights_path} est introuvable.")
#
# # Load prices data
# prices_path = os.path.join(DATA_DIR, 'prices.csv')
# if os.path.exists(prices_path):
#     prices_df = pd.read_csv(prices_path)
#     print("Fichier prices.csv chargé avec succès !")
# else:
#     raise FileNotFoundError(f"Le fichier {prices_path} est introuvable.")
#
# # Load returns data
# returns_path = os.path.join(DATA_DIR, 'returns.csv')
# if os.path.exists(returns_path):
#     returns_df = pd.read_csv(returns_path)
#     print("Fichier returns.csv chargé avec succès !")
# else:
#     raise FileNotFoundError(f"Le fichier {returns_path} est introuvable.")
#
# returns_numeric = returns_df.drop(columns=['Date'])
#
# # Available combinations
# available_combinations = list(optimal_weights.keys())
#
# # Initialize Dash App
# app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
# # Accès au serveur Flask sous-jacent
# server = app.server  # Cela permet à Gunicorn d'accéder au serveur WSGI.
#
# # Navbar
# navbar = dbc.Navbar(
#     id='navbar',
#     children=[
#         dbc.Row(
#             children=[
#                 dbc.Col(
#                     dbc.NavbarBrand(
#                         "Portfolio Optimization",
#                         style={
#                             'color': 'white',
#                             'fontSize': '30px',
#                             'fontFamily': 'Arial',
#                             'margin-left': '15px',
#                             'fontWeight': 'bold'
#                         }
#                     )
#                 )
#             ],
#             align="center",
#             justify="center"
#         )
#     ],
#     color='#01080b',
#     dark=True,
#     fixed="top"
# )
#
# # Dropdown Card
# card_content_dropdown = dbc.CardBody([
#     html.H6('', style={'textAlign': 'center'}),
#     dbc.Row([
#         dbc.Col([
#             html.H6('Stocks'),
#             dcc.Dropdown(
#                 id='stocks-dropdown',
#                 options=[
#                     {'label': 'AAPL', 'value': 'AAPL'},
#                     {'label': 'PG', 'value': 'PG'},
#                     {'label': 'XOM', 'value': 'XOM'}
#                 ],
#                 value=["AAPL", "PG", "XOM"],
#                 multi=True
#             ),
#         ])
#     ])
# ])
#
# # Labels and Colors for Pie Chart
# labels = ["AAPL", "PG", "XOM"]
# colors = ['#ff9999', '#66b3ff', '#99ff99']
#
# # App Layout
# body_app = dbc.Container([
#     html.Br(),
#     html.Br(),
#
#     # Metrics and Dropdown
#     dbc.Row([
#         dbc.Col([dbc.Card(card_content_dropdown, style={'height': '150px'})], width=4),
#         dbc.Col([dbc.Card([dbc.CardBody([
#             html.H6('Expected Performance', style={'fontWeight': 'lighter', 'textAlign': 'center'}),
#             html.H3(id='expected-return', style={'color': 'rgb(64 165 193)', 'textAlign': 'center'})
#         ])], style={'height': '150px'})]),
#         dbc.Col([dbc.Card([dbc.CardBody([
#             html.H6('Sharpe Ratio', style={'fontWeight': 'lighter', 'textAlign': 'center'}),
#             html.H3(id='sharpe-ratio', style={'color': 'rgb(64 165 193)', 'textAlign': 'center'})
#         ])], style={'height': '150px'})]),
#         dbc.Col([dbc.Card([dbc.CardBody([
#             html.H6('VaR', style={'fontWeight': 'lighter', 'textAlign': 'center'}),
#             html.H3(id='var-value', style={'color': 'rgb(64 165 193)', 'textAlign': 'center'})
#         ])], style={'height': '150px'})])
#     ]),
#
#     html.Br(),
#     html.Br(),
#
#     # Graphs
#     dbc.Row([
#         dbc.Col([dbc.Card([dcc.Graph(id='pie-chart')])]),
#         dbc.Col([dbc.Card([dcc.Graph(id='stock-returns-graph')])])
#     ])
# ])
#
# app.layout = html.Div(id='parent', children=[navbar, body_app], style={'margin': '30px'})
#
# # Callbacks
# @app.callback(
#     Output('stock-returns-graph', 'figure'),
#     Input('stocks-dropdown', 'value')
# )
# def update_graph(selected_stocks):
#     if not selected_stocks:
#         return px.line(title="Veuillez sélectionner au moins une action.")
#
#     filtered_df = prices_df[['Date'] + selected_stocks]
#     custom_colors = {
#         'AAPL': {'line': 'rgba(255, 99, 71)', 'fill': 'rgba(255, 99, 71)'},  # Tomate
#         'XOM': {'line': 'rgba(50, 205, 50)', 'fill': 'rgba(50, 205, 50)'},  # Lime
#         'PG': {'line': 'rgba(30, 144, 255)', 'fill': 'rgba(30, 144, 255)'},  # Dodger Blue
#     }
#
#     fig = go.Figure()
#     for stock in selected_stocks:
#         fig.add_trace(go.Scatter(
#             x=filtered_df['Date'],
#             y=filtered_df[stock],
#             mode='lines',
#             name=stock,
#             fill='tozeroy',
#             fillcolor=custom_colors[stock]['fill'],
#             line=dict(color=custom_colors[stock]['line'])
#         ))
#
#     fig.update_layout(
#         title="Historical Prices",
#         xaxis_title='Date',
#         yaxis_title='Price',
#         template='plotly'
#     )
#     return fig
#
# @app.callback(
#     Output('pie-chart', 'figure'),
#     Input('stocks-dropdown', 'value')
# )
# def display_pie_chart(selected_stocks):
#     selected_stocks_sorted = sorted(selected_stocks)
#     selected_combination_str = ','.join(selected_stocks_sorted)
#
#     if selected_combination_str in optimal_weights:
#         weights = optimal_weights[selected_combination_str]
#         return px.pie(names=selected_stocks_sorted, values=weights, title='Optimal weights')
#
#     return px.pie(names=['Aucune sélection'], values=[1], title='Veuillez sélectionner une combinaison valide')
#
# @app.callback(
#     [Output('expected-return', 'children'),
#      Output('sharpe-ratio', 'children'),
#      Output('var-value', 'children')],
#     Input('stocks-dropdown', 'value')
# )
# def calculate_metrics(selected_stocks):
#     if not selected_stocks:
#         return "Aucune sélection", "Aucune sélection", "Aucune sélection"
#
#     selected_stocks_sorted = ','.join(sorted(selected_stocks))
#
#     if selected_stocks_sorted not in optimal_weights:
#         return "Pas de poids disponibles", "Pas de poids disponibles", "Pas de poids disponibles"
#
#     weights = np.array(optimal_weights[selected_stocks_sorted])
#     df = pd.DataFrame({stock: returns_df[stock] for stock in selected_stocks})
#     mean_returns = df.mean()
#     cov_matrix = df.cov()
#
#     expected_return = np.dot(weights, mean_returns)
#     portfolio_std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
#     risk_free_rate = 0.01
#     sharpe_ratio = (expected_return - risk_free_rate) / portfolio_std
#
#     portfolio_returns = df.dot(weights)
#     historical_var = np.percentile(portfolio_returns, 5)
#
#     return (
#         f"{expected_return:.2%}",
#         f"{sharpe_ratio:.2f}",
#         f"{historical_var:.2%}"
#     )
#
# if __name__ == '__main__':
#     app.run_server(debug=True)
#     # serve(app.server, host="0.0.0.0", port=8050)

# import os
# import json
# import dash_bootstrap_components as dbc
# from dash import dcc, html, Input, Output, Dash
# import plotly.graph_objects as go
#
#
# # Paths and Data Loading
# DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '', 'data'))
#
# # Load optimal weights
# optimal_weights_path = os.path.join(DATA_DIR, 'optimal_weights.json')
# if os.path.exists(optimal_weights_path):
#     with open(optimal_weights_path, 'r') as f:
#         optimal_weights = json.load(f)
# else:
#     raise FileNotFoundError(f"Le fichier {optimal_weights_path} est introuvable.")
#
# # Load prices data
# prices_path = os.path.join(DATA_DIR, 'prices.csv')
# if os.path.exists(prices_path):
#     with open(prices_path, 'r') as f:
#         prices = f.readlines()
#     print("Fichier prices.csv chargé avec succès !")
# else:
#     raise FileNotFoundError(f"Le fichier {prices_path} est introuvable.")
#
# # Load returns data
# returns_path = os.path.join(DATA_DIR, 'returns.csv')
# if os.path.exists(returns_path):
#     with open(returns_path, 'r') as f:
#         returns = f.readlines()
#     print("Fichier returns.csv chargé avec succès !")
# else:
#     raise FileNotFoundError(f"Le fichier {returns_path} est introuvable.")
#
#
# # Process prices and returns into lists of dictionaries
# # Assuming CSV structure like "Date, AAPL, PG, XOM"
# def process_csv_data(csv_lines):
#     header = csv_lines[0].strip().split(',')
#     data = []
#     for line in csv_lines[1:]:
#         values = line.strip().split(',')
#         data.append(dict(zip(header, values)))
#     return data
#
#
# prices_data = process_csv_data(prices)
# returns_data = process_csv_data(returns)
#
# # Available combinations
# available_combinations = list(optimal_weights.keys())
# class CallableDash(Dash):
#     def __call__(self, environ, start_response):
#         return self.server(environ, start_response)
# # Initialize Dash App
# app = CallableDash(external_stylesheets=[dbc.themes.BOOTSTRAP])
# print("L'objet app a __call__ ? :", hasattr(app, "__call__"))
#
#
# # Navbar
# navbar = dbc.Navbar(
#     id='navbar',
#     children=[
#         dbc.Row(
#             children=[
#                 dbc.Col(
#                     dbc.NavbarBrand(
#                         "Portfolio Optimization",
#                         style={
#                             'color': 'white',
#                             'fontSize': '30px',
#                             'fontFamily': 'Arial',
#                             'margin-left': '15px',
#                             'fontWeight': 'bold'
#                         }
#                     )
#                 )
#             ],
#             align="center",
#             justify="center"
#         )
#     ],
#     color='#01080b',
#     dark=True,
#     fixed="top"
# )
#
# # Dropdown Card
# card_content_dropdown = dbc.CardBody([
#     html.H6('', style={'textAlign': 'center'}),
#     dbc.Row([
#         dbc.Col([
#             html.H6('Stocks'),
#             dcc.Dropdown(
#                 id='stocks-dropdown',
#                 options=[
#                     {'label': 'AAPL', 'value': 'AAPL'},
#                     {'label': 'PG', 'value': 'PG'},
#                     {'label': 'XOM', 'value': 'XOM'}
#                 ],
#                 value=["AAPL", "PG", "XOM"],
#                 multi=True
#             ),
#         ])
#     ])
# ])
#
# # Labels and Colors for Pie Chart
# labels = ["AAPL", "PG", "XOM"]
# colors = ['#ff9999', '#66b3ff', '#99ff99']
#
# # App Layout
# body_app = dbc.Container([
#     html.Br(),
#     html.Br(),
#
#     # Metrics and Dropdown
#     dbc.Row([
#         dbc.Col([dbc.Card(card_content_dropdown, style={'height': '150px'})], width=4),
#         dbc.Col([dbc.Card([dbc.CardBody([
#             html.H6('Expected Performance', style={'fontWeight': 'lighter', 'textAlign': 'center'}),
#             html.H3(id='expected-return', style={'color': 'rgb(64 165 193)', 'textAlign': 'center'})
#         ])], style={'height': '150px'})]),
#         dbc.Col([dbc.Card([dbc.CardBody([
#             html.H6('Sharpe Ratio', style={'fontWeight': 'lighter', 'textAlign': 'center'}),
#             html.H3(id='sharpe-ratio', style={'color': 'rgb(64 165 193)', 'textAlign': 'center'})
#         ])], style={'height': '150px'})]),
#         dbc.Col([dbc.Card([dbc.CardBody([
#             html.H6('VaR', style={'fontWeight': 'lighter', 'textAlign': 'center'}),
#             html.H3(id='var-value', style={'color': 'rgb(64 165 193)', 'textAlign': 'center'})
#         ])], style={'height': '150px'})])
#     ]),
#
#     html.Br(),
#     html.Br(),
#
#     # Graphs
#     dbc.Row([
#         dbc.Col([dbc.Card([dcc.Graph(id='pie-chart')])]),
#         dbc.Col([dbc.Card([dcc.Graph(id='stock-returns-graph')])])
#     ])
# ])
#
# app.layout = html.Div(id='parent', children=[navbar, body_app], style={'margin': '30px'})
#
#
# @app.callback(
#     Output('stock-returns-graph', 'figure'),
#     Input('stocks-dropdown', 'value')
# )
# def update_graph(selected_stocks):
#     if not selected_stocks:
#         # Retourner un graphique vide ou un message lorsque rien n'est sélectionné
#         return go.Figure()
#
#     filtered_data = []
#     header = prices_data[0].keys()
#     for line in prices_data[1:]:
#         filtered_line = {key: line[key] for key in selected_stocks}
#         filtered_data.append(filtered_line)
#
#     custom_colors = {
#         'AAPL': {'line': 'rgba(255, 99, 71)', 'fill': 'rgba(255, 99, 71)'},  # Tomate
#         'XOM': {'line': 'rgba(50, 205, 50)', 'fill': 'rgba(50, 205, 50)'},  # Lime
#         'PG': {'line': 'rgba(30, 144, 255)', 'fill': 'rgba(30, 144, 255)'},  # Dodger Blue
#     }
#
#     fig = go.Figure()
#
#     # Ajouter les courbes de prix pour chaque action sélectionnée
#     for stock in selected_stocks:
#         dates = [line['Date'] for line in prices_data[1:]]
#         prices = [float(line[stock]) for line in prices_data[1:]]
#
#         fig.add_trace(go.Scatter(
#             x=dates,
#             y=prices,
#             mode='lines',
#             name=stock,
#             fill='tozeroy',
#             fillcolor=custom_colors[stock]['fill'],
#             line=dict(color=custom_colors[stock]['line'])
#         ))
#
#     # Mettre à jour les propriétés du graphique
#     fig.update_layout(
#         title="Historical Prices",
#         xaxis_title='Date',
#         yaxis_title='Price',
#         template='plotly'
#     )
#
#     return fig
#
#
# @app.callback(
#     Output('pie-chart', 'figure'),
#     Input('stocks-dropdown', 'value')
# )
# def display_pie_chart(selected_stocks):
#     selected_stocks_sorted = sorted(selected_stocks)
#     selected_combination_str = ','.join(selected_stocks_sorted)
#
#     if selected_combination_str in optimal_weights:
#         weights = optimal_weights[selected_combination_str]
#
#         # Créer le graphique avec Plotly Graph Objects
#         fig = go.Figure(data=[go.Pie(labels=selected_stocks_sorted, values=weights)])
#         fig.update_layout(title='Optimal weights')
#         return fig
#
#     # Retourner un graphique avec un message d'erreur si aucune sélection valide
#     fig = go.Figure(data=[go.Pie(labels=['Aucune sélection'], values=[1])])
#     fig.update_layout(title='Veuillez sélectionner une combinaison valide')
#     return fig
#
# @app.callback(
#     [Output('expected-return', 'children'),
#      Output('sharpe-ratio', 'children'),
#      Output('var-value', 'children')],
#     Input('stocks-dropdown', 'value')
# )
# def calculate_metrics(selected_stocks):
#     if not selected_stocks:
#         return "Aucune sélection", "Aucune sélection", "Aucune sélection"
#
#     selected_stocks_sorted = ','.join(sorted(selected_stocks))
#
#     if selected_stocks_sorted not in optimal_weights:
#         return "Pas de poids disponibles", "Pas de poids disponibles", "Pas de poids disponibles"
#
#     weights = optimal_weights[selected_stocks_sorted]
#
#     # Manually compute mean returns and covariance
#     mean_returns = {}
#     for stock in selected_stocks:
#         returns_for_stock = [float(line[stock]) for line in returns_data[1:]]
#         mean_returns[stock] = sum(returns_for_stock) / len(returns_for_stock)
#
#     cov_matrix = {}
#     for stock1 in selected_stocks:
#         for stock2 in selected_stocks:
#             returns_stock1 = [float(line[stock1]) for line in returns_data[1:]]
#             returns_stock2 = [float(line[stock2]) for line in returns_data[1:]]
#             cov_matrix[(stock1, stock2)] = sum(
#                 (returns_stock1[i] - mean_returns[stock1]) * (returns_stock2[i] - mean_returns[stock2])
#                 for i in range(len(returns_stock1))
#             ) / len(returns_stock1)
#
#     # Expected return and portfolio volatility
#     expected_return = sum(weights[i] * mean_returns[stock] for i, stock in enumerate(selected_stocks))
#     portfolio_variance = sum(weights[i] * weights[j] * cov_matrix[(selected_stocks[i], selected_stocks[j])]
#                              for i in range(len(selected_stocks)) for j in range(len(selected_stocks)))
#     portfolio_volatility = portfolio_variance ** 0.5
#
#     # Sharpe Ratio
#     risk_free_rate = 0.01
#     sharpe_ratio = (expected_return - risk_free_rate) / portfolio_volatility
#
#     # VaR
#     portfolio_returns = [sum(weights[i] * float(line[selected_stocks[i]]) for i in range(len(selected_stocks)))
#                          for line in returns_data[1:]]
#     historical_var = sorted(portfolio_returns)[int(0.05 * len(portfolio_returns))]
#
#     return (
#         f"{expected_return:.2%}",
#         f"{sharpe_ratio:.2f}",
#         f"{historical_var:.2%}"
#     )
# server = app.server  # Allows Gunicorn to access the WSGI server.
# print("L'objet app a __call__ ? :", hasattr(app, "__call__"))
# print("Le serveur Flask a __call__ ? :", hasattr(app.server, "__call__"))
#
# if __name__ == '__main__':
#     app.run_server(debug=True)
# Importing necessary libraries
import os
import json
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, Dash
import plotly.graph_objects as go

# ---------------------------
# 1. Paths and Data Loading
# ---------------------------

# Directory setup for data files
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '', 'data'))

# Load optimal weights from JSON file
optimal_weights_path = os.path.join(DATA_DIR, 'optimal_weights.json')
if os.path.exists(optimal_weights_path):
    with open(optimal_weights_path, 'r') as f:
        optimal_weights = json.load(f)
else:
    raise FileNotFoundError(f"Le fichier {optimal_weights_path} est introuvable.")

# Load prices and returns data from CSV files
def load_data(file_path, file_type='csv'):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            if file_type == 'csv':
                return f.readlines()
    else:
        raise FileNotFoundError(f"Le fichier {file_path} est introuvable.")

prices = load_data(os.path.join(DATA_DIR, 'prices.csv'))
returns = load_data(os.path.join(DATA_DIR, 'returns.csv'))

# ---------------------------
# 2. Data Processing Functions
# ---------------------------

# Process CSV data into structured dictionaries
def process_csv_data(csv_lines):
    header = csv_lines[0].strip().split(',')
    data = []
    for line in csv_lines[1:]:
        values = line.strip().split(',')
        data.append(dict(zip(header, values)))
    return data

prices_data = process_csv_data(prices)
returns_data = process_csv_data(returns)

# ---------------------------
# 3. Dash App Setup
# ---------------------------

# Create custom Dash class to support WSGI compatibility
class CallableDash(Dash):
    def __call__(self, environ, start_response):
        return self.server(environ, start_response)

# Initialize Dash App with Bootstrap theme
app = CallableDash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# ---------------------------
# 4. Layout & UI Components
# ---------------------------

# Navbar setup
navbar = dbc.Navbar(
    id='navbar',
    children=[
        dbc.Row(
            children=[
                dbc.Col(
                    dbc.NavbarBrand(
                        "Portfolio Optimization",
                        style={
                            'color': 'white',
                            'fontSize': '30px',
                            'fontFamily': 'Arial',
                            'margin-left': '15px',
                            'fontWeight': 'bold'
                        }
                    )
                )
            ],
            align="center",
            justify="center"
        )
    ],
    color='#01080b',
    dark=True,
    fixed="top"
)

# Dropdown for stock selection
card_content_dropdown = dbc.CardBody([
    html.H6('', style={'textAlign': 'center'}),
    dbc.Row([
        dbc.Col([dcc.Dropdown(
            id='stocks-dropdown',
            options=[{'label': stock, 'value': stock} for stock in ['AAPL', 'PG', 'XOM']],
            value=["AAPL", "PG", "XOM"],
            multi=True
        )])
    ])
])

# Layout for the body of the app
body_app = dbc.Container([
    html.Br(),
    html.Br(),
    dbc.Row([
        dbc.Col([dbc.Card(card_content_dropdown, style={'height': '150px'})], width=4),
        dbc.Col([dbc.Card([dbc.CardBody([html.H6('Expected Performance', style={'fontWeight': 'lighter', 'textAlign': 'center'}), html.H3(id='expected-return', style={'color': 'rgb(64 165 193)', 'textAlign': 'center'})])], style={'height': '150px'})]),
        dbc.Col([dbc.Card([dbc.CardBody([html.H6('Sharpe Ratio', style={'fontWeight': 'lighter', 'textAlign': 'center'}), html.H3(id='sharpe-ratio', style={'color': 'rgb(64 165 193)', 'textAlign': 'center'})])], style={'height': '150px'})]),
        dbc.Col([dbc.Card([dbc.CardBody([html.H6('VaR', style={'fontWeight': 'lighter', 'textAlign': 'center'}), html.H3(id='var-value', style={'color': 'rgb(64 165 193)', 'textAlign': 'center'})])], style={'height': '150px'})])
    ]),
    html.Br(),
    html.Br(),
    dbc.Row([dbc.Col([dbc.Card([dcc.Graph(id='pie-chart')])]), dbc.Col([dbc.Card([dcc.Graph(id='stock-returns-graph')])])])
])

app.layout = html.Div(id='parent', children=[navbar, body_app], style={'margin': '30px'})

# ---------------------------
# 5. Callbacks and Logic
# ---------------------------

# Update stock returns graph based on selected stocks
@app.callback(
    Output('stock-returns-graph', 'figure'),
    Input('stocks-dropdown', 'value')
)
def update_graph(selected_stocks):
    if not selected_stocks:
        return go.Figure()

    filtered_data = [{key: line[key] for key in selected_stocks} for line in prices_data[1:]]
    custom_colors = {'AAPL': {'line': 'rgba(255, 99, 71)', 'fill': 'rgba(255, 99, 71)'}, 'XOM': {'line': 'rgba(50, 205, 50)', 'fill': 'rgba(50, 205, 50)'}, 'PG': {'line': 'rgba(30, 144, 255)', 'fill': 'rgba(30, 144, 255)'}}
    fig = go.Figure()

    for stock in selected_stocks:
        dates = [line['Date'] for line in prices_data[1:]]
        prices = [float(line[stock]) for line in prices_data[1:]]
        fig.add_trace(go.Scatter(x=dates, y=prices, mode='lines', name=stock, fill='tozeroy', fillcolor=custom_colors[stock]['fill'], line=dict(color=custom_colors[stock]['line'])))

    fig.update_layout(title="Historical Prices", xaxis_title='Date', yaxis_title='Price', template='plotly')
    return fig

# Display pie chart for optimal weights
@app.callback(
    Output('pie-chart', 'figure'),
    Input('stocks-dropdown', 'value')
)
def display_pie_chart(selected_stocks):
    selected_combination_str = ','.join(sorted(selected_stocks))

    if selected_combination_str in optimal_weights:
        weights = optimal_weights[selected_combination_str]
        fig = go.Figure(data=[go.Pie(labels=selected_stocks, values=weights)])
        fig.update_layout(title='Optimal weights')
        return fig

    fig = go.Figure(data=[go.Pie(labels=['Aucune sélection'], values=[1])])
    fig.update_layout(title='Veuillez sélectionner une combinaison valide')
    return fig

# Calculate portfolio metrics: expected return, Sharpe ratio, and VaR
@app.callback(
    [Output('expected-return', 'children'),
     Output('sharpe-ratio', 'children'),
     Output('var-value', 'children')],
    Input('stocks-dropdown', 'value')
)
def calculate_metrics(selected_stocks):
    if not selected_stocks:
        return "Aucune sélection", "Aucune sélection", "Aucune sélection"

    selected_stocks_sorted = ','.join(sorted(selected_stocks))

    if selected_stocks_sorted not in optimal_weights:
        return "Pas de poids disponibles", "Pas de poids disponibles", "Pas de poids disponibles"

    weights = optimal_weights[selected_stocks_sorted]
    mean_returns = {stock: sum([float(line[stock]) for line in returns_data[1:]]) / len(returns_data[1:]) for stock in selected_stocks}
    cov_matrix = {(stock1, stock2): sum(
        (float(line[stock1]) - mean_returns[stock1]) * (float(line[stock2]) - mean_returns[stock2]) for line in returns_data[1:]
    ) / len(returns_data[1:]) for stock1 in selected_stocks for stock2 in selected_stocks}

    expected_return = sum(weights[i] * mean_returns[stock] for i, stock in enumerate(selected_stocks))
    portfolio_variance = sum(weights[i] * weights[j] * cov_matrix[(selected_stocks[i], selected_stocks[j])] for i in range(len(selected_stocks)) for j in range(len(selected_stocks)))
    portfolio_volatility = portfolio_variance ** 0.5

    risk_free_rate = 0.01
    sharpe_ratio = (expected_return - risk_free_rate) / portfolio_volatility
    portfolio_returns = [sum(weights[i] * float(line[selected_stocks[i]]) for i in range(len(selected_stocks))) for line in returns_data[1:]]
    historical_var = sorted(portfolio_returns)[int(0.05 * len(portfolio_returns))]

    return f"{expected_return:.2%}", f"{sharpe_ratio:.2f}", f"{historical_var:.2%}"

# ---------------------------
# 6. Running the Server
# ---------------------------

server = app.server  # Allows Gunicorn to access the WSGI server.
if __name__ == '__main__':
    app.run_server(debug=True)
