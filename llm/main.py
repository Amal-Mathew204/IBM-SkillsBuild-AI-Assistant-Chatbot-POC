#TODO use pylint doc string this file
from contextlib import asynccontextmanager
from fastapi import FastAPI
from controller import LLMController
from pydantic import BaseModel
import os
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import torch

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

    # Path to the base model on Hugging Face
    base_model_id = "meta-llama/Llama-3.2-3B-Instruct" # Adjust to match the base model you used

    # Your Hugging Face token
    hf_token = "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"

    # Path to your adapter/fine-tuned model
    adapter_path = "/content/drive/MyDrive/trained_models/normal/llama3.2"

    try:
        # Load base model and tokenizer with token
        tokenizer = AutoTokenizer.from_pretrained(
            base_model_id,
            token=hf_token
        )
        base_model = AutoModelForCausalLM.from_pretrained(
            base_model_id,
            token=hf_token,
            torch_dtype=torch.bfloat16 if torch.cuda.is_available() and torch.cuda.get_device_capability()[0] >= 8 else torch.float16,
            device_map="cpu"
        )
        
        # Load the adapter on top of the base model
        model = PeftModel.from_pretrained(base_model, adapter_path)
        
        # Create a modified controller that accepts pre-loaded models
        class AdapterLLMController(LLMController):
            def __init__(self, model, tokenizer):
                # Override the __init__ to accept pre-loaded model and tokenizer
                self.model = model
                self.tokenizer = tokenizer
        
        # Initialize controller with pre-loaded model and tokenizer
        controller = AdapterLLMController(model, tokenizer)
        
        # Process the conversation
        result = controller.process_conversation(conversations)
        
        # Print only the response and suitability status, not the conversation history
        simplified_output = {
            "response": result["response"],
            "suitable_for_search": result["suitable_for_search"]
        }
        return simplified_output
        
    except Exception as e:
        # Log the error for debugging
        import traceback
        error_details = traceback.format_exc()
        print(f"Error loading model: {e}\n{error_details}")
        
        # Return error response without conversation history
        error_output = {
            "error": f"Model loading failed: {str(e)}"
        }
        return error_output

        