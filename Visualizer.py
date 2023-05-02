import streamlit as st
from PIL import Image
import pandas as pd
import datetime

def local_css(file_name):
    with open(file_name) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)
st.set_page_config(layout="wide")
local_css("style.css")


df = pd.read_csv('Book1.csv')
col1, col2 = st.columns(2)

def invalid_purchase():
    #send data to the model and return value
    model_result = True # it is fraud
    current_time = datetime.datetime.now()
    new_row = pd.DataFrame({'date':current_time ,'vendor': 'ALDO', 'amout': "$200"},index =[0])
    global df
    df = pd.concat([new_row, df]).reset_index(drop = True)

    return model_result

def valid_purchase():
    #send data to the model and return value

    current_time = datetime.datetime.now()
    new_row = pd.DataFrame({'date':current_time ,'vendor': "ALDO", 'amout': "$200"},index =[0])
    global df
    df = pd.concat([new_row, df]).reset_index(drop = True)

fraud_detected = False

with col1:
    with st.container():
        st.header("valid tranaction")
        image = Image.open('shoes.jpg')
        st.image(image )
        btn1 = st.button("Purchase", key="valid_purch", use_container_width=True)
        if btn1:
            valid_purchase()
    with st.container():
        st.header("Fraud transaction") 
        image = Image.open('shoes.jpg')
        st.image(image )
        btn2 = st.button("Purchase",key="invalid_purch", use_container_width=True)
        if btn2:
            fraud_detected = invalid_purchase()

def row_style(row):
    if row.index == 0:
        return pd.Series('background-color: red', row.index)
    # else:
    #     return pd.Series('', row.index)

with col2: 
    with st.container():
        st.header("FI view")
        st.subheader("John Doe's transaction history")
        if(fraud_detected):
            st.write("Fraud detected!")
        # st.dataframe(df, use_container_width=True)
            c1 = 'background-color: red'
            d = {0: c1}
            st.dataframe(df.style.apply(lambda x: x.index.map(d)),use_container_width=True)
        else:
            st.dataframe(df, use_container_width=True)