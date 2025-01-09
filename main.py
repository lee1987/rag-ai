from fastapi import FastAPI, HTTPException, status

from model.Conversation import Conversation
from model.db import DB
from gpt import Gpt
from model.preprocessing import Preprocessing
from model.prompt import Prompt

app = FastAPI()
db = DB("localhost", "5432", "interview", "postgres", "pass1")
preprocessor = Preprocessing()
gpt = Gpt(db, preprocessor)


@app.post("/users/{user_uuid}/search")
def search_psoriasis_data(user_uuid: str, prompt: Prompt) -> str:
    """
    Use this endpoint to search for psoriasis data.
    You can input your queries in natural language.
    """
    # @todo: CHANGE THIS
    if user_uuid != "615a9e5f-51b1-4c72-9acb-db1a73f824c1":
        raise HTTPException(
            detail='Invalid User',
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    question = prompt.input

    ## Load context:
    # - from previous conversation in database
    # - from article in vector database
    previousConversation = gpt.build_context_from_previous_conversation(user_uuid)
    articles = gpt.build_context_from_article()
    messages = gpt.build_prompt(question, previousConversation, articles)

    response = gpt.retrieve_output(messages)

    return response


@app.post("/users/{user_uuid}/create_multiple_choice_questions")
def create_multiple_choice_questions(user_uuid: str, prompt: Prompt) -> str:
    """
    Use this endpoint to create multiple choice questions based on psoriasis data.
    You can input your queries in natural language.
    """
    if user_uuid:
        print('test')
    raise HTTPException(
        detail='Not Implemented',
        status_code=status.HTTP_501_NOT_IMPLEMENTED
    )


@app.get("/users/{user_uuid}/conversations")
def get_user_conversations(user_uuid: str) -> Conversation:
    """
    This endpoint retrieves all conversations associated with a specific user.
    It returns a list of conversations.
    """
    # @todo: CHANGE THIS
    raise HTTPException(
        detail='Not Implemented',
        status_code=status.HTTP_501_NOT_IMPLEMENTED
    )
