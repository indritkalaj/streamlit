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


st.title('Testing Project')
df = pd.DataFrame(pd.read_csv(r'C:\Users\kalaj.5\Desktop\Manager_login_lvl_1,_1632475103329 - Copy.csv'))
st.text('Dummy Description')
sql_conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=ALTIRDT0407WZ2;DATABASE=al_datathon_amz;Trusted_Connection=yes')
query = "SELECT * FROM [al_datathon_amz].[dbo].[raw_data]"
df = pd.read_sql(query, sql_conn)
AgGrid(df, height=500, fit_columns_on_grid_load=True)