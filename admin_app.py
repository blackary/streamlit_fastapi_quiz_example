import streamlit as st
from string import ascii_letters, ascii_lowercase
from typing import Literal, Optional, Union
from dataclasses import dataclass, field


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
    questions: list[Question]

    def to_json(self) -> dict:
        base_dict = self.__dict__.copy()
        base_dict["questions"] = [q.__dict__ for q in base_dict["questions"]]
        return base_dict


"# Create new quiz!"

quiz_key = st.text_input("Quiz key")
quiz_name = st.text_input("Quiz pretty name")

if not quiz_key or not quiz_name:
    st.stop()

if "quizzes" not in st.session_state:
    st.session_state["quizzes"] = {}

if quiz_key not in st.session_state["quizzes"]:
    st.session_state["quizzes"][quiz_key] = Quiz(quiz_key, quiz_name, [])

"---"

question_text = st.text_area("Question", height=1)

question_type = st.selectbox(
    "Question type", ["text", "true_false", "multiple_select", "multiple_choice"]
)
if question_type in ["multiple_choice", "multiple_select"]:
    if "num_options" not in st.session_state:
        st.session_state["num_options"] = 2
    if st.button("Add option"):
        st.session_state["num_options"] += 1
    if st.session_state["num_options"] >= 2 and st.button("Remove option"):
        st.session_state["num_options"] -= 1
    options = []
    for item in range(st.session_state["num_options"]):
        options.append(st.text_input(f"Option {ascii_lowercase[item]}"))

    option_keys = list(ascii_letters[: st.session_state["num_options"]])

    if question_type == "multiple_choice":
        answer = st.selectbox("Answer", option_keys)
    else:
        answer = st.multiselect("Answer", option_keys)

elif question_type == "true_false":
    answer = st.selectbox("Answer", ["True", "False"])
    options = option_keys = ["True", "False"]
else:
    answer = st.text_input("Answer")
    options = option_keys = []

alternative_answers = []
if "num_alternatives" not in st.session_state:
    st.session_state["num_alternatives"] = 0
if st.button("Add alternative answer"):
    st.session_state["num_alternatives"] += 1
if st.session_state["num_alternatives"] >= 1 and st.button("Remove alternative answer"):
    st.session_state["num_alternatives"] -= 1
for item in range(st.session_state["num_alternatives"]):
    alternative_answers.append(st.text_input(f"Alternative answer {item}"))

if question_text and answer and st.button("Save question"):
    quiz: Quiz = st.session_state["quizzes"][quiz_key]
    answers = {key: val for key, val in zip(option_keys, options)}
    quiz.questions.append(
        Question(
            question=question_text,
            type=question_type,
            answers=answers,
            answer=answer,
            alternative_answers=alternative_answers,
        )
    )


# st.write(st.session_state)

# current_quiz.__dict__

current_quiz = st.session_state["quizzes"][quiz_key]
st.write(f"Paste the following into `quizzes/{quiz_key}.json`")
st.write(current_quiz.to_json())
