import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

class LLMController:
    """
    Controller class for LLM interactions, focusing on response generation
    and conversation quality assessment for semantic search.
    """
    
    def __init__(self, model_path):
        """
        Initialize the LLM controller with a model.
        
        Args:
            model_path (str): Path to the pre-trained or fine-tuned model
        """
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.bfloat16 if torch.cuda.is_available() and torch.cuda.get_device_capability()[0] >= 8 else torch.float16,
            device_map="auto"
        )
    
    def process_conversation(self, conversation_history):
        """
        Process the conversation history, assess if it's suitable for semantic search,
        and only generate a response if it's NOT suitable.
        
        Args:
            conversation_history (list): List of message objects with role and content
            
        Returns:
            dict: Contains the assistant's response (or None if suitable) and whether
                 the conversation is suitable for semantic search
        """
        # Make a copy to avoid modifying the original
        conversation = conversation_history.copy()
        
        # First assess if the conversation is suitable for semantic search
        is_suitable = self._assess_quality(conversation)
        
        # Only generate a response if the conversation is NOT suitable for search
        response = None
        if not is_suitable:
            response = self._generate_response(conversation)
        
        return {
            "response": response,
            "suitable_for_search": is_suitable
        }
    
    def _generate_response(self, conversation):
        """
        Generate a response to the latest user input in the conversation.
        
        Args:
            conversation (list): List of message objects with role and content
            
        Returns:
            str: The assistant's response
        """
        # Format the conversation for the model
        formatted_prompt = self.tokenizer.apply_chat_template(conversation, tokenize=False, add_generation_prompt=True)
        
        # Generate the response
        inputs = self.tokenizer(formatted_prompt, return_tensors="pt").to(self.model.device)
        with torch.no_grad():
            outputs = self.model.generate(
                inputs["input_ids"],
                max_new_tokens=256,
                do_sample=True,
                temperature=0.7,
                top_p=0.9
            )
        
        # Extract assistant's response
        output = self.tokenizer.decode(outputs[0], skip_special_tokens=False)
        assistant_reply = output.split("<|start_header_id|>assistant<|end_header_id|>")[-1].split("<|eot_id|>")[0].strip()
        
        return assistant_reply
    
    def _assess_quality(self, conversation):
        """
        Assess if the conversation is suitable for semantic search.
        
        Args:
            conversation (list): List of message objects with role and content
            
        Returns:
            bool: Whether the conversation is suitable for semantic search
        """
        # Extract user content from the conversation
        user_content = ' '.join([turn["content"].lower() for turn in conversation if turn["role"] == "user"])
        
        # Check for required content areas based on your content_aware_parser logic
        has_education = any(word in user_content for word in [
            "degree", "bsc", "msc", "phd", "university", "college", "education", "studied"
        ])
        
        has_career_goals = any(word in user_content for word in [
            "transition into", "become", "career", "job", "role", "industry", "position", "work as"
        ]) and not "not sure" in user_content and not "exploring options" in user_content
        
        has_knowledge = any(word in user_content for word in [
            "experience", "skills", "knowledge", "python", "java", "familiar", "proficient", "beginner", "advanced"
        ])
        
        # Check if off-topic
        is_off_topic = "weather" in user_content or "forecast" in user_content
        
        # Determine if content is suitable
        content_suitable = has_education and has_career_goals and has_knowledge and not is_off_topic
        
        return content_suitable