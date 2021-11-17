from fastapi import FastAPI, HTTPException
from random import randint
import json

app = FastAPI()


def get_quiz_contents(quiz_name: str) -> dict:
    with open("quizzes.json") as f:
        quizzes = json.load(f)
        for quiz in quizzes:
            if quiz["name"] == quiz_name:
                return quiz
        raise KeyError(f"Quiz {quiz_name} not found")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/question/{quiz}")
async def get_question(quiz: str, question_id: int = None):
    try:
        contents = get_quiz_contents(quiz)
    except KeyError:
        raise HTTPException(status_code=400, detail=f"Invalid quiz: {quiz}")
    if question_id is None:
        question_id = randint(0, len(contents["questions"]) - 1)
    try:
        question = contents["questions"][question_id]
    except IndexError:
        raise HTTPException(
            status_code=400, detail=f"Invalid question id: {question_id}"
        )
    question_info = {
        "question_text": question["question"],
        "question_id": question_id,
        "question_answers": question.get("answers", []),
        "question_type": question["type"],
    }
    return {"quiz_name": contents["name"], "question_info": question_info}
