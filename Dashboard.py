import streamlit as st
from datetime import datetime, timedelta
from core import Core


st.set_page_config(layout='wide')


start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
end_date = datetime.now().strftime("%Y-%m-%d")

obj = Core()
obj.set_metrics()

st.title("Asteroids - Near Earth Object Web Service Dashboard")
st.markdown("*A 7-day rolling window dashboard for Near Earth Objects. Source: NASA*")

metric_col1, metric_col2 = st.columns(2)

metric_col1.metric("Near Earth Objects", obj.neos)
metric_col2.metric("Potentially Hazardous", obj.hazard)
metric_col1.metric("Flagged by Sentry", obj.sentry)
metric_col2.metric("Avg H Value", obj.h_mag)
metric_col1.metric("Min Estimated Diameter", obj.min_diam + " m")
metric_col2.metric("Max Estimated Diameter", obj.max_diam + " m")
metric_col1.metric("Min Miss Distance", obj.min_miss + " km")
metric_col2.metric("Max Miss Distance", obj.max_miss + " km")
metric_col1.metric("Min Relative Velocity", obj.min_vel + " km/s")
metric_col2.metric("Max Relative Velocity", obj.max_vel + " km/s")