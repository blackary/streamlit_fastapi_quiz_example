import json
from dataclasses import dataclass, field
from pathlib import Path
from string import ascii_lowercase
from typing import Literal, Union
from pandas.core.indexes.base import Index

import requests
import streamlit as st
from streamlit.type_util import Key

BASE_URL = "http://127.0.0.1:8000"


def get_quizzes() -> list[dict]:
    return requests.get(BASE_URL + "/quizzes").json()


def get_question(quiz: str, question_id: int):
    url = f"{BASE_URL}/question_admin/{quiz}?question={question_id}"
    r = requests.get(url).json()
    return r["question_info"]


@dataclass()
class Question:
    question: str
    type: Literal["multiple_choice", "multiple_select", "true_false", "text"]
    answer: Union[str, list[str]]
    answers: dict[str, str] = field(default_factory=dict)
    alternative_answers: list[str] = field(default_factory=list)


@dataclass()
class Quiz:
    name: str
    pretty_name: str
    questions: list[Question] = field(default_factory=list)
    num_questions: int = 0

    def to_json(self) -> str:
        base_dict = self.__dict__.copy()
        base_dict["questions"] = [q.__dict__ for q in base_dict["questions"]]
        del base_dict["num_questions"]
        return json.dumps(base_dict, indent=4)


"# Edit/Create new quiz!"

raw_quizzes = get_quizzes()

quizzes = {
    quiz["name"]: Quiz(
        quiz["name"], quiz["pretty_name"], num_questions=quiz["questions"]
    )
    for quiz in raw_quizzes
}

quiz_options = list(quizzes.keys()) + ["-- Create New --"]

quiz_name = st.selectbox("Select quiz", options=quiz_options)

if quiz_name == "-- Create New --":
    current_quiz = Quiz("", "")
else:
    current_quiz = quizzes[quiz_name]


quiz_key = st.text_input("Quiz key", value=current_quiz.name)
quiz_name = st.text_input("Quiz pretty name", value=current_quiz.pretty_name)

if not quiz_key or not quiz_name:
    st.stop()

if "populated_quizzes" not in st.session_state:
    st.session_state["populated_quizzes"] = []


def populate_questions(quiz: Quiz):
    if quiz.name in st.session_state["populated_quizzes"]:
        return

    print("RUNNING POPULATE")
    questions = []
    for i in range(quiz.num_questions):
        current_question_details = get_question(quiz_key, i)

        q = Question(
            question=current_question_details["question_text"],
            type=current_question_details["question_type"],
            answer=current_question_details["question_answer"],
            answers=current_question_details["question_answers"],
        )
        questions.append(q)
        quiz.questions = questions

    st.session_state["populated_quizzes"].append(quiz.name)


populate_questions(current_quiz)

st.write(st.session_state)

"---"

"## Select an existing question to edit, or go to the end of the list to add a new question"

# if "num_questions" not in st.session_state:
#    st.session_state["question_options"] = []

# st.session_state["question_options"] = list(range(0, current_quiz.num_questions + 1))

# current_question = st.selectbox(
#    "Select question", options=st.session_state["question_options"]
# )

current_question = int(st.text_input("Select question by id (0-indexed)", value=0))

try:
    current_q = current_quiz.questions[current_question]
except IndexError:
    current_q = Question("", "text", "")

st.write(current_q)

if "num_options" not in st.session_state:
    st.session_state["num_options"] = 0
if "num_alternatives" not in st.session_state:
    st.session_state["num_alternatives"] = 0

question_text = st.text_area(
    "Question",
    height=1,
    value=current_q.question,
)

TYPES = ["text", "true_false", "multiple_select", "multiple_choice"]

question_type = st.selectbox(
    "Question type",
    TYPES,
    index=TYPES.index(
        current_q.type,
    ),
)
if question_type in ["multiple_choice", "multiple_select"]:
    st.session_state["num_options"] = len(current_q.answers)
    if st.button("Add option"):
        st.session_state["num_options"] += 1
    if st.session_state["num_options"] >= 2 and st.button("Remove option"):
        st.session_state["num_options"] -= 1
    options = []
    for item in range(st.session_state["num_options"]):
        letter = ascii_lowercase[item]
        try:
            existing_val = current_q.answers[letter]
        except KeyError:
            existing_val = ""
        options.append(st.text_input(f"Option {letter}", value=existing_val))

    option_keys = list(ascii_lowercase[: st.session_state["num_options"]])

    if question_type == "multiple_choice":
        answer = st.selectbox("Answer", option_keys)
    else:
        answer = st.multiselect("Answer", option_keys)

elif question_type == "true_false":
    options = ["True", "False"]
    try:
        idx = options.index(current_q.answer)
    except ValueError:
        idx = 0
    answer = st.selectbox("Answer", ["True", "False"], index=idx)
    options = option_keys = ["True", "False"]
else:
    answer = st.text_input("Answer", value=current_q.answer)
    options = option_keys = []

alternative_answers = []
st.session_state["num_alternatives"] = len(current_q.alternative_answers)
if st.button("Add alternative answer"):
    st.session_state["num_alternatives"] += 1
if st.session_state["num_alternatives"] >= 1 and st.button("Remove alternative answer"):
    st.session_state["num_alternatives"] -= 1
for item in range(st.session_state["num_alternatives"]):
    try:
        existing_val = current_q.alternative_answers[item]
    except IndexError:
        existing_val = ""
    alternative_answers.append(
        st.text_input(f"Alternative answer {item}", value=existing_val)
    )

if question_text and answer and st.button("Save question"):
    answers = {key: val for key, val in zip(option_keys, options)}
    current_quiz.questions.append(
        Question(
            question=question_text,
            type=question_type,
            answers=answers,
            answer=answer,
            alternative_answers=alternative_answers,
        )
    )
    current_quiz.num_questions += 1
    st.session_state["question_options"] = list(
        range(0, current_quiz.num_questions + 1)
    )

st.write(st.session_state)

save_path = (Path("quizzes") / quiz_key).with_suffix(".json")

st.text(current_quiz.to_json())

if st.button(f"Save quiz to {save_path}?"):
    save_path.write_text(current_quiz.to_json())
    "## Saved!"
    st.balloons()
    # st.write(current_quiz.to_json())
