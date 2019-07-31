# Forecasting Model for Oklahoma
sagemakerjul312019
July312019 - Sagemaker project

To predict the total daily incoming solar energy at 98 Oklahoma Mesonet sites

# Goals

* Greater than 70% accuracy.
* Forecasting of energy production at those sites on a 24 hour basis.


# Datasets
Forecasting data sets from Kaggle: - https://www.kaggle.com/c/3354/download-all

Includes:

* Incoming Solar energy data per site from 1994-2007
* GEFS training data
* GEFS elevation data
* Each station's latitude, longitude and elevation.

# Modeling Strategy

* Start with mw energy production data for each site
* Link with weather data
* Link with station elevation data

# Stretch Goals

Use the forecasting model to run forecasts on all 50 states to predict what the solar energy production would look like for each state. This will help in expansion of solar energy plants to the states and regions most suitable for solar energy production.
