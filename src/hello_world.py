# hello_world.py.py
# Benjamin Crestel, 2020-07-01

import streamlit as st

x = st.slider("Select a value")
st.write(x, "squared is", x * x)
st.write(x, "cubed is", x * x * x)