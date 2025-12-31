# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                html.Div(["Input: ", dcc.Dropdown(id='site-dropdown',  
                                    options=[{'label': 'All Sites', 'value': 'ALL'},
                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}],
                                    value='ALL',
                                    placeholder="place holder here",
                                    searchable=True),]),
                                #dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                html.Div(["Select: ", dcc.RangeSlider(id='payload-slider',
                                                    min=0, max=10000, step=1000,
                                                    marks={0: '0',
                                                               10000: '10k'},
                                                    value=[min_payload, max_payload])]),
                                #dcc.RangeSlider(id='payload-slider',...)

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    data = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(data, values='class', 
        names='Launch Site', 
        title='Successes by launch site')
        return fig
    else:
        # return the outcomes piechart for a selected site
        sub_data = data.loc[data["Launch Site"] == entered_site].groupby('class')['class'].count()
        fig = px.pie(sub_data,values='class',names='class', title=f"Successful launches at site {entered_site}")
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value')])
def get_scatter_plot(l_site,min_max):
    data = spacex_df[spacex_df['Payload Mass (kg)'].between(min_max[0], min_max[1])]
    if l_site == 'ALL':
        sfig = px.scatter(data, y='class', 
        x='Payload Mass (kg)', color='Launch Site', 
        title='Successes by launch site and payload mass')
        return sfig
    else:
        sub_data = data.loc[data["Launch Site"] == l_site]
        sfig = px.scatter(sub_data, y='class', 
        x='Payload Mass (kg)',
        title=f'Successes by payload mass for site: {l_site}')
        return sfig

# Run the app
if __name__ == '__main__':
    app.run()
