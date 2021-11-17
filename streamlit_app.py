import streamlit as st
import requests

BASE_URL = "https://d4f1-69-174-156-186.ngrok.io/question/"


############## utilities
@st.experimental_memo
def get_question(lesson, question_id):
    """Get question from API, return question_info key for convenience
    instead of it nested inside the lesson key
    """
    url = BASE_URL + lesson + "?" + "question_id=" + str(question_id)
    r = requests.get(url).json()
    return r["question_info"]


def display_question(resp):
    """Format the question nicely, given the API response"""
    # return "Question " + str(resp["question_id"]) + ": " + resp["question_text"]
    return f"""Question {resp["question_id"]}: {resp["question_text"]}"""


############## streamlit app

## TODO: have multiple lessons/tests available, one per endpoint
lesson = st.sidebar.selectbox(
    "Choose Lesson:",
    ["science_bowl"],
    # format_func=lambda x: x
)

## app header
f"""
# {lesson}
---
"""

### Is this a loop, where r["question_type"] determines the widget?
q0 = get_question(lesson, 0)
q0_ans = st.radio(
    display_question(q0),
    q0["question_answers"],
    format_func=lambda x: q0["question_answers"][x],
)

q1 = get_question(lesson, 1)
q1_ans = st.radio(
    display_question(q1),
    q1["question_answers"],
    format_func=lambda x: q1["question_answers"][x],
)

q2 = get_question(lesson, 2)
q2_ans = st.text_input(display_question(q2))

q3 = get_question(lesson, 3)
q3_ans = st.text_input(display_question(q3))
