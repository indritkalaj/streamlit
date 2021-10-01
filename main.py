import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')


from sklearn import preprocessing
from sklearn.model_selection import train_test_split

st.title('Classification Using A Custom NN Model')

import numpy as np
import pandas as pd
import streamlit as st

df =pd.DataFrame({
            "source_number":[11199,11328,11287,32345,12342,1232,13456,123244,13456],
             "location":["loc2","loc1","loc3","loc1","loc2","loc2","loc3","loc2","loc1"],
             "category":["cat1","cat2","cat1","cat3","cat3","cat3","cat2","cat3","cat2"],
             })

is_check = st.checkbox("Display Data")
if is_check:
    st.table(df)


columns = st.sidebar.multiselect("Enter the variables", df.columns)
st.write("You selected these columns", columns)

sidebars = {}
for y in columns:
    ucolumns=list(df[y].unique())
    sidebars[y+"filter"]=st.sidebar.multiselect('Filter '+y, ucolumns)

st.write(sidebars)
(sidebars[1].str.startswith(sidebars[1][1]) | (sidebars[2].str.startswith(sidebars[2][2]))),['source_number','location','category']])