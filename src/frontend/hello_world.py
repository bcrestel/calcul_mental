# hello_world.py

import time

import numpy as np
import pandas as pd
import streamlit as st


@st.cache_data
def get_numbers(step):
    np.random.seed(int(time.time()))
    return np.random.randint(0, 10, 2 * step, dtype=int).reshape((-1, 2))


st.sidebar.selectbox("Name", ["An", "Op", "Ar"])
st.sidebar.selectbox("Operation", ["+", "-", "x", "/"])
st.sidebar.slider("Max value", 0, 10)
nb_questions = st.sidebar.number_input("Nombre de questions", value=60)
start_button = st.empty()
# btn = start_button.sidebar.button("Démarrer", disabled=False, key="button_start_1")
btn = start_button.button("Démarrer", disabled=False, key="button_start_1")

# start_button.empty()
numbers = get_numbers(nb_questions)
responses = []
for ii in range(nb_questions):
    a, b = numbers[ii]
    c1, c2, _ = st.columns([1, 2, 7])
    with c1:
        st.write("##")
        st.write(f"{a} x {b} = ", key=f"write_{ii}")
    with c2:
        responses.append(st.text_input("Reponse", key=f"reponse_{ii}"))

run = st.button("J'ai fini!")

if run:
    df = pd.DataFrame(
        {
            "question": range(3),
            "a": numbers[:3, 0],
            "b": numbers[:3, 1],
            "reponse": responses,
            "solution": numbers.prod(axis=1)[:3],
        }
    )
    st.dataframe(df)
    st.write(responses)
    st.balloons()
    st.snow()
