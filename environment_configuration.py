# ===============================================================================
# 01.00.01 | Environment Configuration | Documentation
# ===============================================================================
# Name:               01_environment_configuration
# Author:             Rodd
# Last Edited Date:   11/9/19
# Description:        Loads packages, sets working directory, 
#                     and defines global variables.
# Notes:              Must set your working directory outside of this script 
#                     to the location of the repo.
# Warnings:           The setting of the working directory is not automated.
# Outline:            Set your working directory to the code
#                     folder of the repo location (outside of this script).
#
#
# =============================================================================
# 01.00.02 | Import Packages
# =============================================================================
import os

print('Script: 01.00.02 [Import Packages] completed')

# =============================================================================
# 01.01.01 |Set Working Directory and Paths
# =============================================================================
# set working directory and create variable

# Get original working directory
owd = os.getcwd()

# Get out of the dash folder
#os.chdir("..")

# Set that as the working directory variable
working_directory = os.getcwd()

# Switch all the backlashes to forward slashes so it works with "Path"
working_directory = working_directory.replace('\\', '/')

# Switch the working directory back to default
os.chdir(owd)

# other file paths
data_path = '/data/input_data'
modeling_path = '../output/models'
dash_data_path = '/data'

# define data paths
products_path = '/product_metadata_dashboard.pkl'
top_10_products_path = '/top_10_products.pkl'
product_recs_orig_path = '/dnn_autoencoder_20_predictions.pkl'
user_recs_orig_path = '/dnn_user_prod_dense_20_predictions.pkl'
product_recs_path = '/product_recommendations.pkl'
user_recs_path = '/user_recommendations.pkl'

print('Script: 01.01.01 [Set working directory and other paths] completed')


# =============================================================================
# 01.02.01 | Define Other Global Variables
# =============================================================================
# colors are in spirit of Amazon color palette
colors = {'black_col': '#000000',     # Black
          'white_col': '#ffffff',     # White
          'vl_gray_col': '#f2f2f2',   # Very light gray
          'lgray_col': '#cdcdcd',     # Light gray          
          'gray_col': '#b3b3b3',      # Gray
          'orange_col': '#FF9900',    # Pure orange
          's_blue_col': '#146eb4',    # Strong blue
          'd_blue_col': '#232f3e'}    # Very dark desaturated blue
          
# defining length of tables
PAGE_SIZE = 10

# used for controlling filtering of tables
operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]

print('Script: 01.02.01 [Define Other Global Variables] completed')


# =============================================================================
# 01.03.01 | Define Functions
# =============================================================================
# used to help with filtering
# found this code here: https://dash.plot.ly/datatable/callbacks
def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value

    return [None] * 3

print('Script: 01.03.01 [Define Functions] completed')