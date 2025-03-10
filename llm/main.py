#TODO use pylint doc string this file
from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel


class Interaction(BaseModel):
    role: str
    content: str

class ConversationState(BaseModel):
    conversation_state: list[Interaction]


@asynccontextmanager
async def lifespan(app: FastAPI):

    yield
    #NOTE the yeild keyword separate the code
    #Code before yield happends before the server starts
    #Code after yeild happens when the server ends

app = FastAPI(lifespan=lifespan)


@app.post("/chatbot/")
def llm(conversation_state: ConversationState):

    raise NotImplementedError()