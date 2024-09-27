# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px
import numpy as np

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

#Create the options for the site dropdown list
options = spacex_df["Launch Site"].unique()
options = np.append(options, "All Sites")

# Create a dash application
app = dash.Dash(__name__)
# Set the title of the dashboard
app.title = "SpaceX Launch Records Analytics"

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36','font-size': 40}
    ),
# TASK 1: Add a dropdown list to enable Launch Site selection
# The default select value is for ALL sites
# dcc.Dropdown(id='site-dropdown',...)
    html.Div(
        dcc.Dropdown(
            id="site-dropdown",
            options= options,
            value = "All Sites",
            placeholder = "Select a Launch Site here",
            searchable = True
        )
    ),
    html.Br(),

# TASK 2: Add a pie chart to show the total successful launches count for all sites
# If a specific launch site was selected, show the Success vs. Failed counts for the site
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),

# TASK 3: Add a slider to select payload range
    html.Div(
        dcc.RangeSlider(
            id="payload-slider",
            min=0, max=10000, step=1000,
            value=[min_payload, max_payload]
        )
    ),

# TASK 4: Add a scatter chart to show the correlation between payload and launch success
    html.Div(
        dcc.Graph(
            id='success-payload-scatter-chart'
        )
    ),
]
)


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)

def updatepiechart(selected_location):
    df_pie = spacex_df
    #df_pie_selected = df_pie.groupby("Launch Site")["class"].sum().reset_index
    if selected_location == "All Sites":
        fig = px.pie(
            df_pie,
            names = "Launch Site",
            values = "class",
            title="Total Success Launches By Site"
        )
    else:
        df_pie = spacex_df[spacex_df["Launch Site"]==selected_location]
        df_pie = df_pie["class"].value_counts().reset_index()
        df_pie.columns = ["class","count"]
        fig = px.pie(
            df_pie, 
            names= "class",
            values="count",
            title="Total Success Launches for Site " + selected_location
        )
    
    fig.update_layout()
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id="success-payload-scatter-chart", component_property="figure"),
    [Input(component_id="payload-slider", component_property="value"),
    Input(component_id="site-dropdown", component_property="value")]
)

def updateScatter(selected_payload, selected_location):
    df_scatter = spacex_df[(spacex_df["Payload Mass (kg)"]<=selected_payload[1]) & (spacex_df["Payload Mass (kg)"]>=selected_payload[0])]
    if selected_location == "All Sites":
        fig = px.scatter(
            df_scatter,
            x="Payload Mass (kg)",
            y = "class",
            color = "Booster Version Category",
            title="Correlation between Payload and Success for all sites"
        )
    else:
        df_scatter = df_scatter[df_scatter["Launch Site"]==selected_location]
        fig = px.scatter(
            df_scatter,
            x="Payload Mass (kg)",
            y= "class",
            color = "Booster Version Category", 
            title="Correlation from Payload and Success for "+selected_location           
        )
    fig.update_layout()
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)