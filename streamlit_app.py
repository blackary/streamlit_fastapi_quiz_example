import streamlit as st
import requests

BASE_URL = "https://cbdf-69-174-156-186.ngrok.io"


############## utilities
# TODO: does this get factored into a full-blown library? Then, specifying
# test app is just a handful of functions that automatically generate necessary parts
@st.experimental_memo(ttl=600)
def get_quizzes():
    """Get all possible quizzes. Memo assumes that quizzes won't appear
    more frequently than 10 minutes"""
    return requests.get(BASE_URL + "/quizzes").json()


@st.experimental_memo
def get_question(lesson, question_id):
    """Get question from API, return question_info key for convenience
    instead of it nested inside the lesson key. No ttl set, with expectation
    that answers won't change
    """
    url = BASE_URL + "/question/" + lesson + "?" + "question_id=" + str(question_id)
    r = requests.get(url).json()
    return r["question_info"]


def display_question(resp):
    """Format the question nicely, given the API response"""
    return f"""Question {resp["question_id"]}: {resp["question_text"]}"""


def generate_choices(resp):
    """Return the proper Streamlit input widget based on the question type"""

    if resp["question_type"] == "multiple_select":
        return st.multiselect(
            display_question(resp),
            resp["question_answers"],
            format_func=lambda x: resp["question_answers"][x],
        )  # would this be better as a series of checkboxes?
    elif resp["question_type"] == "text":
        return st.text_input(display_question(resp))
    elif resp["question_type"] == "multiple_choice":
        return st.radio(
            display_question(resp),
            resp["question_answers"],
            format_func=lambda x: resp["question_answers"][x],
        )
    elif resp["question_type"] == "true_false":
        return st.radio(display_question(resp), resp["question_answers"])


############## streamlit app

qlist = get_quizzes()

## populate selectbox with all possible quizzes as they arrive
quiz_name = st.sidebar.selectbox("Choose Lesson:", [x["name"] for x in qlist])

quiz_details = [x for x in qlist if x["name"] == quiz_name][0]

## app header
f"""# Quiz: {quiz_name}
"""

answers = {}

with st.form("quiz"):
    for idx in range(quiz_details["questions"]):
        q = get_question(quiz_name, idx)
        ans = generate_choices(q)
        "---"
        answers[idx] = ans
    submitted = st.form_submit_button("Submit")

answers
