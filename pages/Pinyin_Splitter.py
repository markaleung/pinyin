import os
os.chdir(os.path.dirname(__file__)+'/..')
from classes import pivot
import streamlit as st

pivot = pivot.Pivot()
pivot.column = st.selectbox('Character Part', ['Initial', 'Rhyme'])
pivot.pinyin = st.selectbox('Language', ['Cantonese', 'Mandarin'])
unique_values = sorted(pivot.df_raw[f'{pivot.column}_{pivot.pinyin}'].unique())
pivot.value = st.selectbox('Value', unique_values)
pivot.main()
st.dataframe(pivot.df)