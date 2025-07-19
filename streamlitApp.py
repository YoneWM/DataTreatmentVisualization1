import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from Components.overviewETC import overviewTabs,businessView,valAbvMarker,salesView

#region 1STDATA MANIP
@st.cache_resource
def getData():
    #1st - load data and first look
    df = pd.read_excel("Financial Data Clean.xlsx")

    df.drop("Currency",axis=1,inplace=True)
    df = df[df["Year"]>=2021]

    return df

df = getData()

#2nd - df subsets for each YEAR and Scenario ("Budget","Forecast","Actuals")
df_Actuals=[] #[2021,2022]

for i in range(2021,2023):
    df_Actuals.append(df[(df["Year"] == i) & (df["Scenario"] == "Actuals")])

df_Budget2023=df[(df["Year"]==2023) & (df["Scenario"]=="Budget")]
df_Forecast2023=df[(df["Year"]==2023) & (df["Scenario"]=="Forecast")] 

#3rd - sum the monthly values and group by Account (9 unique)
for m in range(2):
    df_Actuals[m] = df_Actuals[m].groupby("Account").sum(numeric_only=True).drop("Year", axis=1)

df_Budget2023 = df_Budget2023.groupby("Account").sum(numeric_only=True).drop("Year", axis=1)
df_Forecast2023 = df_Forecast2023.groupby("Account").sum(numeric_only=True).drop("Year", axis=1)

#4th - subset for each ACCOUNT (9 unique)
Accounts_Budget2023 = []
Accounts_Forecast2023 = []
Accounts_Actuals2021 = []
Accounts_Actuals2022 = []


for index,row in df_Budget2023.iterrows():
    Accounts_Budget2023.append(row)

for index,row in df_Forecast2023.iterrows():
    Accounts_Forecast2023.append(row)

for index,row in df_Actuals[0].iterrows(): #2021
    Accounts_Actuals2021.append(row)

for index,row in df_Actuals[1].iterrows(): #2022
    Accounts_Actuals2022.append(row)

#endregion

#region VISUALIZATION
st.set_page_config(page_title="Data Training",layout="wide",page_icon="📈")
st.title("Sample Financial Data 2021-2023",width="stretch")

overviewTabs(Accounts_Actuals2021,Accounts_Actuals2022,Accounts_Budget2023,Accounts_Forecast2023)

st.divider()

st.subheader("Business Analysis")
businessView(df)

_="""OBS: 2nd data manip in businessView() at the file named overviewETC.py"""

st.divider()

st.subheader("Sales Analysis")

salesView(df)