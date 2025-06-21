import pandas as pd
import streamlit as st
df = pd.DataFrame([
    ['hk', 1], 
    ['cz', 2.744], 
    ['eu', 0.1107], 
    ['pl', 0.4718], 
], columns = ['currency', 'rate']).set_index('currency')

amount = st.number_input('Amount', value = 100, min_value = 0)
currency = st.radio('Currency', df.index, horizontal = True)

df.rate /= df.at[currency, 'rate']
df['amount'] = amount * df.rate
st.write(df.round(2))