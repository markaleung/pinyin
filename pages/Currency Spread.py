import streamlit as st

low = st.number_input('Low', value = 100.0, min_value = 0.0)
high = st.number_input('High', value = 100.0, min_value = low)
diff = high - low
diff2 = round(diff, 4)
spread = diff / high
spread2 = round(spread * 100, 4)
output = f'''
```python
Diff   = {high} - {low} = {diff2}
Spread = {diff2} / {high} = {spread2}%
```
'''
st.write(output)
