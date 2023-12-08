import time  # to simulate a real time data, time loop

import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
import streamlit as st  # 🎈 data web app development
import folium
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score

st.set_page_config(
    page_title="Real-Time Data Science Dashboard",
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
        title="Plant Locations",
        mapbox_style="open-street-map",  # You can choose a different mapbox style
        height=600,
        width=1000,
        center=taiwan_center,
        zoom=6,  # You can adjust the zoom level
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
st.title("The Centre for Energy Research and Air")

# top-level filters
job_filter = st.selectbox("Select Plant", pd.unique(df["facility_id"]))

# creating a single-element container
placeholder = st.empty()

# near real-time / live feed simulation
for seconds in range(200):

    df["age_new"] = 2
    df["balance_new"] = 2

    # creating KPIs
    avg_age = np.mean(df["age_new"])


    balance = np.mean(df["balance_new"])

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
            value=sum(data[data['PowerPlantID']==job_filter]['value']),
        )


        st.markdown("### Plant Locations")
        st.plotly_chart(plot_points_on_map(df, 0, len(df), 'latitude', 'longitude'))
        # st.write(fig_map)
        
        st.markdown("### visual inspection of prediction of emission vs actual value of emission")

        # Plotly Express for the scatter plot
        fig12 = plt.figure(figsize=(10, 5))
        fig12.suptitle("visual inspection of prediction of emission (y_pred) vs measured value of emission (y_test)")
        ax1 = fig12.add_subplot(111)
        ax1.plot(range(0,len(pred['Actual'])), pred['Actual'], label='Actual', color='b')
        #ax12 = ax1.twinx()
        ax1.plot(range(0,len(pred['Predicted'])), pred['Predicted'], label='Predicted', color='r') 
        ax1.legend(); #; ax12.legend()

        # Show the plot
        st.plotly_chart(fig12)

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


        st.markdown("### Detailed Data View")
        st.dataframe(data)
        time.sleep(1)