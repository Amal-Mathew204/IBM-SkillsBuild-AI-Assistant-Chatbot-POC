#TODO use pylint doc string this file
from contextlib import asynccontextmanager
from fastapi import FastAPI
from controller import LLMController
from pydantic import BaseModel
import os
from unsloth import LlamaForCausalLM

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
    conversations = dict(conversation_state)["conversation_state"]
    # Make sure unsloth is installed in your Docker
    model_path = "./llama3.2"
    
    # Load using Unsloth's loader
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = LlamaForCausalLM.from_pretrained(
        model_path,
        device_map="auto",
        torch_dtype="auto"
    )

    result = controller.process_conversation(conversations)

    # If a response was generated, add it to the conversation history
    if result["response"] is not None:
        conversations.append({
            "role": "assistant",
            "content": result["response"]
        })
    
    # Return the result with the updated conversation and suitability flag
    return {
        "conversation_state": conversations,
        "response": result["response"],
        "suitable_for_search": result["suitable_for_search"]
    }
    return(conversations)
