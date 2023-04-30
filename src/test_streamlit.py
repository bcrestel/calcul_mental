import streamlit as st
import random

if "show_inputs" not in st.session_state:
    st.session_state.show_inputs = False

if "random_numbers" not in st.session_state:
    st.session_state.random_numbers = [random.randint(1, 100) for _ in range(3)]

def show_text_inputs():
    text_input = []
    for idx, rnd in enumerate(st.session_state.random_numbers):
        text_input.append(st.text_input(f"Text Input {rnd}", key=f"text_{idx}"))
    submit_button = st.button("Submit")
    if submit_button:
        for txt, rnd in zip(text_input, st.session_state.random_numbers):
            st.write(f"Text Input {rnd}: {txt}")
        st.session_state.show_inputs = False

if st.sidebar.button("Show Text Inputs"):
    st.session_state.show_inputs = True
    st.session_state.random_numbers = [random.randint(1, 100) for _ in range(3)]

if st.session_state.show_inputs:
    show_text_inputs()
