import time
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
import folium
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score
pd.set_option('display.float_format', '{:.25f}'.format)

st.set_page_config(
    page_title="Plant Emission Dashboard",
    page_icon="✅",
    layout="wide",
)


def plot_points_on_map(dataframe, begin_index, end_index, latitude_column, longitude_column):
    df = dataframe.iloc[begin_index:end_index]
    taiwan_center = {'lat': 23.6978, 'lon': 120.9605}

    fig = px.scatter_mapbox(
        df,
        lat=latitude_column,
        lon=longitude_column,
        text='name',
        mapbox_style="open-street-map",
        height=600,
        width=1000,
        center=taiwan_center,
        zoom=6,
    )

    return fig


# read csv from a github repo
dataset_url = "https://raw.githubusercontent.com/aisyahrzk/hacktotherescue-challenge7/master/powerplant.csv"
dataset_url2 = "https://raw.githubusercontent.com/aisyahrzk/hacktotherescue-challenge7/master/output.csv"
dataset_url3 = "https://raw.githubusercontent.com/aisyahrzk/hacktotherescue-challenge7/master/prediction_test.csv"

# read csv from a URL
@st.cache_data
def get_data() -> pd.DataFrame:
    return pd.read_csv(dataset_url)

@st.cache_data
def get_data2() -> pd.DataFrame:
    return pd.read_csv(dataset_url2)

@st.cache_data
def get_data3() -> pd.DataFrame:
    return pd.read_csv(dataset_url3)


df = get_data()
data = get_data2()
pred = get_data3()


# dashboard title
st.title("EcoForecast: Predicting Emissions for The Better \n Challenge 7")

# top-level filters
job_filter = st.selectbox("Select Plant", pd.unique(df["facility_id"]))

# creating a single-element container
placeholder = st.empty()

# near real-time / live feed simulation

with placeholder.container():

    # create three columns
    kpi1, kpi2, kpi3 = st.columns(3)

    # fill in those three columns with respective metrics or KPIs
    kpi1.metric(
        label="Total Plants ⏳",
        value=round(len(df['facility_id'])),
    )
    kpi3.metric(
        label="Current Plant Emission",
        value=sum(data[data['PowerPlantID'] == job_filter]['value']),
    )

    st.markdown("### Plant Locations")
    st.plotly_chart(plot_points_on_map(df, 0, len(df), 'latitude', 'longitude'))

    st.markdown("### Detailed Data View")
    data['NO2'] = data['NO2'].astype(float)
    displayed_data = data[data['PowerPlantID'] == job_filter].drop(columns=['date'])

    csv_export = displayed_data.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Data as CSV",
        data=csv_export,
        file_name="displayed_data.csv",
        key="dwnld",
    )
    st.dataframe(displayed_data)

    # Allow download of the displayed dataframe


    st.markdown("### Model Prediction Result")

    # create three columns
    rmse, r2 = st.columns(2)

    # fill in those three columns with respective metrics or KPIs
    rmse.metric(
        label="RMSE Overall ⏳",
        value=np.sqrt(mean_squared_error(pred['Actual'], pred['Predicted'])),
    )
    r2.metric(
        label="Overall R2",
        value=r2_score(pred['Actual'], pred['Predicted']),
    )

    st.markdown("### Visual Inspection of Prediction of Emission vs Actual Value of Emission")

    fig12 = plt.figure(figsize=(10, 5))
    fig12.suptitle("Visual Inspection of Prediction of Emission (y_pred) vs Measured Value of Emission (y_test)")
    ax1 = fig12.add_subplot(111)
    ax1.plot(range(0, len(pred['Actual'])), pred['Actual'], label='Actual', color='b')
    ax1.plot(range(0, len(pred['Predicted'])), pred['Predicted'], label='Predicted', color='r')
    ax1.legend()

    st.plotly_chart(fig12)



    st.markdown('## Prediction Plant Emission in Test Set \n **Filtered by Plant Dropdown**')
    csv_export = pred[pred['PowerPlantID'] == job_filter].to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Prediction Data as CSV",
        data=csv_export,
        file_name="prediction.csv",
        key="dwnld_pred",
    )
    st.dataframe(pred[pred['PowerPlantID'] == job_filter])


 


