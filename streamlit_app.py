import streamlit as st, re
from classes import annotate

one_text = annotate.OneText()
one_text.config.newline = '  \n' # Markdown newline needs 2 spaces
one_text.config.text = st.text_area("Enter Chinese Text Here")
# one_text.config.split_text_on_punctuation = st.checkbox('Split Text on Chinese Punctuation', value = True)

one_text.config.language = st.selectbox('Choose a Language', annotate.CLASSES.keys())
# if one_text.config.language == 'cantonese':
#     one_text.config.cantonese_multiple_pronunciation = st.checkbox('Show Multiple Pronunciations for Cantonese', value = True)

st.markdown('Chinese Text With Romanisation')
st.markdown(re.sub(r'([$#_*\\<>])', r'\\\1', one_text.main()))
