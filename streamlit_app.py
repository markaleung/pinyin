import streamlit as st, re
from classes import annotate

one_text = annotate.OneText()
one_text.config.newline = '  \n' # Markdown newline needs 2 spaces
one_text.config.text = st.text_area("Enter Chinese Text Here")
one_text.config.language = st.selectbox('Choose a Language', ['cantonese', 'mandarin'])
st.markdown('Chinese Text With Romanisation')
st.markdown(re.sub(r'([#_*\\<>])', r'\\\1', one_text.main()))
