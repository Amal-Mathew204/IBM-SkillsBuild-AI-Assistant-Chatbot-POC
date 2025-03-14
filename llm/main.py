#TODO use pylint doc string this file
import traceback
from fastapi import FastAPI
from controller import LLMController
from pydantic import BaseModel


class Interaction(BaseModel):
    role: str
    content: str

class ConversationState(BaseModel):
    conversation_state: list[Interaction]

app = FastAPI()


@app.post("/chatbot/")
def llm(conversation_state: ConversationState):
    """
    Method
    """
    unformatted_conversations = dict(conversation_state)["conversation_state"]
    conversations = []
    for convo in unformatted_conversations:
        conversations.append(dict(convo))
    

    try:
        model_path: str ="./llama_model"
        controller = LLMController(model_path)
        # Process the conversation
        result = controller.process_conversation(conversations) #pylint: disable=no-member
        # Print only the response and suitability status, not the conversation history
        simplified_output = {
            "response": result["response"],
            "suitable_for_search": result["suitable_for_search"]
        }
        return simplified_output
    except Exception as e: #pylint: disable = broad-exception-caught
        # Log the error for debugging
        error_details = traceback.format_exc()
        print(f"Error loading model: {e}\n{error_details}")
        # Return error response without conversation history
        error_output = {
            "error": f"Model loading failed: {str(e)}"
        }
        return error_output
