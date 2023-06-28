import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
df=pd.read_csv('startup_cleaned.csv')
df['date']=pd.to_datetime(df['date'],errors='coerce')
def  load_invester_detail(investor):
    st.title(investor)
    #main thing is to get the last 5 invesetments in form of data frame(which gives using name of investor),use fun to display
    last_5_inv=df[df['investors'].str.contains(investor)].head()[['date','startup','vertical','city','amount']]
    st.subheader('most recent investment')
    st.dataframe(last_5_inv)
    big_inv=df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(
        ascending=False)
    st.subheader('big investments')
    st.dataframe(big_inv)
    #plot sector wise analysis
    vert_serises=df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
    try:

        st.subheader("Sector Invested")
        fig1,ax1=plt.subplots()
        ax1.pie(vert_serises,labels=vert_serises.index,autopct="%0.01f%%")
        st.pyplot(fig1)

        df["year"] = df['date'].dt.year
        yoy=df[df['investors'].str.contains("IDG Ventures")].groupby("year")['amount'].sum()
        st.subheader("YOY Investment")
        fig3, ax3 = plt.subplots()
        ax3.plot(yoy.index,yoy.values)
        st.pyplot(fig3)
    except ValueError:
        print("Not invested till now")
    #city
    # city = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum()
    # st.subheader("City Invested")
    # fig2, ax2 = plt.subplots()
    # ax2.pie(vert_serises, labels=city.index, autopct="%0.01f%%")
    # st.pyplot(fig2)
# st.dataframe(df)
st.sidebar.title("startup funding analysis")

option=st.sidebar.selectbox('select one',["overall analysis","start up","invester"])
if option=="overall analysis":
    st.title("overall analysis")
elif option=="start up":
    st.sidebar.selectbox("select startup",sorted(df["startup"].unique().tolist()))
    st.title("startup analysis")
    btn1=st.sidebar.button("find startup details")
else:
    selected_ivester=st.sidebar.selectbox("select investor",sorted(set(df['investors'].str.split(',').sum())))
    st.title("Investor Analysis")
    btn2 = st.sidebar.button("find investor details")
    if btn2:
        load_invester_detail(selected_ivester)

