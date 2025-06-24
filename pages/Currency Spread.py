import streamlit as st

low = st.number_input('Low', value = 100.0, min_value = 0.0)
high = st.number_input('High', value = 100.0, min_value = low)
diff = high - low
spread = diff / high
output = f'''
```python
Diff   = {high} - {low} = {diff}
Spread = {diff} / {high} = {round(spread, 6)}
```
'''
st.write(output)
