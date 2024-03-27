import streamlit as st
from datetime import datetime, timedelta
from core import Core
import pandas as pd
import plotly.express as px


st.set_page_config(layout='wide')


start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
end_date = datetime.now().strftime("%Y-%m-%d")

obj = Core()
obj.set_metrics()

tab1, tab2 = st.tabs(["Dashboard", "Raw Data"])

with tab1:

    st.title("Asteroids - Near Earth Object Web Service Dashboard")
    st.markdown("*A 7-day rolling window dashboard for Near Earth Objects. Source: NASA*")

    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

    metric_col1.metric("Near Earth Objects", obj.neos)
    metric_col2.metric("Potentially Hazardous", obj.hazard)
    metric_col3.metric("Flagged by Sentry", obj.sentry)
    metric_col4.metric("Avg H Value", obj.h_mag)
    metric_col1.metric("Min Estimated Diameter", obj.min_diam + " km")
    metric_col2.metric("Max Estimated Diameter", obj.max_diam + " km")
    metric_col3.metric("Min Miss Distance", obj.min_miss + " au")
    metric_col4.metric("Max Miss Distance", obj.max_miss + " au")
    metric_col1.metric("Min Relative Velocity", obj.min_vel + " km/s")
    metric_col2.metric("Max Relative Velocity", obj.max_vel + " km/s")

    bar_col1, bar_col2 = st.columns((2, 1))
    bar_chart_data = obj.get_bar_chart_data()
    bar_chart = px.bar(bar_chart_data, x='Date', y='Object Count', hover_data=['Object Count', 'Potentially Hazardous', 'Sentry Objects', 'Min Estimated Diameter (km)', 'Max Estimated Diameter (km)',
    'Min Miss Distance (au)', 'Max Miss Distance (au)', 'Min Relative Velocity (km/s)', 'Max Relative Velocity (km/s)'])
    bar_col1.plotly_chart(bar_chart, theme='streamlit', use_container_width=True)

    date_options = bar_col2.multiselect(label="Select date(s) to get observed Object IDs", options=pd.unique(bar_chart_data['Date'].values), default=pd.unique(bar_chart_data['Date'].values)[0])
    bar_col2.table(bar_chart_data.loc[bar_chart_data['Date'].isin(date_options)]['Objects'])

    scatter_chart_data = obj.get_scatter_chart_data()
    object_options = st.multiselect(label="Select Object to view close approach graph", options=pd.unique(scatter_chart_data['ID']), default=pd.unique(scatter_chart_data['ID'].values))
    scatter_chart = px.scatter(scatter_chart_data.loc[scatter_chart_data['ID'].isin(object_options)], x='Avg. Relative Velocity (km/s)', y='Avg. Miss Distance (au)', color='Orbiting Body', size='Observation Count',
                                animation_frame='Close Approach Year')
    st.plotly_chart(scatter_chart, theme='streamlit', use_container_width=True)

with tab2:

    data_option = st.selectbox(label="Select data to view", options=['NEO 7-day data', 'NEO Close-approach data'])
    if data_option=='NEO 7-day data':
        st.dataframe(obj.neo_data)
    elif data_option=='NEO Close-approach data':
        st.dataframe(obj.neo_close_data)