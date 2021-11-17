import json
from random import randint
from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class QuestionDetails(BaseModel):
    question_text: str
    question_id: int
    question_answers: dict[str, str]
    question_type: str


class Question(BaseModel):
    quiz_name: str
    question_info: QuestionDetails


class Quiz(BaseModel):
    name: str
    questions: int
    question_types: list[str]


Correctness = Literal["Correct", "Incorrect"]


def get_all_quiz_contents() -> list[dict]:
    with open("quizzes.json") as f:
        return json.load(f)


def get_quiz_contents(quiz_name: str) -> dict:
    quizzes = get_all_quiz_contents()
    for quiz in quizzes:
        if quiz["name"] == quiz_name:
            return quiz
    raise KeyError(f"Quiz {quiz_name} not found")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/quizzes")
def get_quizzes() -> list[Quiz]:
    quizzes = get_all_quiz_contents()

    details: list[Quiz] = []

    for quiz_details in quizzes:
        questions = quiz_details["questions"]
        question_types = list(set(question["type"] for question in questions))
        details.append(
            Quiz(
                **{
                    "name": quiz_details["name"],
                    "questions": len(questions),
                    "question_types": question_types,
                }
            )
        )

    return details


def get_quiz(quiz_name: str) -> dict:
    try:
        contents = get_quiz_contents(quiz_name)
    except KeyError:
        raise HTTPException(status_code=400, detail=f"Invalid quiz: {quiz_name}")
    return contents


def get_question_details(quiz: dict, question_id: int) -> dict:
    try:
        question = quiz["questions"][question_id]
    except IndexError:
        raise HTTPException(
            status_code=400, detail=f"Invalid question id: {question_id}"
        )
    return question


@app.get("/question/{quiz}", response_model=Question)
async def get_question(quiz: str, question_id: int = None) -> Question:
    contents = get_quiz(quiz)
    if question_id is None:
        question_id = randint(0, len(contents["questions"]) - 1)
    question = get_question_details(contents, question_id)
    if "answers" in question:
        question_answers = question["answers"]
    elif question["type"] == "true_false":
        question_answers = {
            "True": "True",
            "False": "False",
        }
    else:
        question_answers = {}
    question_info = {
        "question_text": question["question"],
        "question_id": question_id,
        "question_answers": question_answers,
        "question_type": question["type"],
    }
    return {"quiz_name": contents["name"], "question_info": question_info}


@app.put("/answer/{quiz}/{question_id}/")
async def post_answer(quiz: str, question_id: int, answer: str) -> Correctness:
    contents = get_quiz(quiz)
    question = get_question_details(contents, question_id)

    answer = answer.lower().strip()

    print(question)
    print(answer)

    if question["answer"].lower() == answer:
        return "Correct"

    elif answer in question.get("alternative_answers", []):
        return "Correct"

    return "Incorrect"
