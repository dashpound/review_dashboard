# ===============================================================================
# 01.00.01 | Data Configuration | Documentation
# ===============================================================================
# Name:               01_data_configuration
# Author:             Rodd
# Last Edited Date:   11/16/19
# Description:        
#  
#                   
# Notes:              
#                     
#
# Warnings:           
#
#
# Outline:         
# TO DO: 
#       Get URL variable and potentially images from raw data.
#       Get prediction sets.
#       Clarify user metadata with Hemant - # of reviews & ratings are at a user or product level?   
#
#
# =============================================================================
# 01.00.02 | Import Packages
# =============================================================================
# Import packages
import pandas as pd
import pickle
from pathlib import Path
import gc

# Import modules (other scripts)
from environment_configuration import working_directory, data_path, dash_data_path
from environment_configuration import reviews_ind_path, reviews_agg_path, products_path


# =============================================================================
# 01.01.01| Import Data
# =============================================================================
# Load individual review level dataset
with open(Path(working_directory + data_path + reviews_ind_path), 'rb') as pickle_file:
    review_data_ind = pickle.load(pickle_file)
    review_data_ind = pd.DataFrame(review_data_ind)

gc.collect()


# Load product level metadata dataset
with open(Path(working_directory + data_path + products_path), 'rb')  as pickle_file:
    product_data = pickle.load(pickle_file)
    product_data = pd.DataFrame(product_data)

gc.collect()

## Load product recommendations
#with open(Path(working_directory + data_path + reviews_ind_path), 'rb') as pickle_file:
#    review_data_ind = pickle.load(pickle_file)
#    review_data_ind = pd.DataFrame(review_data_ind)
#
#gc.collect()
#
#
## Load user recommendations
#with open(Path(working_directory + data_path + reviews_ind_path), 'rb') as pickle_file:
#    review_data_ind = pickle.load(pickle_file)
#    review_data_ind = pd.DataFrame(review_data_ind)
#
#gc.collect()



# =============================================================================
# 01.02.01| Select columns
# =============================================================================
product_data_sub = product_data[['asin','title','category2_t','category3_t','price_t','numberReviews','meanStarRating']]
# universally only taking the first 60 characters for the title
product_data_sub['title'] = product_data_sub['title'].str[:60]


# =============================================================================
# 01.03.01| Add relevant metadata to predictions
# =============================================================================



# =============================================================================
# 01.04.01| Define Summary Data Frames
# =============================================================================
# top 10 products
top_10_products = product_data_sub.sort_values('numberReviews', ascending=False).head(10)[['title','numberReviews']]
top_10_products = top_10_products.sort_values('numberReviews', ascending=True)

# =============================================================================
# 01.05.01| Pickle Results
# =============================================================================
top_10_products.to_pickle(Path(working_directory + dash_data_path + "/top_10_products.pkl"))