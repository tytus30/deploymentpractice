# %% [markdown]
# ### Assignment #4/5: Basic UI
# 
# DS4003 | Spring 2024
# 
# Objective: Practice buidling basic UI components in Dash. 
# 
# Task: Build an app that contains the following components user the gapminder dataset: `gdp_pcap.csv`. [Info](https://www.gapminder.org/gdp-per-capita/)
# 
# UI Components:
# A dropdown menu that allows the user to select `country`
# -   The dropdown should allow the user to select multiple countries
# -   The options should populate from the dataset (not be hard-coded)
# 
# A slider that allows the user to select `year`
# -   The slider should allow the user to select a range of years
# -   The range should be from the minimum year in the dataset to the maximum year in the dataset
# 
# A graph that displays the `gdpPercap` for the selected countries over the selected years
# -   The graph should display the gdpPercap for each country as a line
# -   Each country should have a unique color
# -   The graph should have a title and axis labels in reader friendly format  
# 
# Layout:  
# - Use a stylesheet
# - There should be a title at the top of the page
# - There should be a description of the data and app below the title (3-5 sentences)
# - The dropdown and slider should be side by side above the graph and take up the full width of the page
# - The graph should be below the dropdown and slider and take up the full width of the page
# 
# Submission: 
# - There should be only one app in your submitted work
# - Comment your code
# - Submit the html file of the notebook save as `DS4003_A4_LastName.html`
# 
# 
# **For help you may use the web resources and pandas documentation. No co-pilot or ChatGPT.**

# %%
# import libraries
import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px
from dash import Dash, html, dcc, Input, Output

# %%
# load the data
gdp1 = pd.read_csv("gdp_pcap.csv")

# pivot the table because the variables are not all on their own column
gdp = gdp1.melt(id_vars='country', var_name='year', value_name='gdp')

# look at data
print(gdp.dtypes)
print(gdp.head())

# define a function to convert 'k' suffixes to thousands, while avoiding all other values
def convert_to_thousands(value):
    if 'k' in value:
        return float(value.replace('k', '')) * 1000
    else:
        return float(value)

# apply the function to the 'gdp' column
gdp['gdp'] = gdp['gdp'].astype(str).apply(convert_to_thousands)

# look at the gdp column, does it look right...
print(gdp['gdp'])

# change year and gdp to int
gdp['year'] = gdp['year'].astype(int)
gdp['gdp'] = gdp['gdp'].astype(float)

# confrim data
print(gdp.dtypes)

# %%
# add a stylesheet
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# create a color map for each country to ensure each country gets a unique color
color_map = {
    country: f'rgb({np.random.randint(0, 256)}, {np.random.randint(0, 256)}, {np.random.randint(0, 256)})'
    for country in gdp['country'].unique()
}

# make the graph
fig = px.line(gdp, x="year", y="gdp", color="country", color_discrete_map=color_map) #call the color map to ensure colors are shown
fig.update_layout(title='GDP Change Over Time', xaxis_title='Year', yaxis_title='GDP') # adds title and axis


# initialize app
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Countries' GDP Change Over Time"

# define layout and elements
app.layout = html.Div([

    #titles and subheadings
    html.Div(className='row', children=[ #row makes this its own row
        html.H1("GDP Per Capita"),
        html.H4("This app lets you visualize GDP changes over time for selected countries. Use the dropdown menu to select countries. Use the range slider to select the years you want to see. Afterwards, it graphs the countries you have selected and shows their GDP change over the time period you've selected.")
    ]),

    html.Div(children = [
        dcc.Dropdown( #this is making the dropdown feature
            gdp.country.unique(), #this is to select from the countries column
            id = 'pandas-dropdown',
            placeholder =  'select countries',
            value = gdp.country.unique(), #adding all values into the dropdown to start off with every country on the graph
            multi = True # this makes dropdown multi-select
            ),
    ], style={'width': '50%', 'display': 'inline-block'}), #puts this in 50% of the screen
    #className = 'six columns'), #puts this in 50% of the screen with the range slider row, but couldnt get this to work properly

    html.Div(children = [
        dcc.RangeSlider( #making a range slider for the years
            id = 'pandas-range-slider',
            min = gdp['year'].min(), #finds the min in year column
            max = gdp['year'].max(), #finds the max in the year column
            step = 1,
            value = [gdp['year'].min(), gdp['year'].max()],  # set initial value to min and max years
            marks= {year: str(year) for year in range(gdp['year'].min(), gdp['year'].max() + 1, 50)},
            tooltip={"placement": "bottom", "always_visible": True} #this adds a year pop-up to know which year is selected
            )
    ], style={'width': '50%', 'display': 'inline-block'}), #puts this in 50% of the screen
    #className = 'six columns'), #puts this in 50% of the screen with the range slider row

    html.Div(children = [
        dcc.Graph( #making a graph
            id = 'pandas-graph',
            figure= fig #call the plotly graph from above
        )
    ])
])

# define callback for updating the graph
@app.callback(
    Output('pandas-graph', 'figure'),
    Input('pandas-dropdown', 'value'),
    Input('pandas-range-slider', 'value')
)
def update_graph(selected_countries, selected_years):
    filtered_gdp = gdp[(gdp['country'].isin(selected_countries)) & (gdp['year'].between(selected_years[0], selected_years[1]))]
# problem is here

    fig = px.line(filtered_gdp, x="year", y="gdp", color="country", color_discrete_map=color_map)
    fig.update_layout(title='GDP Change Over Time', xaxis_title='Year', yaxis_title='GDP')
    return fig

# run app
if __name__ == '__main__':
    app.run(jupyter_mode='tab', debug=True)


