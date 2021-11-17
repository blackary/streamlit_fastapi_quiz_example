from fastapi import FastAPI
import json

app = FastAPI()


def get_quiz_contents() -> dict:
    with open("quiz.json") as f:
        return json.load(f)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/question/{quiz}/{id}")
async def get_question(quiz: str, id: int):
    contents = get_quiz_contents()
    question = contents["questions"][id]
    question_info = {
        "question_text": question["question"],
        "question_answers": question.get("answers", []),
        "question_type": question["type"],
    }
    return {"quiz_name": contents["name"], "question_info": question_info}
