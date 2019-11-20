# ===============================================================================
# 02.00.01 | Dashboard App | Documentation
# ===============================================================================
# Name:               02_app
# Author:             Rodd/Patel
# Last Edited Date:   11/17/19
# Description:        Loads packages, loads and summarizes data, and defines dash components.
#  
#                   
# Notes:              Must install dash outside of this script.
#                        pip install dash==1.4.1  # The core dash backend
#                        pip install dash-daq==0.2.1  # DAQ components (newly open-sourced!)
#                    Dash code is finnicky on formatting and placement. There is some code that could be made into a function but dash does not like calling a function.
#                     
#
# Warnings:           Cannot filter the reviews aggregated data to Camera & Photo.
#
#
# Outline:            Import packages.
#                     Load data.
#                     Define dash layout.
#                     Define dash reactive components.
#                     Run dash.
#
#
# =============================================================================
# 02.00.02 | Import Packages
# =============================================================================
# Import packages
import pandas as pd
from pathlib import Path
from math import trunc

# Import modules (other scripts)
from environment_configuration import working_directory, dash_data_path
from environment_configuration import product_recs_path, user_recs_path, top_10_products_path
from environment_configuration import colors, PAGE_SIZE, operators, split_filter_part

# Dash packages
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# Dash data table
import dash_table


# =============================================================================
# 02.01.01| Import Data
# =============================================================================
# Load product recommendations
product_recs = pd.read_pickle(Path(working_directory + dash_data_path + product_recs_path))

# Load user recommendations
user_recs = pd.read_pickle(Path(working_directory + dash_data_path + user_recs_path))

# Load top 10 producs
top_10_products = pd.read_pickle(Path(working_directory + dash_data_path + top_10_products_path))

## =============================================================================
## 02.02.01| Filter Data
## =============================================================================
## product data
#sample_mapped_product['Mapped Product'] = sample_mapped_product['Mapped Product'].astype(str)
#sample_mapped_product['Product Code'] = sample_mapped_product['Product Code'].astype(str)
#
## reviewer data
#sample_mapped_reviewer['Product Code'] = sample_mapped_reviewer['Product Code'].astype(str)
#

# =============================================================================
# 02.03.01| Dash Layout
# =============================================================================
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

app.layout = html.Div(style={'backgroundColor': colors['d_blue_col']}, children=[
        
        
        html.Div([dbc.Row([
        # CognoClick Logo
                dbc.Col(html.Div(children=[html.Img(src=app.get_asset_url("../assets/CognoClick_upscaled_logo.jpg"),
                                                    id="cognoclick-logo",
                                                    style={'height':'35px', 
                                                           'width':'auto', 
                                                           'margin-top':'10px',
                                                           'margin-bottom':'10px',
                                                           'margin-left':'10px'})]),width=3,lg=3), 

        # Title
                dbc.Col(html.H1(children='Amazon Recommendation Engine',
                                style={'textAlign': 'center',
                                       'font-family':'Arial',
                                       'fontSize':36,
                                       'color': colors['gray_col']})),
    
        # Amazon Logo
                dbc.Col(html.Div(children=[html.Img(src=app.get_asset_url("../assets/Amazon_Logo.png"),
                                                    id="amazon-logo",
                                                    style={'background':colors['white_col'],
                                                           'height':'32px', 
                                                           'width':'auto', 
                                                           'margin-top':'10px',
                                                           'margin-left':'20px',
                                                           'margin-right':'10px',
                                                           'margin-bottom':'10px'
                                                           })]), width=3,lg=2)],align="center")]),
    

        # Top 10 Products Bar Chart
        dcc.Graph(
            id='top-10-graph',
            figure={
                'data': [go.Bar(y=top_10_products['title'],
                                x=top_10_products['numberReviews'], 
                                orientation='h',
                                marker_color=colors['orange_col'],
                                # adding custom hover info to bar plot
                                # had to search high and low to discover that this formatting works properly
                                # <br> is used to create new lines
                                text=['<b>Number of Reviews: </b>'+'{}'.format(trunc(numberReviews))+ # need this to be integer format
                                      '<br><b>Price: </b>'+'${:.2f}'.format(price_t)+
                                      '<br><b>Category 2: </b>'+'{}'.format(category2_t)+
                                      '<br><b>Category 3: </b>'+'{}'.format(category3_t)
                                      for numberReviews, price_t, category2_t, category3_t in 
                                               zip(list(top_10_products['numberReviews']),
                                               list(top_10_products['price_t']), 
                                               list(top_10_products['category2_t']),
                                               list(top_10_products['category3_t']))],
                                hoverinfo="text",
                                hoverlabel_align = 'left'
                                )],
                'layout': {'title': 'Top 10 Products Overall',
                           'plot_bgcolor': colors['white_col'],
                           'paper_bgcolor': colors['white_col'],
                           'font': {'color': colors['black_col']},
                           # titles are long so need to add a hefty left margin
                           'margin': {'l':500, 'pad':4}}}),
                          

        # Creating tabs to use to add in the recommendation components
        html.Div([dcc.Tabs(id="tabs", 
                           colors={'border': colors['black_col'],
                                   'primary': colors['orange_col'],
                                   'background': "cornsilk"},
                           children=[
        # Product Recommendation Tab
                dcc.Tab(label='Product Recommendations', children=[
                dash_table.DataTable(
                        id='product-table',
                        columns=[{"name": i, "id": i} for i in product_recs.columns],
                        page_current=0,
                        page_size=PAGE_SIZE,
                        page_action='custom',
                        filter_action='custom',
                        filter_query='' ,
                        style_table={'overflowX': 'scroll'},
                        style_cell={'padding':'5px',
                                    'font-family':'Arial',
                                    'fontSize':11,
                                    'textAlign': 'left',
                                    'minWidth': '0px', 'maxWidth': '180px',
                                    'whiteSpace': 'normal'},
                        style_header={'backgroundColor': colors['d_blue_col'],
                                      'color': colors['white_col'],
                                      'fontSize':13,
                                      'fontWeight': 'bold'},
                        style_data_conditional=[{'if': {'row_index': 'odd'}, 'backgroundColor': colors['lgray_col']}
        ]),
                # To add a new line, just add two spaces at the end of a sentence.
                # Cheating to get rid of dark background color at the end of text by adding a pad.
                dcc.Markdown('''
                             ###### Directions
                             Each column can be filtered based on user input.  
                             For string columns, just enter a partial string such as "Nook."  
                             Exception: For product columns, use quotes around filter, such as "328."  
                             For numeric columns, filters such as "=5" or ">=200" are valid filters.  
                             Use "Enter" to initiate and remove filters.  ''',
                             style={'backgroundColor': colors['white_col'],
                                    'fontSize':11,
                                    'padding':'10px'})]),
    
          # User Recommendation Tab
                dcc.Tab(label='User Recommendations', children=[
                dash_table.DataTable(
                        id='user-table',
                        columns=[{"name": i, "id": i} for i in user_recs.columns],
                        page_current=0,
                        page_size=PAGE_SIZE,
                        page_action='custom',
                        filter_action='custom',
                        filter_query='' ,
                        style_table={'overflowX': 'scroll'},
                        style_cell={'padding':'5px',
                                    'font-family':'Arial',
                                    'fontSize':11,
                                    'textAlign': 'left',
                                    'minWidth': '0px', 'maxWidth': '180px',
                                    'whiteSpace': 'normal'},
                        style_header={'backgroundColor': colors['d_blue_col'],
                                      'color': colors['white_col'],
                                      'fontSize':13,
                                      'fontWeight': 'bold'},
                        style_data_conditional=[{'if': {'row_index': 'odd'}, 'backgroundColor': colors['lgray_col']}]),
                # To add a new line, just add two spaces at the end of a sentence.
                # Cheating to get rid of dark background color at the end of text by adding a pad.
                dcc.Markdown('''
                             ###### Directions
                             Each column can be filtered based on user input.  
                             For string columns, just enter a partial string such as "Nook."  
                             Exception: For product columns, use quotes around filter, such as "328."  
                             For numeric columns, filters such as "=5" or ">=200" are valid filters.  
                             Use "Enter" to initiate and remove filters.  ''',
                             style={'backgroundColor': colors['white_col'],
                                    'fontSize':11,
                                    'padding':'10px'})]),
        ])]), # ends tabs
                        
        # Disclaimer at the bottom         
        dcc.Markdown('''
                     **Disclaimer**: This project was completed as part of the MSDS 498 Capstone Project course within the Northwestern University. This dashboard and data are completely simulated and not in any way connected to or a reﬂection of Amazon. Please do not duplicate or distribute outside of the context of this course.''',
                     style={'backgroundColor': colors['white_col'],
                                    'fontSize':8,
                                    'padding':'10px'})
    ])
    
    
# =============================================================================
# 02.04.01| Dash Reactive Components | Product Table
# =============================================================================
@app.callback(
    Output('product-table', "data"),
    [Input('product-table', "page_current"),
     Input('product-table', "page_size"),
     Input('product-table', "filter_query")])

# tried to move this to config file and call function but dash doesn't like that
def update_table(page_current,page_size, filter):
    print(filter)
    filtering_expressions = filter.split(' && ')
    dff = product_recs
    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)

        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            # these operators match pandas series operator method names
            dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
        elif operator == 'contains':
            dff = dff.loc[dff[col_name].str.contains(filter_value)]
        elif operator == 'datestartswith':
            # this is a simplification of the front-end filtering logic,
            # only works with complete fields in standard format
            dff = dff.loc[dff[col_name].str.startswith(filter_value)]

    return dff.iloc[
        page_current*page_size:(page_current+ 1)*page_size
    ].to_dict('records')
    

# =============================================================================
# 02.04.02| Dash Reactive Components | User Table
# =============================================================================
@app.callback(
    Output('user-table', "data"),
    [Input('user-table', "page_current"),
     Input('user-table', "page_size"),
     Input('user-table', "filter_query")])

def update_table2(page_current,page_size, filter):
    print(filter)
    filtering_expressions = filter.split(' && ')
    dff = user_recs
    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)

        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            # these operators match pandas series operator method names
            dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
        elif operator == 'contains':
            dff = dff.loc[dff[col_name].str.contains(filter_value)]
        elif operator == 'datestartswith':
            # this is a simplification of the front-end filtering logic,
            # only works with complete fields in standard format
            dff = dff.loc[dff[col_name].str.startswith(filter_value)]

    return dff.iloc[
        page_current*page_size:(page_current+ 1)*page_size
    ].to_dict('records')
    
    
# =============================================================================
# 02.05.01| Run Dash
# =============================================================================                               
if __name__ == '__main__':
    app.run_server(debug=True)