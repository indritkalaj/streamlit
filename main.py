
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
st.info('The following data are for internal use only! Please do not distribute the data outside the group of interest!')


#AgGrid(df, height=500)
st.write('\n')
st.write('\n')
st.subheader('Show / Hide RAW Data 💹' )



months = ("January","February","March","April","May","June","July","August","September","October","November","December")
years = ("2020","2021","2022")
mtd = st.selectbox('Select month as filter',months)
ytd = st.selectbox('Select year as filter', years)
month_selection = months.index(mtd) + 1

sql_conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=ALTIRDT0407WZ2;DATABASE=al_datathon_amz;Trusted_Connection=yes')
query = '''
SELECT * FROM [al_datathon_amz].[dbo].[raw_data] where [activity_month] = 8 and [activity_date] like '%2020%'
'''
query = query.replace( "8", str(month_selection)).replace("2020", str(ytd) )
df = pd.read_sql(query, sql_conn)


is_check = st.checkbox("Display Table")
st.text('This checkbox will show a preview of the data stored on the DB. This takes some seconds to load. Please be patient.')
if is_check:
    #st.text('The data can be sorted by column and columns can be filtered by value.')
    #AgGrid(df, height=500, sideBar=True, dndSource=True, suppressCsvExport=False)
    st.write(df)
file_name = "raw data.csv"
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
st.info('Use the filters below for the pivot table only!')

rap_df_pivot = df.copy()

rap_df_pivot['RAP'] = (rap_df_pivot['hmd_response_yes_adjusted'].astype('int64') / (rap_df_pivot['hmd_response_yes_adjusted'].astype('int64') + rap_df_pivot['hmd_response_no_adjusted'].astype('int64')))
rap_df_pivot['RAP'] = pd.Series(["{0:.2f}%".format(val * 100) for val in rap_df_pivot['RAP']])
rap_df_pivot['CCX_U'] = (rap_df_pivot['understandability_45count'].astype('int64') / rap_df_pivot['understandability_12345count'].astype('int64'))
rap_df_pivot['CCX_U'] = pd.Series(["{0:.2f}%".format(val * 100) for val in rap_df_pivot['CCX_U']])


#rap_df_pivot = rap_df_pivot.style.format({'RAP': "{:.2f}",'CCX_U': "{:.2f}"})
#rap_df_pivot = pd.pivot_table(rap_df_pivot, index=['manager_login_lvl_1', 'login_name'] )


############################################################################################

#############################################################################################


st.cache()
contact_type = list(rap_df_pivot['contact_type'].drop_duplicates())
#agent_name = list(rap_df_pivot['login_name'].drop_duplicates())
team_manager = list(rap_df_pivot['manager_login_lvl_1'].drop_duplicates())
activity_month = list(rap_df_pivot['activity_month'].drop_duplicates())
activity_week = list(rap_df_pivot['activity_week'].drop_duplicates())
activity_date = list(rap_df_pivot['activity_date'].drop_duplicates())

#st.sidebar.subheader('Use this filters for the pivot table only!')

contact_type_choice = st.multiselect('Contact Type: ', contact_type, default=contact_type)
team_manager_choice = st.multiselect('Team Leader Name: ', team_manager)
#agent_name_choice = st.multiselect('Agent Name: ', agent_name, default=[])
activity_month_choice = st.multiselect('Month:', activity_month)
activity_week_choice = st.multiselect('Week:', activity_week)
activity_date_choice = st.multiselect('Date:', activity_date)

#rap_df_pivot = rap_df_pivot.loc[rap_df_pivot['contact_type'].isin(contact_type_choice)]
rap_df_pivot = rap_df_pivot[
    (rap_df_pivot.contact_type.isin(contact_type_choice)) &
    (rap_df_pivot.manager_login_lvl_1.isin(team_manager_choice)) &
    (rap_df_pivot.activity_month.isin(activity_month_choice)) &
    (rap_df_pivot.activity_week.isin(activity_week_choice)) &
    (rap_df_pivot.activity_date.isin(activity_date_choice))
]
#rap_pivot_df = rap_pivot_df[rap_pivot_df['contact_type'] == 'phone']

st.dataframe(rap_df_pivot)

#############################################################################################


#############################################################################################


#############################################################################################





#############################################################################################
#  https://discuss.streamlit.io/t/filter-dataframe-by-selections-made-in-select-box/6627/14


#############################################################################################