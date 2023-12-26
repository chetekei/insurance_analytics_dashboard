import streamlit as st
import plotly as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
from datetime import datetime
import base64

# configuration
st.set_option('deprecation.showfileUploaderEncoding', False)

# title of the app
st.title("Gras Savoye Client Claims Analytics ")

# Add a sidebar
st.sidebar.image('graslogo.jpg', use_column_width=True)
st.sidebar.subheader("Visualization Settings")


# Add demo file download link
demo_data = pd.read_csv('demo_data.csv')
csv = demo_data.to_csv(index=False)
b64 = base64.b64encode(csv.encode()).decode()
href = f'<a href="data:file/csv;base64,{b64}" download="demo_data.csv">Download Demo Claims Data</a>'
st.sidebar.markdown(href, unsafe_allow_html=True)

# Setup file upload
uploaded_file = st.sidebar.file_uploader(
    label="Upload your CSV or Excel file. (200MB max)",
    type=['csv', 'xlsx', 'xls']
)

if uploaded_file is not None:
    try:
        if uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            df = pd.read_excel(uploaded_file, header=8)
        elif uploaded_file.type == "text/csv":
            df = pd.read_csv(uploaded_file, header=8)
    except Exception as e:
        st.write("Error:", e)

                      

# convert date column to month name
df = df.iloc[1:]
df['Month'] = pd.to_datetime(df['Loss Date']).dt.strftime('%B')
df['Day'] = pd.to_datetime(df['Loss Date']).dt.day_name()
df['Year'] = pd.to_datetime(df['Loss Date']).dt.year
df.dropna(subset=['Claim No'], inplace=True)
mask = df['Claim Type'].str.startswith('Work Injury')
df.loc[mask, 'Claim Type'] = 'WIBA'

df['Frequency'] = np.bool_(1)

# convert timestamp to datetime
df['timestamp'] = pd.to_datetime(df['Time of Loss'])

st.sidebar.selectbox("Choose", ['Brief Description of Data Set', 'Top Claim Payout', 'Day of Week', 'Month of Loss'])



        
               
          
   


    
