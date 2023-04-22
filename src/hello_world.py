# hello_world.py

import streamlit as st
import numpy as np
import pandas as pd
import time


@st.cache_data
def get_numbers(step):
    np.random.seed(int(time.time()))
    return np.random.randint(0, 10, 20, dtype=int).reshape((-1, 2))

#if "data" not in st.session_state:
#    cols = ["a", "b", "reponse", "solution"]
#    st.session_state.data = pd.DataFrame(columns=cols)
if "idx" not in st.session_state:
    st.session_state.idx = 0

numbers = get_numbers(0)
a, b = numbers[st.session_state.idx]
st.write(f"idx={st.session_state.idx}, a={a}, b={b}")

st.write(f"{a} x {b} = ")
reponse = st.text_input("Reponse")

run = st.button('Submit')

if run:
    st.write(f"idx={st.session_state.idx}, a={a}, b={b}, reponse={reponse}")
    #st.session_state.data.loc[st.session_state.idx] = [a, b, reponse, a*b]
    st.session_state.idx += 1
    a, b = numbers[st.session_state.idx]
    st.write(f"idx={st.session_state.idx}, a={a}, b={b}")

#st.dataframe(st.session_state.data)