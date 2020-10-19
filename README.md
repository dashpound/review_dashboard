# Amazon Recommendation Engine

Deployed here using a hobby instance of Heroku: https://cognoclick.herokuapp.com/

Since its inception nearly 25 years ago, Amazon has been focused on delivering a world class customer experience. In a world where consumer choice is paramount, Amazon continues to need better ways to target new and existing customers by presenting them with products they are most likely to purchase. The key to solving this problem lies in one of Amazon’s greatest data assets: customer reviews.

Amazon has a subset of customers who write reviews about their purchased products (reviewers). Reviewers tend to be more engaged with Amazon’s platform, giving Amazon the ability to increase product exposure with this segment. By mining historical reviews for information on product preference and sentiment, Amazon can understand and utilize reviewer preference to develop a more personalized product recommendation experience for each reviewer. 

Disclaimer: This project was completed as part of the MSDS 498 Capstone Project course within the Northwestern University. All data, dashboards, and insights used throughout this project are completely simulated and not in any way connected to or a reﬂection of Amazon. Please do not duplicate or distribute outside of the context of this course. 

## Codebase

This is the codebase for the dashboard.
The codebase for the recommendation engine is located here:
[https://github.com/dashpound/capstone](https://github.com/dashpound/capstone)

This repo is used to generate a dash app that is deployed via Heroku.

### Prerequisites

Please see the requirements.txt file for the full list of requirements. 
Note: this data is compressed using git large file storae (git-lfs); when cloning be sure to have it installed.

```
nltk
python3.x
dash==1.4.1  # The core dash backend
dash-daq==0.2.1  # DAQ components (newly open-sourced!)
dash-bootstrap-components
```

## Contributing

* John Kiley
* Brian Merrill
* Hemant Patel
* Julia Rodd

## Note regarding a common error when cloning this codebase
If you are copying this code base, git-lfs is required to properly clone out the pickle files that contain the data.
If you are trying to run and get an error at pd.read_pickle(<PATH_TO_FILE>) its because the pickle file has been compressed in a way that pandas does not recognize.
To fix, install git-lfs and reclone the repo.
Read more about git-lfs here:  https://git-lfs.github.com/
