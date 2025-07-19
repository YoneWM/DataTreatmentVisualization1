import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

@st.fragment
def overviewTabs(Accounts_Actuals2021:list,Accounts_Actuals2022:list,Accounts_Budget2023:list,Accounts_Forecast2023:list):
    """
    st.fragment with tabs containing data overview 
    
    Parameters
    ----------
    lists with pandas.DataFrame items corresponding to each AccountYear
    
    """
    with st.container(border = False):
        st.subheader("Overview")

        tab1,tab2,tab3,tab4 = st.tabs(["Actuals 2021","Actuals 2022","Budget 2023","Forecast 2023"])

        with tab1:
            fig,ax = plt.subplots(ncols=3,nrows=3,layout="constrained")
            fig.suptitle("2021 Actuals by Account")
            fig.set_size_inches(15,5)

            k=0
            for i in range(3):
                for j in range(3):
                    
                    mean_monthly = Accounts_Actuals2021[k].mean()
                    ax[i,j].bar(list(Accounts_Actuals2021[k].index),Accounts_Actuals2021[k].values,color = (.5,0,0) if mean_monthly<0 else (0,0,.5))
                    ax[i,j].set_title(Accounts_Actuals2021[k].name)
                    ax[i,j].set_ylabel("Actuals (USD)")
                    #ax[i,j].set_xlabel("Months")
                    ax[i,j].axhline(y=mean_monthly, linestyle='--', label='Mean')
                    ax[i,j].set_yticks([mean_monthly])
                    k+=1
            st.pyplot(fig)
            plt.close(fig)
        
        with tab2:
            fig,ax = plt.subplots(ncols=3,nrows=3,layout="constrained")
            fig.suptitle("2022 Actuals by Account")
            fig.set_size_inches(15,5)

            k=0
            for i in range(3):
                for j in range(3):
                    
                    mean_monthly = Accounts_Actuals2022[k].mean()
                    ax[i,j].bar(list(Accounts_Actuals2022[k].index),Accounts_Actuals2022[k].values,color = (.5,0,0) if mean_monthly<0 else (0,0,.5))
                    ax[i,j].set_title(Accounts_Actuals2022[k].name)
                    ax[i,j].set_ylabel("Actuals (USD)")
                    #ax[i,j].set_xlabel("Months")
                    ax[i,j].axhline(y=mean_monthly, linestyle='--', label='Mean')
                    ax[i,j].set_yticks([mean_monthly])
                    k+=1
            st.pyplot(fig)
            plt.close(fig)
        
        with tab3:
            fig,ax = plt.subplots(ncols=3,nrows=3,layout="constrained")
            fig.suptitle("2023 Budget by Account")
            fig.set_size_inches(15,5)

            k=0
            for i in range(3):
                for j in range(3):
                    
                    mean_monthly = Accounts_Budget2023[k].mean()
                    ax[i,j].bar(list(Accounts_Budget2023[k].index),Accounts_Budget2023[k].values,color = (.5,0,0) if mean_monthly<0 else (0,0,.5))
                    ax[i,j].set_title(Accounts_Budget2023[k].name)
                    ax[i,j].set_ylabel("Budget (USD)")
                    #ax[i,j].set_xlabel("Months")
                    ax[i,j].axhline(y=mean_monthly, linestyle='--', label='Mean')
                    ax[i,j].set_yticks([mean_monthly])
                    k+=1
            st.pyplot(fig)
            plt.close(fig)
        
        with tab4:
            fig,ax = plt.subplots(ncols=3,nrows=3,layout="constrained")
            fig.suptitle("2023 Forecast by Account")
            fig.set_size_inches(15,5)

            k=0
            for i in range(3):
                for j in range(3):
                    
                    mean_monthly = Accounts_Forecast2023[k].mean()
                    ax[i,j].bar(list(Accounts_Forecast2023[k].index),Accounts_Forecast2023[k].values,color = (.5,0,0) if mean_monthly<0 else (0,0,.5))
                    ax[i,j].set_title(Accounts_Forecast2023[k].name)
                    ax[i,j].set_ylabel("Forecast (USD)")
                    #ax[i,j].set_xlabel("Months")
                    ax[i,j].axhline(y=mean_monthly, linestyle='--', label='Mean')
                    ax[i,j].set_yticks([mean_monthly])
                    k+=1
            st.pyplot(fig)
            plt.close(fig)

#region BusView 2data MANIP -> business_unit/Year focus analysis by Month/Account
@st.fragment
def businessView(df:pd.DataFrame):
    business =["Software","Hardware","Advertising"]
    year = [2021,2022,2023]
    col1,col2 = st.columns(2)

    with col1:
        busSelection = st.pills("Business Unit",selection_mode="single",options=business,default="Software")
        
    with col2:
        userYear = st.selectbox("Select Year",options=year,index=len(year)-1,accept_new_options=False)
    # st.write(f"{busSelection=="Software"} | {userYear}")

    dfbus = df.groupby(["Year","Account","business_unit"]).sum(numeric_only=True)
    dfbus = dfbus.xs((userYear,busSelection),level=["Year","business_unit"])
    dfbus = dfbus.drop("Sales")

    if userYear != 2023:

        fig,ax = plt.subplots(layout = "constrained")
        fig.set_size_inches(12,5)

        btm = np.zeros(12)
        for index,row in dfbus.iterrows():
            ax.bar(x=row.index,height=row.values,label=row.name,bottom=btm)
            btm+=row.values
            
        ax.grid(color="Grey",linewidth=.2,axis="y")
        ax.set_title("Monthly Actuals vs Accounts")
        box = ax.get_position()
        ax.set_position([box.x0, box.y0 + box.height * 0.3, box.width, box.height * 0.9])
        ax.legend(loc='lower left', bbox_to_anchor=(1.0, .4),ncol=1)


        st.pyplot(fig)
        plt.close(fig)
    else:
        #2023 Forecast
        dfbus = df.groupby(["Year","Account","Scenario","business_unit"]).sum(numeric_only=True)
        dfbus = dfbus.xs(("Forecast",userYear,busSelection),level=["Scenario","Year","business_unit"])
        dfbus.drop("Sales",inplace=True)

        fig,ax = plt.subplots(layout="constrained")
        fig.set_size_inches(12,5)

        btm = np.zeros(12)
        for index,row in dfbus.iterrows():
            plt.bar(row.index,row.values,label=row.name,bottom = btm)
            btm+=row.values
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width, box.height])
        
        ax.grid(color="Grey",linewidth=.2,axis="y")
        ax.set_ylabel("Forecast")
        ax.legend(bbox_to_anchor=(1,.7),ncol=1)
        ax.set_title(f"Monthly Forecast vs Account")
        st.pyplot(fig)
        plt.close(fig)

        #2023 Budget
        dfbus = df.groupby(["Year","Account","Scenario","business_unit"]).sum(numeric_only=True)
        dfbus = dfbus.xs(("Budget",userYear,busSelection),level=["Scenario","Year","business_unit"])
        dfbus.drop("Sales",inplace=True)

        fig,ax = plt.subplots(layout="constrained")
        fig.set_size_inches(12,5)

        btm = np.zeros(12)
        for index,row in dfbus.iterrows():
            ax.bar(x=row.index,height=row.values,label=row.name,bottom=btm)
            btm+=row.values
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width, box.height])
        
        
        ax.grid(color="Grey",linewidth=.2,axis="y")
        ax.set_ylabel("Budget")
        ax.legend(bbox_to_anchor=(1,.7),ncol=1)
        ax.set_title(f"Monthly Budget vs Account")
        st.pyplot(fig)
        plt.close(fig)
#endregion

def valAbvMarker(ax,xVal,yVal):
    n=len(xVal)
    
    for i in range(n):
        # ax.text(xVal[i],yVal[i]+2,f"{yVal[i]:.3g}",ha="center",va="bottom",fontsize=7)  #if 3 significant digits
        ax.text(xVal[i],yVal[i]+yVal[i]*.05,f"{str(yVal[i])[:1]+"."+str(yVal[i])[1:3]}",ha="center",va="bottom",fontsize=7)
