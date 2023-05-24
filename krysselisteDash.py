# These packages will be used in the project
import pandas as pd                                          # Reading and Organizing Data
#import numpy as np                                           # Allow for easier number handling
import dash                                                  # Running the Application
from dash import dcc                                         # Creating Interactive Components
from dash import html                                        # Allow for the use of HTML tags
from dash import Dash
import plotly.express as px                                  # Creating Interactive Plots
#from pandas_datareader import wb                             # Used for importing data
from dash.dependencies import Input, Output                  # Neccesary for interactivity in the app
import dash_bootstrap_components as dbc                      # Used for styling of application
from dash_bootstrap_templates import load_figure_template    # Used for styling of
from jupyter_dash import JupyterDash                         # Jupyter Notebook compatability

# Import Style Files
dbc_css = 'https://bootswatch.com/5/litera/bootstrap.min.css'
load_figure_template('litera')

# Load the data into memory and converting names to correct format
kryss = pd.read_csv("krysseliste_anon.csv", delimiter=";")

# Reprogramming the date column into the correct format
# kryss.info()

kryss['tidspunkt'] = pd.to_datetime(kryss['tidspunkt'], format='%Y-%m-%d %H:%M:%S')

# Header Dashboard
# :-------------------------------
# Here we make use of a custom CSS file in order to
# resize and color the background picture

header_card = dbc.Card(
    [
        dbc.CardImg(
            src="/assets/bergen_drone.JPG",
            top=True,
            className="card-image",
            style={"opacity": 0.3}
        ),
        dbc.CardImgOverlay(
            dbc.CardBody(
                [
                    dbc.Row(children=[
                        dbc.Col(html.H4('K8 SEKUNDER | SANDER DAHLING', style = {'textAlign' : 'center', 'color':'white'}))
                         ]),
                    
                    dbc.Row(children=[
                        dbc.Col(html.H1('Krysseliste Dashboard',style = {'textAlign' : 'center', "fontSize":"300%", 'color':'white'}))
                        ]),
                ],
            ),
            className="overlay",
        ),
    ],
    style={"width": "12"},
)


# Body Text of the Dashboard
# :-------------------------------
description_dash = """
Denne applikasjonen har hentet data direkte fra K8 Sekunder sin krysseliste database. Den har ulike features som skal belyse en enkeltpersons konsum,
i tillegg til aggregerte tall for hele gruppen.
"""

body_card = html.Div(
    [
        dbc.Card(description_dash, body=True),
    ]
)

# Feature 1
# :-------------------------------
def top_obs(dataframe, column_name, i):
    # Count the number of observations in the column
    value_counts = dataframe[column_name].value_counts()
    
    # Get the top three most common observations
    top_three_values = value_counts.head(i)
    
    # Create a dataframe to store the results
    result_df = pd.DataFrame({
        'Observation': top_three_values.index,
        'Count': top_three_values.values
    })
    
    return result_df

# Top 3 Mest likte drikke
pop_drink = top_obs(kryss, "vare", 3)

# Highest Krysser
high_kryss = top_obs(kryss, "bruker", 3)

# Best Hansa Drinker (Hansa Pils 0,33)
hansa_kryss = kryss[kryss["vare"] == "Hansa Pils 0,33"]

top_hansa_fan = top_obs(hansa_kryss, "bruker", 3)

# :-------------------------------
# Creating the cards

# Card Creation Function
def card_display(title, info):
    card = [
        dbc.CardHeader(title, style={"text-align":"center"}),
        dbc.CardBody([
            html.H1(f"{info}", className="card-title", style={"text-align":"center", "font-size":"200%"})
            ], style={"display":"flex", "justify-content":"center", "align-items":"center", "flex-direction":"column"}),
    ]
    return card


# Top 3 Card Creation Function
def top_3_display(title, df, value, name):
    df = df.nlargest(3, value)  # get the top 3 records with highest 'value'
    records = []
    for i, row in enumerate(df.iterrows(), start=1):  # start enumeration from 1
        formatted_value = round(row[1][value], 2)  # round the 'value' to 2 decimal places
        records.append(html.P(f"{i}. {row[1][name]}: {formatted_value} stk", className="standard-font"))
    
    card = [
        dbc.CardHeader(title, className="standard-font custom-class"),
        dbc.CardBody(html.B(records)),
    ]
    return(card)

# :-------------------------------
# Creating a top card section
top_card = dbc.Card(children=[
    dbc.Row(children=[
        # Most Popular Drink
        dbc.Col(dbc.Card(top_3_display("Mest Populære Drikker 22/23", pop_drink, "Count", "Observation"), color = "light", inverse=False, style={"height":"100%", "display":"flex", "justify-content":"center", "align-items":"center"})),
        
        # Highest Krysser
        # dbc.Col(dbc.Card(card_display("Mest Antall Kryss 22/23", f'{high_kryss["Observation"][0]}: {high_kryss["Count"][0]} stk'), color = "light", inverse=False, style={"height":"100%", "display":"flex", "justify-content":"center", "align-items":"center"})),
        
        dbc.Col(dbc.Card(top_3_display("Mest Antall Kryss 22/23", high_kryss, "Count", "Observation"), color = "light", inverse=False, style={"height":"100%", "display":"flex", "justify-content":"center", "align-items":"center"})),
        
        # Biggest Lover of Hansa Pils
        # dbc.Col(dbc.Card(card_display("Største Hansa 0.33 Fan 22/23", f'{top_hansa_fan["Observation"][0]}: {top_hansa_fan["Count"][0]} stk'), color = "light", inverse=False, style={"height":"100%", "display":"flex", "justify-content":"center", "align-items":"center"})),
        
        dbc.Col(dbc.Card(top_3_display("Største Hansa 0.33 Fan 22/23", top_hansa_fan, "Count", "Observation"), color = "light", inverse=False, style={"height":"100%", "display":"flex", "justify-content":"center", "align-items":"center"})),
    ])
], body=True, style={"height":"2"}
)

# :-------------------------------
# Creating User Input Functions

# :-------------------------------
# Drikke Dropdown
drikke_options = [{"label" : i, "value" : i} for i in kryss["vare"].unique()]

drikke_dropdown = dcc.Dropdown(
    id = "drikke-dropdown",
    options=drikke_options,
    multi=True
)

# Every Drink Button
select_all = dbc.Button("Velg Alle", id='select-all-button', className="me-2")

clear_all = dbc.Button("Fjern Alle", id='clear-all-button', className="me-2")


# :-------------------------------
# Line or Bar plot Radio Button
chart_radio = dcc.RadioItems(
    id = "radio-diag",
    options = {"line_diag":"Linjediagram",
               "bar_diag":"Barplott"},
    value="line_diag",
    inline=False
)
# :-------------------------------
# Line or Bar plot Radio Button
user_radio = dcc.RadioItems(
    id = "radio-diag-user",
    options = {"pie_diag":"Kakediagram",
               "bar_diag":"Barplott"},
    value="bar_diag",
    inline=False
)

# :-------------------------------
# Time Frame Choice Drikke
time_dropdown_drink = dcc.Dropdown(
    id = "time-dropdown-drink",
    options={"day":"Day",
             "month":"Month"},
    multi=False,
    value="month"
)

# Time Frame Choice Bruker
time_dropdown_user = dcc.Dropdown(
    id = "time-dropdown-user",
    options={"day":"Day",
             "month":"Month"},
    multi=False,
    value="month"
)

# :-------------------------------
# Name Dropdown
name_options = [{"label" : i, "value" : i} for i in kryss["bruker"].unique()]

name_dropdown = dcc.Dropdown(
    id = "name-dropdown",
    options=name_options,
    value=None,
    multi=False
)

# :-------------------------------
# The First Card Showing the drink plots
card_drink = dbc.Card(children=[
    dbc.Row(dbc.Col(dbc.CardHeader(html.B('Feature 2:'), style = {"fontSize":"200%"}))),
    dbc.Row(dbc.Col(dbc.CardBody('I denne delen av dashbordet kan du velge hvilke drikker som skal vises, samtidig som du kan velge hvordan dataen skal vises og hvordan den aggregeres'))),
    
    html.Br(), 
    # Drink Dropdown
    dbc.Row(children=[
        dbc.Col(drikke_dropdown, width=9),
        dbc.Col(select_all, width="auto"),
        dbc.Col(clear_all, width="auto")
    ]),
    html.Br(),
    dbc.Row(children=[
        dbc.Col(chart_radio, width="auto"),
        dbc.Col(time_dropdown_drink, width=3)    
    ]),
    html.Br(),
    
    # Line Diagram
    dbc.Row(children=[
        dbc.Col([dcc.Graph(id = "my-drink-graph", style = {"height":"45vh"})])
    ], justify="centre"),
], style = {"width" : "12"})

# :-------------------------------
# The Second Card Showing the Indivdual Members
card_name = dbc.Card(children=[
    dbc.Row(dbc.Col(dbc.CardHeader(html.B('Feature 3:'), style = {"fontSize":"200%"}))),
    dbc.Row(dbc.Col(dbc.CardBody('I denne delen kan man se på de individuelle kryssevanene til de ulike medlemmene av K8.'))),
    
    html.Br(), 
    # Drink Dropdown
    dbc.Row(children=[
        dbc.Col(name_dropdown, width=9)
    ]),
    html.Br(),
    dbc.Row(children=[
        dbc.Col(user_radio, width="auto"),
        dbc.Col(time_dropdown_user, width=3, id = "show-timeframe")    
    ]),
    html.Br(),
    
    # Line Diagram
    dbc.Row(children=[
        dbc.Col([dcc.Graph(id = "my-user-graph", style = {"display":"none"})])
    ], justify="centre"),

], style = {"width" : "12"})

# Tabs
tab1 = dbc.Tab(children = [card_drink], label = "Drikke")

tab2 = dbc.Tab(children = [card_name], label = "Bruker")

# Creating a dash framework
load_figure_template('litera')
app = Dash(external_stylesheets = [dbc.themes.LITERA, dbc_css])
server = app.server

app.layout = dbc.Container(
    children = [

        html.Br(),
        header_card,
        html.Br(),
        body_card,
        html.Br(),
        top_card,
        html.Br(),

        # # Line Chart Card
        dbc.Tabs(children = [
            tab1, 
            tab2
        ]), 
        html.Br()
    ]
)

# :-------------------------------
# Callback Functions

# :-------------------------------
# # Choose Every Drink
@app.callback(
    Output('drikke-dropdown', 'value'),
    Input('select-all-button', 'n_clicks'), 
    Input('clear-all-button', 'n_clicks')
)
def update_dropdown(select_all_clicks, clear_all_clicks):
    ctx = dash.callback_context
    if not ctx.triggered:
        return ["Hansa Pils 0,33"]
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == 'select-all-button' and select_all_clicks is not None:
        return [option['value'] for option in drikke_options]
    elif button_id == 'clear-all-button' and clear_all_clicks is not None:
        return []
    return []

# :-------------------------------
# Drikke Graph
@app.callback(
    Output("my-drink-graph", "figure"),
    Input("drikke-dropdown", "value"),
    Input("radio-diag", "value"),
    Input("time-dropdown-drink", "value")
)
def drikke_graph(drikke, choice, timeframe):
    
    if timeframe == "day":
        # Aggregating Kryss into each respective day
        kryss['tidspunkt'] = pd.to_datetime(kryss['tidspunkt']).dt.date
        grouped_kryss = kryss.groupby(['tidspunkt', 'vare']).size().reset_index(name='count')

        # Creating a subset for each chosen drink
        subset = grouped_kryss[grouped_kryss["vare"].isin(drikke)]
    
    elif timeframe == "month":
        kryss['tidspunkt'] = pd.to_datetime(kryss['tidspunkt']).dt.date
        grouped_kryss = kryss.groupby(['tidspunkt', 'vare']).size().reset_index(name='count')
        subset = grouped_kryss[grouped_kryss["vare"].isin(drikke)].copy()  # Make a copy of the subset DataFrame
        subset['tidspunkt'] = pd.to_datetime(subset['tidspunkt'])
        subset.loc[:, 'tidspunkt'] = subset['tidspunkt']  # Use .loc to set values in the DataFrame
        subset = subset.groupby([pd.Grouper(key='tidspunkt', freq='MS'), 'vare']).sum().reset_index()


    if choice == "bar_diag":
        
        fig = px.bar(
            subset,
            x = "tidspunkt",
            y = "count",
            color = "vare",
            labels={
                     "count": "Antall Kryss per Varetype",
                     "tidspunkt": f"Tidspunkt {timeframe}",
                     "vare": "Krysseobjekt"
                 },
            title=f"Barplott av K7 sitt krysseforbruk"
        )
    
    else:
        fig = px.line(
            subset,
            x = "tidspunkt",
            y = "count",
            color = "vare",
            labels={
                     "count": "Antall Kryss per Varetype",
                     "tidspunkt": f"Tidspunkt {timeframe}",
                     "vare": "Krysseobjekt"
                 },
            title=f"Linjediagram av K7 sitt krysseforbruk"
        )
    
    #fig.update_xaxes(rangeslider_visible=True)
    return(fig)

# :-------------------------------
# User Graph
# id = "my-user-graph"
@app.callback(
    Output("my-user-graph", "figure"),
    Input("name-dropdown", "value"),
    Input("radio-diag-user", "value"),
    Input("time-dropdown-user", "value")
)
def drikke_graph(name, choice, timeframe):
    user_kryss = kryss[kryss["bruker"] == name]
    
    pie_subset = user_kryss.copy()

    pie_subset['tidspunkt'] = pd.to_datetime(pie_subset['tidspunkt'])
    pie_subset.loc[:, 'tidspunkt'] = pie_subset['tidspunkt']  # Use .loc to set values in the DataFrame
    pie_subset = pie_subset.groupby(['bruker', 'vare']).size().reset_index(name='vare_count')
    
    if timeframe == "day":
        subset = user_kryss.copy()

        subset['tidspunkt'] = pd.to_datetime(subset['tidspunkt'])
        subset.loc[:, 'tidspunkt'] = subset['tidspunkt']  # Use .loc to set values in the DataFrame
        subset = subset.groupby([pd.Grouper(key='tidspunkt', freq='D'), 'bruker', 'vare']).size().reset_index(name='vare_count')
        
    elif timeframe == "month":
        subset = user_kryss.copy()

        subset['tidspunkt'] = pd.to_datetime(subset['tidspunkt'])
        subset.loc[:, 'tidspunkt'] = subset['tidspunkt']  # Use .loc to set values in the DataFrame
        subset = subset.groupby([pd.Grouper(key='tidspunkt', freq='MS'), 'bruker', 'vare']).size().reset_index(name='vare_count')
        
    if choice == "bar_diag":
        
        fig = px.bar(
            subset,
            x = "tidspunkt",
            y = "vare_count",
            color = "vare",
            labels={
                     "vare_count": "Antall Kryss per Varetype",
                     "tidspunkt": f"Tidspunkt {timeframe}",
                     "vare": "Krysseobjekt"
                 },
            title=f"Barplott av {name} sitt krysseforbruk"
        )
    
    else:
        fig = px.pie(
            pie_subset,
            values="vare_count",
            names = "vare"
        )
    
    #fig.update_xaxes(rangeslider_visible=True)
    
    return(fig)

# :-------------------------------
# Show timeframe
@app.callback(
    Output("time-dropdown-user", "style"),
    Input("radio-diag-user", "value")
)
def show_timeframe (pie_checked):
    if pie_checked == "pie_diag":
        return {"display":"none"}
    else:
        return {"display":"block"}

# :-------------------------------
# Show User Graph
@app.callback(
    Output("my-user-graph", "style"),
    Input("name-dropdown", "value")
)
def show_user (user_selected):
    if user_selected == None:
        return({"display":"none"})
    else:
        return({"display":"block"})

# :-------------------------------
# Run the App
app.run_server(debug = True, port = 8052)
