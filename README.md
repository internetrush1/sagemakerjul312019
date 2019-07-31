# Forecasting Model for Oklahoma
sagemakerjul312019
July312019 - Sagemaker project

To predict the total daily incoming solar energy at 98 Oklahoma Mesonet sites

# Goals

* Greater than 70% accuracy.
* Forecasting of energy production at those sites on a 24 hour basis.


# Datasets
Forecasting data sets from Kaggle: - 

Includes:

* Incoming Solar energy data per site from 1994-2007 TODO LINK)
* GEFS training data (TODO LINK)
* GEFS elevation data (TODO LINK)
* Each station's latitude, longitude and elevation. (TODO LINK)

# Modeling Strategy

* Start with mw energy production data for each site
* Link with weather data
* Link with station elevation data
