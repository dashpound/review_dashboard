# ===============================================================================
# 01.00.01 | Data Configuration | Documentation
# ===============================================================================
# Name:               01_data_configuration
# Author:             Rodd
# Last Edited Date:   11/19/19
# Description:        Creates relevant pickles to feed into dash app.
#  
#                   
# Notes:             Had to get pickles from Brian from capstone repo to run this file. 
#                     
#
# Warnings:           
#
#
# Outline:           Load packages.
#                    Import data to prepare.
#                    Select needed columns from the product data frame and truncate title to first 60 chars.
#                    Manipulate product recommendations data to create columns for dashboard.
#                    Create rank order variable for product recommendations and reorder data.
#                    Save recommendations via pickle.
#                    Repeat steps above for user recommendations.
#                    Create top 10 products data frame and pickle it.    
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
import sys

# Import modules (other scripts)
from environment_configuration import working_directory, data_path, dash_data_path
from environment_configuration import products_path, top_10_products_path
from environment_configuration import product_recs_orig_path, product_recs_path, user_recs_orig_path, user_recs_path

# =============================================================================
# 01.01.01| Import Data
# =============================================================================
# Load product level metadata dataset
with open(Path(working_directory + data_path + products_path), 'rb')  as pickle_file:
    product_data = pickle.load(pickle_file)
    product_data = pd.DataFrame(product_data)

gc.collect()

# Load product recommendations
with open(Path(working_directory + data_path + product_recs_orig_path), 'rb') as pickle_file:
    product_recs = pickle.load(pickle_file)
    product_recs = pd.DataFrame(product_recs)

gc.collect()


# Load user recommendations
with open(Path(working_directory + data_path + user_recs_orig_path), 'rb') as pickle_file:
    user_recs = pickle.load(pickle_file)
    user_recs = pd.DataFrame(user_recs)

gc.collect()

print('Script: 01.01.01 [Import Data] completed')


# =============================================================================
# 01.02.01| Select product columns
# =============================================================================
product_data_sub = product_data[['asin','title','category2_t','category3_t','price_t','numberReviews','meanStarRating','imUrl']]
# universally only taking the first 60 characters for the title
product_data_sub['title'] = product_data_sub['title'].str[:60]

print('Script: 01.02.01 [Select product columns] completed')


# =============================================================================
# 01.03.01| Add relevant metadata to product predictions
# =============================================================================
# we have to do two joins to the product data because we have the original and recommended products and need metadata for both
# recommended products
product_recs_enhanced1 = pd.merge(product_recs, product_data_sub, how='left', left_on=['recommended_product_id'], right_on=['asin'])

product_recs_enhanced1.rename(columns={'title':'Recommended Product',
                                       'predicted_rating': 'Predicted Rating'}, inplace=True)

# original products
product_recs_enhanced2 = pd.merge(product_recs_enhanced1['original_product_id'], product_data_sub[['asin','title']], how='left', left_on=['original_product_id'], right_on=['asin'])

product_recs_enhanced2.rename(columns={'title':'Original Product',
                                       'asin': 'Original Product Id'}, inplace=True)
    
# need to take distinct so as not to duplicate the rows when we join back
# the number of rows is equal to the number of recs per product
product_recs_enhanced2.drop_duplicates(inplace=True)
    
# put it all together
product_recs_enhanced = pd.merge(product_recs_enhanced1, product_recs_enhanced2, how='inner', left_on=['original_product_id'], right_on=['Original Product Id'])

# verify no rows were lost
if(product_recs_enhanced.shape[0]==product_recs.shape[0] is False):
    sys.exit("Product recommendation data prep lost data")

# remove unnecessary columns
columns_to_remove = ['recommended_product_id_int','recommended_product_id',
                     'original_product_id_int','original_product_id_x',
                     'original_product_id_y','asin']
product_recs_enhanced = product_recs_enhanced.drop(columns_to_remove, axis=1)

# rename columns
product_recs_enhanced.rename(columns={'category2_t':'Product Category 2',
                                      'category3_t':'Product Category 3',
                                      'price_t':'Price',
                                      'imUrl':'Product URL',
                                      'numberReviews':'Number of Reviews',
                                      'meanStarRating':'Average Rating'}, inplace=True)

print('Script: 01.03.01 [Add relevant metadata to product predictions] completed')


# =============================================================================
# 01.03.02| Transform Rank Order Column
# =============================================================================
product_recs_enhanced["Rank Order"] = product_recs_enhanced.groupby('Original Product Id')["Predicted Rating"].rank("dense", ascending=False)

# have to sort values so thank rank 1 is first for each product
product_recs_enhanced = product_recs_enhanced.sort_values(by=['Original Product Id','Rank Order'], ascending=True)

product_recs_enhanced = product_recs_enhanced.drop('Predicted Rating', axis=1)

# reorder columns
product_recs_enhanced = product_recs_enhanced[['Original Product Id','Original Product',
                                               'Rank Order','Recommended Product',
                                               'Product Category 2','Product Category 3',
                                               'Price','Number of Reviews',
                                               'Average Rating','Product URL']]

print('Script: 01.03.02 [Transform rank order column] completed')


# =============================================================================
# 01.03.03| Pickle Product Predictions
# =============================================================================
product_recs_enhanced.to_pickle(Path(working_directory + dash_data_path + product_recs_path))

print('Script: 01.03.03 [Pickle Product Predictions] completed')


# =============================================================================
# 01.04.01| Add relevant metadata to user predictions
# =============================================================================
user_recs_enhanced = pd.merge(user_recs, product_data_sub, how='left', left_on=['recommended_product_id'], right_on=['asin'])

# rename columns
user_recs_enhanced.rename(columns={'original_reviewerID':'Reviewer Id',
                                   'title':'Recommended Product',
                                   'predicted_rating':'Predicted Rating',
                                   'category2_t':'Product Category 2',
                                   'category3_t':'Product Category 3',
                                   'price_t':'Price',
                                   'imUrl':'Product URL',
                                   'numberReviews':'Number of Reviews',
                                   'meanStarRating':'Average Rating'}, inplace=True)

# remove unnecessary columns
columns_to_remove = ['original_reviewerID_int','recommended_product_id_int',
                     'asin','recommended_product_id']
user_recs_enhanced = user_recs_enhanced.drop(columns_to_remove, axis=1)

# verify no rows were lost
if(user_recs_enhanced.shape[0]==user_recs.shape[0] is False):
    sys.exit("User recommendation data prep lost data")

print('Script: 01.04.01 [Add relevant metadata to user predictions] completed')


# =============================================================================
# 01.04.02| Transform Rank Order Column
# =============================================================================
user_recs_enhanced["Rank Order"] = user_recs_enhanced.groupby('Reviewer Id')["Predicted Rating"].rank("dense", ascending=False)

# have to sort values so thank rank 1 is first for each reviewer
user_recs_enhanced = user_recs_enhanced.sort_values(by=['Reviewer Id','Rank Order'], ascending=True)

user_recs_enhanced = user_recs_enhanced.drop('Predicted Rating', axis=1)

# reorder columns
user_recs_enhanced = user_recs_enhanced[['Reviewer Id',
                                         'Rank Order','Recommended Product',
                                         'Product Category 2','Product Category 3',
                                         'Price','Number of Reviews',
                                         'Average Rating','Product URL']]

print('Script: 01.04.02 [Transform rank order column] completed')


# =============================================================================
# 01.03.03| Pickle User Predictions
# =============================================================================
user_recs_enhanced.to_pickle(Path(working_directory + dash_data_path + user_recs_path))

print('Script: 01.04.03 [Pickle User Predictions] completed')


# =============================================================================
# 01.05.01| Create Top 10 Products Data Frame
# =============================================================================
# top 10 products
top_10_products = product_data_sub.sort_values('numberReviews', ascending=False).head(10)[['title','numberReviews','price_t','category2_t','category3_t']]
top_10_products = top_10_products.sort_values('numberReviews', ascending=True) 

print('Script: 01.05.01 [Create Top 10 Products Data Frame] completed')


# =============================================================================
# 01.05.02| Pickle Top 10 Products
# =============================================================================
top_10_products.to_pickle(Path(working_directory + dash_data_path + top_10_products_path))

print('Script: 01.05.02 [Pickle Top 10 Products] completed')