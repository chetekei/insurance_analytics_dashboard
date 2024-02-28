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
df['Count'] = 1

df['Frequency'] = np.bool_(1)

# convert timestamp to datetime
df['timestamp'] = pd.to_datetime(df['Time of Loss'])

 # Main Streamlit app code
def main(): 
    # Create a sidebar to switch between views
    view = st.sidebar.radio("Select", ["Dashboard"])

    if view == "Dashboard":

        months = df.groupby('Month')['Count'].sum()
        day = df.groupby('Day')['Count'].sum()
        claims = df.groupby('Claim Type')['Count'].sum()

        # Sort by the sum of Count in descending order
        result = months.sort_values(by='Count', ascending=False)
        result1 = day.sort_values(by='Count', ascending=False)        
        result2 = claims.sort_values(by='Count', ascending=False)

        # Get the class with the highest sum
        highest_month = result.head(1)
        highest_day = result1.head(1)
        highest_class = result2.head(1)

        month_name = highest_month['Month'].values[0]
        day_name = highest_day['Day'].values[0]
        class_name = highest_class['Claim Type'].values[0]



        st.markdown(
                        f'<div style= "display: flex; flex-direction: row;">'  # Container with flex layout
                        f'<div style="background-color: #f19584; padding: 10px; border-radius: 10px; width: 250px; margin-right: 20px;">'
                        f'<strong style="color: black; font-size: 12px">MOST FREQUENT CLAIM TYPE</strong> <br>'  
                        f"<br>"
                        f"{class_name}<br>"
                        f'</div>'
                        f'<div style="background-color: #FFE599; padding: 10px; border-radius: 10px; width: 250px; margin-right: 20px;">'
                        f'<strong style="color: black; font-size: 12px">MOST FREQUENT CLAIM MONTH</strong> <br>'
                        f"<br>"
                        f"{month_name}<br>"
                        f'</div>'                
                        f'<div style="background-color: #a8e4a0; padding: 10px; border-radius: 10px; width: 250px; margin-right: 20px;">'
                        f'<strong style="color: black; font-size: 12px">MOST FREQUENT DAY</strong> <br>'  
                        f"<br>"
                        f"{day_name}<br>"
                        f'</div>'                    
                        f'</div>',
                        unsafe_allow_html=True
                    )

               
          
   


    
