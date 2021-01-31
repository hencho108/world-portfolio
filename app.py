import funcs
import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.express as px
import pandas as pd

external_stylesheets = [
    dbc.themes.FLATLY,
    'https://use.fontawesome.com/releases/v5.7.2/css/all.css'
]

app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ],
    suppress_callback_exceptions=True
)

server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(
        id='page-content',
        style={
            'width':'80%',
            'max-width':'350px',
            'min-width':'350px',
            'margin':'0 auto',
            'margin-top':'10px',
            'padding':'5px',
            'height':'1000px',
            'border':'0px dashed grey'
        }
    )
], style={'height':'100vh','width':'100vw'}
)

home_layout = html.Div([
    html.H4(
        'Investment Simulator 📈',
        id='title',
        className='display-5',
        style={'text-align':'center', 'font-weight':'bold'}
    ),
    html.H6('Average Yearly Return', style={'margin-top':'25px'}),
    dbc.Input(id='avg_return', value=0.055, type='number', className='form-control'),

    html.H6('Standard Deviation', style={'margin-top':'10px'}),
    dbc.Input(id='std', value=0.18, type='number', className='form-control'),

    html.H6('Starting Amount', style={'margin-top':'10px'}),
    dbc.Input(id='start_amount', value=10000, type='number', className='form-control'),

    html.H6('Monthly Investment', style={'margin-top':'10px'}),
    dbc.Input(id='monthly_invest', value=1000, type='number', className='form-control'),

    html.H6('Years to Invest', style={'margin-top':'10px'}),
    dbc.Input(id='n_years', value=15, type='number', className='form-control'),


    html.H6('Simulations', style={'margin-top':'10px'}),
    dbc.Input(id='n_simulations', value=10000, type='number', className='form-control'),

    dbc.Button(
        [
            html.Span(
                'Simulate',
                style={'margin-right':'10px'}
            ),
            html.I(
                className='fas fa-flag-checkered'
            )
        ],
        id='submit_button',
        color='primary',
        className='btn btn-primary btn-lg btn-block',
        n_clicks_timestamp=0,
        style={'margin-top':'25px'}
    ),
    html.Br(),
    html.Div(id='out_final_amount'),
    html.Div(id='out_portfolio_val'),
    html.Div(id='out_profit'),
    html.Div(id='out_pos_proba'),
    dcc.Graph(id="graph", style={'width': 340, 'overflowY': 'scroll'})
], style={'border':'0px dashed red'}
)

@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/':
        return home_layout


@app.callback(
    [
        Output('out_final_amount','children'),
        Output('out_portfolio_val','children'),
        Output('out_profit','children'),
        Output('out_pos_proba','children'),
        Output('graph', 'figure')
    ],
    [
        Input('submit_button','n_clicks')
    ],
    [
        State('avg_return','value'),
        State('std','value'),
        State('start_amount','value'),
        State('monthly_invest','value'),
        State('n_years','value'),
        State('n_simulations','value')
    ]
)
def run_simulation(n_clicks, avg_return, std, start_amount, monthly_invest, n_years, n_simulations):
    if n_clicks is None:
        fig = px.histogram({'na': []}, 'na')
        return '', '', '' ,'', fig
    else:
        sim_result = funcs.simulation(avg_return, std, start_amount, monthly_invest, n_years, n_simulations)

        avg_portfolio_val = sim_result['avg_portfolio_val']

        df = pd.DataFrame(sim_result)
        fig = px.histogram(df, x='profits')

        txt_final_amount = 'Final Amount Invested: {:,.0f}'.format(sim_result['final_amount_invested'])
        txt_portfolio_val = 'Final Portfolio Value: {:,.0f} (SD: {:,.0f})'.format(sim_result['avg_portfolio_val'], sim_result['std_portfolio_val'])
        txt_profit = 'Avg. Profit: {:,.0f} (SD: {:,.0f})'.format(sim_result['avg_profit'], sim_result['std_profit'])
        txt_pos_proba = 'Positive Scenarios: {:.1%}'.format(sim_result['pos_proba'])

        return txt_final_amount, txt_portfolio_val, txt_profit, txt_pos_proba, fig


if __name__ == '__main__':
    app.run_server(debug=False)#, host='0.0.0.0')
