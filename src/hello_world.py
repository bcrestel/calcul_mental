# hello_world.py

import streamlit as st
import numpy as np
import pandas as pd
import time


@st.cache_data
def get_numbers(step):
    np.random.seed(int(time.time()))
    return np.random.randint(0, 10, 20, dtype=int).reshape((-1, 2))

numbers = get_numbers(0)
responses = []
for ii in range(3):
    a, b = numbers[ii]
    c1, c2, _ = st.columns([1, 2, 7])
    with c1:
        st.write("##")
        st.write(f"{a} x {b} = ", key=f"write_{ii}")
    with c2:
        responses.append(st.text_input("Reponse", key=f"reponse_{ii}"))

run = st.button('Submit')

if run:
    df = pd.DataFrame({
        "question": range(3),
        "a": numbers[:3,0],
        "b": numbers[:3,1],
        "reponse": responses,
        "solution": numbers.prod(axis=1)[:3],
    })
    st.dataframe(df)
    st.write(responses)