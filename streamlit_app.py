import streamlit as st
from classes import annotate

one_text = annotate.OneText()
one_text.config.newline = '  \n'
one_text.config.text = st.text_area("Enter Chinese Text Here")
one_text.config.language = st.selectbox('Choose a language', ['cantonese', 'mandarin'])
st.markdown('Chinese Text With Romanisation')
st.markdown(one_text.main())