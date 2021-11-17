import streamlit as st
import requests

BASE_URL = "https://cbdf-69-174-156-186.ngrok.io"


############## utilities
@st.experimental_memo(ttl=600)
def get_quizzes():
    """Get all possible quizzes. Memo assumes that quizzes won't appear
    more frequently than 10 minutes"""
    return requests.get(BASE_URL + "/quizzes").json()


@st.experimental_memo
def get_question(lesson, question_id):
    """Get question from API, return question_info key for convenience
    instead of it nested inside the lesson key
    """
    url = BASE_URL + "/question/" + lesson + "?" + "question_id=" + str(question_id)
    r = requests.get(url).json()
    return r["question_info"]


def display_question(resp):
    """Format the question nicely, given the API response"""
    return f"""Question {resp["question_id"]}: {resp["question_text"]}"""


# def generate_choices(resp):

#     if resp["question_type"] == "multiple_choice":


############## streamlit app
# get all possible quizzes
qlist = get_quizzes()


quiz = st.sidebar.selectbox(
    "Choose Lesson:",
    [x["name"] for x in qlist],
)

## app header
f"""# Quiz: {quiz}
"""

### Is this a loop, where r["question_type"] determines the widget?
q0 = get_question(quiz, 0)
q0_ans = st.radio(
    display_question(q0),
    q0["question_answers"],
    format_func=lambda x: q0["question_answers"][x],
)
"---"

q1 = get_question(quiz, 1)
q1_ans = st.radio(
    display_question(q1),
    q1["question_answers"],
    format_func=lambda x: q1["question_answers"][x],
)
"---"

q2 = get_question(quiz, 2)
q2_ans = st.text_input(display_question(q2))
"---"

q3 = get_question(quiz, 3)
q3_ans = st.text_input(display_question(q3))
"---"

q4 = get_question(quiz, 4)
q4_ans = st.radio(display_question(q4), q4["question_answers"])
"---"
