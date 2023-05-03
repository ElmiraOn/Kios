import streamlit as st
from PIL import Image
import pandas as pd
import datetime

def local_css(file_name):
    with open(file_name) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)
st.set_page_config(layout="wide")
local_css("style.css")


df = pd.read_csv('out.csv')
col1, col2 = st.columns([1,1.5])

def invalid_purchase():
    #send data to the model and return value
    model_result = True # it is fraud
    current_time = datetime.datetime.now()
    new_row = pd.DataFrame({'date':current_time ,'Merchant': 'ALDO', 'amount': "$200"},index =[0])
    global df
    df = pd.concat([new_row, df]).reset_index(drop = True)
    df.to_csv('out.csv', index=False) 
    return model_result

def valid_purchase():
    #send data to the model and return value

    current_time = datetime.datetime.now()
    new_row = pd.DataFrame({'date':current_time ,'Merchant': "ALDO", 'amount': "$200"},index =[0])
    global df
    df = pd.concat([new_row, df]).reset_index(drop = True)
    df.to_csv('out.csv',index=False) 

fraud_detected = False
btn1 = False
btn2 = False
if st.session_state.get("invalid_purch", True):
    st.session_state.disabled = False
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
        btn2 = st.button("Purchase",key="c", use_container_width=True)
        if btn2:
            fraud_detected = invalid_purchase()

def row_style(row):
    if row.index == 0:
        return pd.Series('background-color: red', row.index)
    # else:
    #     return pd.Series('', row.index)

with col2:
    with st.container():
        st.header("Financial Institution view")
        st.subheader("Account 30407675418785 transaction history")
        c1, c2 = st.columns([1,3])
        with c1:
            st.write("Account #: 30407675418785")
            st.write("Account Holder: John Doe")
        with c2: 
            st.write("Address: 32941 Krystal Mill Apt. 17, Toronto, ON, Canada, M3J 4v1")
            st.write("BD: 1990-5-20")
        #init
        if(btn1 == False and btn2==False):        
            data_in = pd.read_csv('in.csv')
            st.dataframe(data_in, use_container_width=True)
        
        else:
            data =  pd.read_csv('out.csv')
            btn4 = False
            if(fraud_detected==False or btn4 == True) :
                st.dataframe(data, use_container_width=True)
            else:
                st.write("Fraud Activity detected in this account!")
                st.write("The suspected transaction is paused. Please contact the account holder to the investigate the marked transaction")
                btn3 = st.button("Contact",key="contact", use_container_width=True)
                btn4 = st.button("Resolve",key="resolved", use_container_width=True)
            # st.dataframe(df, use_container_width=True)
                
                c1 = 'background-color: red'
                d = {0: c1}
                st.dataframe(data.style.apply(lambda x: x.index.map(d)),use_container_width=True) 

    