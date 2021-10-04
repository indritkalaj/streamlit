
### If the data table exeeds 50 Mb of data, edit the following line:
## "C:\Users\xxxxx\Desktop\streamlit\venv\streamlit\Lib\site-packages\streamlit\server\server_util.py"

import base64
import io
from io import BytesIO
import pyodbc
import sqlalchemy as sal
from sqlalchemy import create_engine
import pandas as pd
import streamlit as st
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from sqlalchemy import Table, MetaData, Column, Integer
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
import st_aggrid
from st_aggrid import AgGrid
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
import streamlit as st
import pyodbc



st.set_page_config(layout="wide")

st.title('Data Import from DB using Streamlit')
st.text('The following data are for internal use only! Please do not distribute the data outside the group of interest!')


# sql_conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=ALTIRDT0407WZ2;DATABASE=al_datathon_amz;Trusted_Connection=yes')
# query = "SELECT * FROM [al_datathon_amz].[dbo].[raw_data];"
# df = pd.read_sql(query, sql_conn)

#AgGrid(df, height=500)
st.write('\n')
st.write('\n')
st.subheader('Show / Hide RAW Data 💹' )

months = ("January","February","March","April","May","June","July","August","September","October","November","December")
mtd = st.selectbox('Select month as filter',months)
month_selection = months.index(mtd) + 1

sql_conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=ALTIRDT0407WZ2;DATABASE=al_datathon_amz;Trusted_Connection=yes')
query = "SELECT * FROM [al_datathon_amz].[dbo].[raw_data] where [activity_month] = 8"
query = query.replace("8", str(month_selection))
df = pd.read_sql(query, sql_conn)


is_check = st.checkbox("Display Table")
st.text('This checkbox will show a preview of the data stored on the DB. This takes some seconds to load. Please be patient.')
if is_check:
    #st.text('The data can be sorted by column and columns can be filtered by value.')
    #AgGrid(df, height=500, sideBar=True, dndSource=True, suppressCsvExport=False)
    st.write(df)
file_name = "df.csv"
file_path = f"./{file_name}"
df.to_csv(file_path)
# Create Download Button
file_bytes = open(file_path, 'rb')
st.download_button(label='Download RAW Data',
                   data=file_bytes,
                   file_name=file_name,
                   key='download_df')
file_bytes.close()
st.text('The download button will download all the data from the DB where the datas are stored!')
#############################################################################################

#############################################################################################
st.write('\n')
st.write('\n')
st.subheader('Descriptive Statistics on each column 📊' )

st.subheader('Show / Hide Stats' )

is_check_stats = st.checkbox("Display Stats")
st.text('This checkbox will show a preview of statistics related to the raw data columns.')
if is_check_stats:
    #st.text('The data can be sorted by column and columns can be filtered by value.')
    #AgGrid(df, height=500, sideBar=True, dndSource=True, suppressCsvExport=False)
    # removing null values to avoid errors
    df_stats = df.copy()
    df_stats.dropna(inplace=True)
    # percentile list
    perc = [.20, .40, .60, .80]
    # list of dtypes to include
    include = ['object', 'float', 'int']
    # calling describe method
    desc = df_stats.iloc[:, 21:35].copy()
    desc = desc.astype(int).describe()
    # display
    st.write(desc)
file_name = "df_stats.csv"
file_path = f"./{file_name}"
desc = df.iloc[:, 21:35].copy()
desc = desc.astype(int).describe()
desc.to_csv(file_path)
# Create Download Button
file_bytes = open(file_path, 'rb')
st.download_button(label='Download Stats Data',
                   data=file_bytes,
                   file_name=file_name,
                   key='download_df')
file_bytes.close()
st.text('The download button will download stats over the data table.')


############################################################################################
st.write('\n')
st.write('\n')
st.subheader('Pivoting the RAW Data below:' )


sql_conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=ALTIRDT0407WZ2;DATABASE=al_datathon_amz;Trusted_Connection=yes')
query = "SELECT * FROM [al_datathon_amz].[dbo].[raw_data] where [activity_month] = 8"
query = query.replace("8", str(month_selection))
rap_df = pd.read_sql(query, sql_conn)


rap_df['RAP'] = (rap_df['hmd_response_yes_adjusted'].astype('int64') / (rap_df['hmd_response_yes_adjusted'].astype('int64') + rap_df['hmd_response_no_adjusted'].astype('int64')))
rap_df['CCX_U'] = (rap_df['understandability_45count'].astype('int64') / rap_df['understandability_12345count'].astype('int64'))
rap_df['Channel'] = rap_df['contact_type']


rap_df = rap_df.style.format({'RAP': "{:.2f}",'CCX_U': "{:.2f}"})
st.dataframe(rap_df)
rap_df_pivot = pd.pivot_table(rap_df, index=['manager_login_lvl_1', 'login_name'] )


############################################################################################

#############################################################################################


st.cache()
contact_type = list(rap_df['Channel'].drop_duplicates())
agent_name = list(rap_df['login_name'].drop_duplicates())
team_manager = list(rap_df['manager_login_lvl_1'].drop_duplicates())
activity_week = list(df['activity_week'].drop_duplicates())
activity_month = list(df['activity_month'].drop_duplicates())
activity_date = list(df['activity_date'].drop_duplicates())
# #data_col = data['Data'][(data['Geography'] == Country_choice) & (data['Category'] == Category_choice) & (data['Series'] == Series_choice) & (data['Data Type'] == Data_type_choice)].unique()
st.sidebar.subheader('Use this filters for the pivot table only!')
#contact_type_choice = []
#contact_type_choice = st.sidebar.multiselect('Contact Type: ', contact_type, default=contact_type)
# agent_name_choice = st.sidebar.selectbox('Agent Name:', agent_name)
# team_manager_choice = st.sidebar.selectbox('Team Leader Name:', team_manager)
# activity_week_choice = st.sidebar.selectbox('Week:', activity_week)
# activity_month_choice = st.sidebar.selectbox('Month:', activity_month)
# activity_date = st.sidebar.selectbox('Date:', activity_date)

#rap_df_pivot = rap_df_pivot.loc[rap_df_pivot['Channel'].isin(contact_type_choice)]
#rap_pivot_df = rap_pivot_df[rap_pivot_df['contact_type'] == 'phone']

st.dataframe(rap_df_pivot)

#############################################################################################


#############################################################################################


#############################################################################################





#############################################################################################
#  https://discuss.streamlit.io/t/filter-dataframe-by-selections-made-in-select-box/6627/14


#############################################################################################