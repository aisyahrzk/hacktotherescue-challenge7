# EcoForecast: Forecasting Emissions for The Better

## Overview

This project aims to predict NOx emissions from power plants in Taiwan by leveraging a diverse set of datasets. Two primary types of datasets are provided: raster data in GeoTIFF format (satellite and weather data) and CSV files containing information on Taiwan's power plants.

### Data Details

- **Temporal Coverage:** 1 Mar 2019 - 30 Sep 2023
- **Geospatial Reference:** WGS 84 coordinate system (EPSG 4326)
- **Resolution:** Latitude-longitude grid with 0.025° resolution covering Taiwan (119°E, 21°N; 123°E, 27°N)
- **Raster Data:** 1 file/day

### Datasets

1. **Taiwan Power Plants:**
   - Provides information on power plants in Taiwan, including name, location, and a unique identifier ("facility_id").
   - File: `Taiwan_powerplants.csv`

2. **Ground Truth for NOx Emissions:**
   - Hourly NOx emissions for power plants in kg per hour.
   - File: `Taiwan_nox_emissions.csv`

3. **Satellite: NO2 Measurement (TROPOMI):**
   - Provides NO2 measurements from ESA's TROPOMI satellite.
   - Daily files: `satellite/NO2/no2_kgm2_<YYYYMMDD>.tiff`

4. **Satellite: Cloud Fraction:**
   - Cloud fraction derived from satellite measurements.
   - Daily files: `satellite/cloud_fraction/cloud_fraction_<YYYYMMDD>.tiff`

5. **Weather Data:**
   - Various meteorological variables, including wind components, temperature, relative humidity, boundary layer height, and solar radiation.
   - Daily files: `weather/<variable>/<var>_<units>_<YYYYMMDD>.tiff`

6. **NO2 Flux:**
   - NO2 net transport or flux divergence calculated from satellite NO2 and wind data.
   - Daily files: `NO2flux/no2flux_kgm2s_<YYYYMMDD>.tiff`

### Model Usage

The Emission Prediction Project employs the XGBoost regressor (`XGBRegressor`) to predict NOx emissions based on the provided GeoTIFF data. The XGBoost model is known for its performance and efficiency in handling complex relationships within datasets.

### Jupyter Notebook

A Jupyter notebook is provided with examples for reading and visualizing the data, as well as implementing the XGBoost regression model for emission prediction.

## Project Structure

- **Notebooks:** Jupyter notebooks or Python scripts for data exploration, preprocessing, feature engineering, model training (XGBoost), and evaluation.
- **Models:** model.pkl contains the xgboost regressor model.
- **Requirements:** `requirements.txt` specifying the Python libraries and dependencies needed to run the code successfully.
