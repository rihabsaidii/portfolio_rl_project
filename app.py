import os
import json
import numpy as np
import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go

# Paths and Data Loading
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '', 'data'))

# Load optimal weights
optimal_weights_path = os.path.join(DATA_DIR, 'optimal_weights.json')
if os.path.exists(optimal_weights_path):
    with open(optimal_weights_path, 'r') as f:
        optimal_weights = json.load(f)
else:
    raise FileNotFoundError(f"Le fichier {optimal_weights_path} est introuvable.")

# Load prices data
prices_path = os.path.join(DATA_DIR, 'prices.csv')
if os.path.exists(prices_path):
    prices_df = pd.read_csv(prices_path)
    print("Fichier prices.csv chargé avec succès !")
else:
    raise FileNotFoundError(f"Le fichier {prices_path} est introuvable.")

# Load returns data
returns_path = os.path.join(DATA_DIR, 'returns.csv')
if os.path.exists(returns_path):
    returns_df = pd.read_csv(returns_path)
    print("Fichier returns.csv chargé avec succès !")
else:
    raise FileNotFoundError(f"Le fichier {returns_path} est introuvable.")

returns_numeric = returns_df.drop(columns=['Date'])

# Available combinations
available_combinations = list(optimal_weights.keys())

# Initialize Dash App
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# Navbar
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

# Dropdown Card
card_content_dropdown = dbc.CardBody([
    html.H6('', style={'textAlign': 'center'}),
    dbc.Row([
        dbc.Col([
            html.H6('Stocks'),
            dcc.Dropdown(
                id='stocks-dropdown',
                options=[
                    {'label': 'AAPL', 'value': 'AAPL'},
                    {'label': 'PG', 'value': 'PG'},
                    {'label': 'XOM', 'value': 'XOM'}
                ],
                value=["AAPL", "PG", "XOM"],
                multi=True
            ),
        ])
    ])
])

# Labels and Colors for Pie Chart
labels = ["AAPL", "PG", "XOM"]
colors = ['#ff9999', '#66b3ff', '#99ff99']

# App Layout
body_app = dbc.Container([
    html.Br(),
    html.Br(),

    # Metrics and Dropdown
    dbc.Row([
        dbc.Col([dbc.Card(card_content_dropdown, style={'height': '150px'})], width=4),
        dbc.Col([dbc.Card([dbc.CardBody([
            html.H6('Expected Performance', style={'fontWeight': 'lighter', 'textAlign': 'center'}),
            html.H3(id='expected-return', style={'color': 'rgb(64 165 193)', 'textAlign': 'center'})
        ])], style={'height': '150px'})]),
        dbc.Col([dbc.Card([dbc.CardBody([
            html.H6('Sharpe Ratio', style={'fontWeight': 'lighter', 'textAlign': 'center'}),
            html.H3(id='sharpe-ratio', style={'color': 'rgb(64 165 193)', 'textAlign': 'center'})
        ])], style={'height': '150px'})]),
        dbc.Col([dbc.Card([dbc.CardBody([
            html.H6('VaR', style={'fontWeight': 'lighter', 'textAlign': 'center'}),
            html.H3(id='var-value', style={'color': 'rgb(64 165 193)', 'textAlign': 'center'})
        ])], style={'height': '150px'})])
    ]),

    html.Br(),
    html.Br(),

    # Graphs
    dbc.Row([
        dbc.Col([dbc.Card([dcc.Graph(id='pie-chart')])]),
        dbc.Col([dbc.Card([dcc.Graph(id='stock-returns-graph')])])
    ])
])

app.layout = html.Div(id='parent', children=[navbar, body_app], style={'margin': '30px'})

# Callbacks
@app.callback(
    Output('stock-returns-graph', 'figure'),
    Input('stocks-dropdown', 'value')
)
def update_graph(selected_stocks):
    if not selected_stocks:
        return px.line(title="Veuillez sélectionner au moins une action.")

    filtered_df = prices_df[['Date'] + selected_stocks]
    custom_colors = {
        'AAPL': {'line': 'rgba(255, 99, 71)', 'fill': 'rgba(255, 99, 71)'},  # Tomate
        'XOM': {'line': 'rgba(50, 205, 50)', 'fill': 'rgba(50, 205, 50)'},  # Lime
        'PG': {'line': 'rgba(30, 144, 255)', 'fill': 'rgba(30, 144, 255)'},  # Dodger Blue
    }

    fig = go.Figure()
    for stock in selected_stocks:
        fig.add_trace(go.Scatter(
            x=filtered_df['Date'],
            y=filtered_df[stock],
            mode='lines',
            name=stock,
            fill='tozeroy',
            fillcolor=custom_colors[stock]['fill'],
            line=dict(color=custom_colors[stock]['line'])
        ))

    fig.update_layout(
        title="Historical Prices",
        xaxis_title='Date',
        yaxis_title='Price',
        template='plotly'
    )
    return fig

@app.callback(
    Output('pie-chart', 'figure'),
    Input('stocks-dropdown', 'value')
)
def display_pie_chart(selected_stocks):
    selected_stocks_sorted = sorted(selected_stocks)
    selected_combination_str = ','.join(selected_stocks_sorted)

    if selected_combination_str in optimal_weights:
        weights = optimal_weights[selected_combination_str]
        return px.pie(names=selected_stocks_sorted, values=weights, title='Optimal weights')

    return px.pie(names=['Aucune sélection'], values=[1], title='Veuillez sélectionner une combinaison valide')

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

    weights = np.array(optimal_weights[selected_stocks_sorted])
    df = pd.DataFrame({stock: returns_df[stock] for stock in selected_stocks})
    mean_returns = df.mean()
    cov_matrix = df.cov()

    expected_return = np.dot(weights, mean_returns)
    portfolio_std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    risk_free_rate = 0.01
    sharpe_ratio = (expected_return - risk_free_rate) / portfolio_std

    portfolio_returns = df.dot(weights)
    historical_var = np.percentile(portfolio_returns, 5)

    return (
        f"{expected_return:.2%}",
        f"{sharpe_ratio:.2f}",
        f"{historical_var:.2%}"
    )

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
