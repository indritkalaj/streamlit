
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

#


st.title('Data Import from DB using Streamlit')
st.text('The following data are for internal use only! Please do not distribute the data outside the group of interest!')


df = pd.DataFrame(pd.read_csv(r'C:\Users\kalaj.5\Desktop\Manager_login_lvl_1,_1632475103329 - Copy.csv'))
sql_conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=ALTIRDT0407WZ2;DATABASE=al_datathon_amz;Trusted_Connection=yes')
query = "SELECT * FROM [al_datathon_amz].[dbo].[raw_data] where [activity_month] = 9;"

df = pd.read_sql(query, sql_conn)
#AgGrid(df, height=500)

is_check = st.checkbox("Display Table")
if is_check:
    #st.text('The data can be sorted by column and columns can be filtered by value.')
    #AgGrid(df, height=500, sideBar=True, dndSource=True, suppressCsvExport=False)
    st.write(df)

#############################################################################################

contact_type = df['contact_type'].drop_duplicates()
agent_name = df['login_name'].drop_duplicates()
team_manager = df['manager_login_lvl_1'].drop_duplicates()
activity_week = df['activity_week'].drop_duplicates()
activity_month = df['activity_month'].drop_duplicates()
activity_date = df['activity_date'].drop_duplicates()
df['RAP'] = (df['hmd_response_yes_adjusted'].astype(int)/(df['hmd_response_yes_adjusted'].astype(int) + df['hmd_response_no_adjusted'].astype(int)))
#data_col = data['Data'][(data['Geography'] == Country_choice) & (data['Category'] == Category_choice) & (data['Series'] == Series_choice) & (data['Data Type'] == Data_type_choice)].unique()

contact_type_choice = st.sidebar.selectbox('Contact Type: ', contact_type)
agent_name_choice = st.sidebar.selectbox('Agent Name:', agent_name)
team_manager_choice = st.sidebar.selectbox('Team Leader Name:', team_manager)
activity_week_choice = st.sidebar.selectbox('Week:', activity_week)
activity_month_choice = st.sidebar.selectbox('Month:', activity_month)
activity_date = st.sidebar.selectbox('Date:', activity_date)

st.write()

#############################################################################################



#############################################################################################
#  https://discuss.streamlit.io/t/filter-dataframe-by-selections-made-in-select-box/6627/14
#


Data_filtering = []
contact_type = df.contact_type.unique()
contact_type_choice = Data_filtering[0].selectbox("Contact Type: ", contact_type)

# CATEGORY - get all row values in the category column that are in the country column
agent_name = df['agent_name'].loc[df['contact_type'] == contact_type_choice].unique()
contact_type_choice = Data_filtering[1].selectbox("Agent Name: ", agent_name)


# SERIES - get all series row values that are in the category column
series = data.Series.loc[data['Category']==Category_choice].unique()
Series_choice = Data_filtering[2].radio('Sequential Data type', series)


# filter another column called 'Data' which I will use as columns for the reshaped dataframe to display the dataframe and then chart the selected data. Here the 'Data' column will be displayed based on the choices made in the above.
data_col = data['Data'][(data['Geography']==Country_choice) & (data['Category']==Category_choice) & (data['Series']==Series_choice) & (data['Data Type']==Data_type_choice)].unique()

# Create a pivot table to reshape the dataframe into a 2d dataframe which I can use the data_col variable choices to select the filtered data from.
Trans_data=data.pivot_table(index='Date', columns='Data', values='Values').rename_axis(None, axis=1)

#############################################################################################