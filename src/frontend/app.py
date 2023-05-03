import streamlit as st
import logging
import time

from src.users.users import Users
from src.utils.constants import map_sym_text_op
from src.backend.get_summary_files import get_summary_files
from src.backend.result_file import ResultFile
from src.frontend.quiz_generator import quiz_generator

logging.basicConfig(level=logging.ERROR, format='%(asctime)s %(levelname)s %(filename)s--l.%(lineno)d: %(message)s')
logger = logging.getLogger(__name__)

# Define the sidebar
all_users = Users()
user_name = st.sidebar.selectbox("Prénom", all_users.users)
operation_symbol = st.sidebar.selectbox("Operation", map_sym_text_op.keys())
operation_type = map_sym_text_op[operation_symbol]
min_b, max_b = st.sidebar.slider("Quelles tables travailler?", 0, 12, (1, 10))
nb_questions = st.sidebar.number_input("Nombre de questions", value=60)

if "show_quizz" not in st.session_state:
    st.session_state.show_quizz = False
    st.session_state.summaryfile = None
    st.session_state.summaryfile_session = None
    st.session_state.result_file = None
    st.session_state.t0 = None
    st.session_state.t1 = None
    st.session_state.celebration = False

def show_quizz():
    questions = quiz_generator(st.session_state.summaryfile_session)
    logger.debug(questions)
    answers = []
    if st.session_state.t0 is None:
        st.session_state.t0 = time.time()
    for idx, quest in enumerate(questions):
        c1, c2, _ = st.columns([1, 2, 7])
        with c1:
            st.write("##")
            st.write(quest, key=f"write_{idx}")
        with c2:
            answers.append(st.text_input("Réponse", key=f"reponse_{idx}"))

    if st.button("J'ai fini!"):
        if st.session_state.t1 is None:
            st.session_state.t1 = time.time()
            st.session_state.time_spent = st.session_state.t1 - st.session_state.t0
        assert len(answers) == len(st.session_state.summaryfile_session)
        st.session_state.summaryfile_session["answers"] = [int(aa) for aa in answers]
        result_file = ResultFile(
            user_name=user_name,
            result_table=st.session_state.summaryfile_session,
            total_time_spent=st.session_state.time_spent,
        )
        st.session_state.result_file = result_file
        if result_file.nb_failure == 0:
            st.session_state.celebration = True
        # Log results
        st.session_state.summaryfile.update_from_answers(result_table=st.session_state.result_file.result_table)
        st.session_state.result_file.update_logfile()

        st.session_state.show_quizz = False
        st.experimental_rerun()

if st.sidebar.button("Démarrer"):
    # reset a few keys in session_state
    st.session_state.result_file = None
    st.session_state.t0 = None
    st.session_state.t1 = None
    summaryfile, summaryfile_session = get_summary_files(
        user_name=user_name,
        operation_type=operation_type,
        min_b=int(min_b),
        max_b=int(max_b),
        nb_questions=int(nb_questions),
    )
    st.session_state.summaryfile = summaryfile
    st.session_state.summaryfile_session = summaryfile_session
    st.session_state.show_quizz = True

if st.session_state.show_quizz:
    show_quizz()
    #st.dataframe(st.session_state.summaryfile_session)

if st.session_state.result_file is not None:
    if st.session_state.celebration:
        st.balloons()
        st.session_state.celebration = False
    text = st.session_state.result_file.analyze_results()
    for tt in text.split("\n"):
        st.sidebar.write(tt)

