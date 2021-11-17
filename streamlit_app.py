import streamlit as st
import requests

BASE_URL = "https://d4f1-69-174-156-186.ngrok.io/question/"


############## utilities
@st.experimental_memo
def get_question(lesson, question_id):
    url = BASE_URL + lesson + "?" + "question_id=" + str(question_id)
    r = requests.get(url).json()
    return r["question_info"]


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
q1 = get_question(lesson, 1)
"Question ", str(q1["question_id"]), ": ", q1["question_text"]  # make an f-string?

q1_ans = st.radio(
    "",
    q1["question_answers"],
    format_func=lambda x: q1["question_answers"][x],
)

# q1
# q1_ans
