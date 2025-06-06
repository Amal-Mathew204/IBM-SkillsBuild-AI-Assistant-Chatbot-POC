import os
import requests
import torch
from peft import PeftModel
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
        base_model_id = "meta-llama/Llama-3.2-3B-Instruct"
        hf_token = "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"

        self.tokenizer = AutoTokenizer.from_pretrained(
            base_model_id,
            token=hf_token
        )
        base_model = AutoModelForCausalLM.from_pretrained(
            base_model_id,
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True,
            token=hf_token
        )

        self.model = PeftModel.from_pretrained(base_model, model_path,
                                                      low_cpu_mem_usage=True)

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
        is_suitable, missing_info = self._assess_quality(conversation)
        print("Is suitable for search: ", is_suitable)
        print("Conversation history: ", conversation_history)
        print("Missing Info: ", missing_info)
        courses = []
        # Only generate a response if the conversation is NOT suitable for search
        response = None
        if not is_suitable:
            response = self._generate_follow_up_questions(conversation, missing_info)
        else:
            search_context = self.create_search_context(conversation)
            courses = self.get_courses_from_semantic_search(search_context)
            courses = self.generate_individual_justifications(conversation, courses)
        
        return {
            "response": response,
            "courses": courses
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
        Assess if the conversation is suitable for semantic search by checking if all required information is provided.
        
        Args:
            conversation (list): List of message objects with role and content
            
        Returns:
            bool, dict: Whether the conversation is suitable for semantic search and a dictionary of missing information
        """
        # Extract user content from the conversation
        user_content = ' '.join([turn["content"].lower() for turn in conversation if turn["role"] == "user"])
        
        # Identify missing information
        missing_info = {}

        has_education = any(word in user_content for word in [
            "degree", "bsc", "msc", "phd", "university", "college", "education", "studied"
        ])
        if not has_education:
            missing_info["education"] = "Can you tell me about your education background?"

        has_career_goals = any(word in user_content for word in [
            "transition into", "become", "career", "job", "role", "industry", "position", "work as"
        ]) and not "not sure" in user_content and not "exploring options" in user_content
        if not has_career_goals:
            missing_info["career_goals"] = "What is your desired career role or industry?"

        has_knowledge = any(word in user_content for word in [
            "experience", "skills", "knowledge", "python", "java", "familiar", "proficient", "beginner", "advanced"
        ])
        if not has_knowledge:
            missing_info["knowledge"] = "What technical skills or programming languages are you familiar with?"

        # Check if off-topic
        is_off_topic = "weather" in user_content or "forecast" in user_content
        
        # Determine if content is suitable (all required info is available)
        content_suitable = has_education and has_career_goals and has_knowledge and not is_off_topic
        
        return content_suitable, missing_info

    def get_courses_from_semantic_search(self, context: str) -> list[dict] | None:
        """
        Method retrieves courses from semantic search container
        
        Args:
            context(str): String containing information to find a course for the user 
                          extracted information from the user conversation
        Returns:
            list[dict]: list of course objects
            None: Returned if No courses was obtained from the container
        """
        url: str = f"http://semanticsearch:{os.getenv('SEMANTIC_SEARCH_PORT')}/{context}/{5}"
        response = requests.get(url, timeout=30)
        print("Semantic Search Response: ")
        print(response.status_code)
        print(response.text)
        if response.status_code == 200:
            courses = response.json()
            return courses
        return None
    
    def extract_search_metadata(self, conversation):
        """
        Extract educational background, career aspirations, and current knowledge
        from the conversation for semantic search.
        
        Args:
            conversation (list): List of message objects with role and content
            
        Returns:
            dict: Extracted metadata
        """
        # Join all user messages
        user_content = ' '.join([turn["content"] for turn in conversation if turn["role"] == "user"])
        user_content_lower = user_content.lower()
        
        # Extract educational background
        education_keywords = [
            "degree", "bsc", "msc", "phd", "university", "college", "education", "studied",
            "bachelor", "master", "graduate", "school"
        ]
        education_fields = [
            "computer science", "engineering", "mathematics", "physics", "biology", "economics", 
            "business", "marketing", "psychology", "nursing", "medicine"
        ]
        
        education_background = "Not specified"
        education_sentences = []
        
        # Find sentences containing education keywords
        for sentence in user_content.split('.'):
            sentence = sentence.strip()
            if any(keyword in sentence.lower() for keyword in education_keywords):
                education_sentences.append(sentence)
        
        if education_sentences:
            education_background = '. '.join(education_sentences)
        
        # Check for professional titles (which imply education)
        professional_titles = ["nurse", "doctor", "physician", "engineer", "scientist", "professor"]
        if education_background == "Not specified" and any(title in user_content_lower for title in professional_titles):
            for sentence in user_content.split('.'):
                if any(title in sentence.lower() for title in professional_titles):
                    education_background = sentence.strip()
                    break
        
        # Extract career aspirations
        career_keywords = [
            "become", "transition into", "work as", "career", "job", "role", "position",
            "data scientist", "data analyst", "healthcare data analysis", "analyze", "bioinformatics"
        ]
        
        career_aspirations = "Not specified"
        career_sentences = []
        
        # Find sentences containing career keywords
        for sentence in user_content.split('.'):
            sentence = sentence.strip()
            if any(keyword in sentence.lower() for keyword in career_keywords):
                career_sentences.append(sentence)
        
        if career_sentences:
            career_aspirations = '. '.join(career_sentences)
        
        # Extract knowledge level
        knowledge_keywords = [
            "experience", "skills", "knowledge", "python", "java", "r", "sql", "tableau", "excel",
            "programming", "statistical", "analysis", "beginner", "intermediate", "advanced"
        ]
        
        knowledge_level = "Not specified"
        knowledge_sentences = []
        
        # Find sentences containing knowledge keywords
        for sentence in user_content.split('.'):
            sentence = sentence.strip()
            if any(keyword in sentence.lower() for keyword in knowledge_keywords):
                knowledge_sentences.append(sentence)
        
        if knowledge_sentences:
            knowledge_level = '. '.join(knowledge_sentences)
        
        # Handle "no programming experience" case
        if knowledge_level == "Not specified" and "no programming" in user_content_lower:
            for sentence in user_content.split('.'):
                if "no programming" in sentence.lower():
                    knowledge_level = sentence.strip()
                    break
        
        return {
            "education_background": education_background,
            "career_aspirations": career_aspirations,
            "knowledge_level": knowledge_level
        }
    
    def create_search_context(self, conversation):
        """
        Create a formatted string from extracted metadata for semantic search.
        
        Args:
            conversation (list): List of message objects with role and content
            
        Returns:
            str: Formatted context string for semantic search
        """
        metadata = self.extract_search_metadata(conversation)
        
        # Format as a single string for semantic search
        search_context = (
            f"Educational Background: {metadata['education_background']}. "
            f"Career Aspirations: {metadata['career_aspirations']}. "
            f"Knowledge Level: {metadata['knowledge_level']}."
        )
        
        return search_context
    
    def generate_individual_justifications(self, conversation, courses_data):
        """
        Generate individual justifications for each course based on user information.
        
        Args:
            conversation (list): List of message objects with role and content
            courses_data (list): List of course objects returned from semantic search
            
        Returns:
            list: Original courses with added justification field
        """
        # Extract all user input for context
        user_input = " ".join([turn["content"] for turn in conversation if turn["role"] == "user"])
        
        # Process each course individually
        justified_courses = []
        
        for course in courses_data:
            # Get course title/name
            course_title = course.get("title", course.get("name", "Unknown Course"))
            
            # Create conversation with this specific course
            formatted_turns = []
            for turn in conversation:
                formatted_turns.append({"role": turn["role"], "content": turn["content"]})
            
            # Add a message recommending this specific course
            formatted_turns.append({
                "role": "assistant", 
                "content": f"Based on your background, I recommend the course: {course_title}"
            })
            
            # Ask for justification
            formatted_turns.append({
                "role": "user",
                "content": "Why is this course specifically beneficial for my background?"
            })
            
            # Format for the model
            formatted_prompt = self.tokenizer.apply_chat_template(formatted_turns, tokenize=False, add_generation_prompt=True)
            
            # Generate the justification
            with torch.no_grad():
                outputs = self.model.generate(
                    self.tokenizer(formatted_prompt, return_tensors="pt").to(self.model.device).input_ids,
                    max_new_tokens=256,
                    do_sample=True,
                    temperature=0.7,
                    top_p=0.9
                )
            
            # Extract only the justification
            output = self.tokenizer.decode(outputs[0], skip_special_tokens=False)
            justification = output.split("<|start_header_id|>assistant<|end_header_id|>")[-1].split("<|eot_id|>")[0].strip()
            
            # Create a copy of the course and add justification
            course_copy = course.copy()
            course_copy["justification"] = justification
            justified_courses.append(course_copy)
        
        return justified_courses
    
    def _generate_follow_up_questions(self, conversation, missing_info):
        """
        Generate a response with follow-up questions based on the missing information.
        
        Args:
            conversation (list): List of message objects with role and content
            missing_info (dict): Dictionary of missing information categories
            
        Returns:
            str: The assistant's response with appropriate follow-up questions
        """
        # If there's no conversation yet, generate a welcome message
        if len(conversation) == 0:
            welcome_message = (
                "Welcome to the IBM Skills Build data science course assistant! "
                "To help you find the most relevant courses, I'd like to know about your background. "
                "Could you tell me about your educational background or any degrees/qualifications you've completed?"
            )
            return welcome_message
        
        # Create a modified conversation with a hint about missing information
        prompt_conversation = conversation.copy()
        
        # Add a subtle hint about what information is missing
        hint = ""
        if "education" in missing_info:
            hint = "The user needs to provide educational background information."
        elif "career_goals" in missing_info:
            hint = "The user needs to provide career goals or aspirations."
        elif "knowledge" in missing_info:
            hint = "The user needs to provide information about their current knowledge level or technical skills."
        
        if hint:
            # Add a system message with the hint
            prompt_conversation.append({
                "role": "system",
                "content": hint + " Ask a follow-up question to gather the required details. Do not recommend courses."
            })
        
        # Let the fine-tuned model generate the follow-up question
        formatted_prompt = self.tokenizer.apply_chat_template(prompt_conversation, tokenize=False, add_generation_prompt=True)
        
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

    def _assess_quality_new(self, conversation):
        """
        Assess if the conversation is suitable for semantic search by checking if all required information is provided
        using the LLM's ability to evaluate content, without generating follow-up questions.
        
        Args:
            conversation (list): List of message objects with role and content
        
        Returns:
            bool, dict: Whether the conversation is suitable for semantic search and a dictionary of missing information
        """
            # Extract user content from the conversation
        user_content = ' '.join([turn["content"] for turn in conversation if turn["role"] == "user"])

        # Refined prompt for the LLM to assess the conversation
        prompt = (
            f"Based on the following conversation, assess if the user has provided sufficient information about the following categories:\n"
            f"1. Education\n"
            f"2. Career Goals (Specific to Data Science)\n"
            f"3. Knowledge (Technical Skills for Data Science)\n\n"
            f"Here is the conversation:\n\n{user_content}\n\n"
            f"Answer only with the following format:\n"
            f"Education: Provided or Education: Missing\n"
            f"Career Goals: Provided or Career Goals: Missing\n"
            f"Knowledge: Provided or Knowledge: Missing\n\n"
            f"To assess the categories:\n"
            
            # Education assessment
            f"1. Education: Look for mentions of academic qualifications or certifications.\n"
            f"   Examples: Bachelor’s, Master’s, PhD, data science certifications, etc.\n\n"
            
            # Career Goals assessment (Specific to Data Science)
            f"2. Career Goals: Look for mentions of career goals in data science, AI, machine learning, etc.\n"
            f"   Examples: Data scientist, machine learning engineer, AI researcher, etc.\n\n"
            
            # Knowledge (Technical Skills) assessment
            f"3. Knowledge: Look for mentions of technical skills, programming languages, tools, or techniques in data science.\n"
            f"   Examples:\n"
            f"- Programming languages (Python, R, SQL, Scala)\n"
            f"- Data science tools (TensorFlow, PyTorch, Pandas, NumPy, Scikit-learn)\n"
            f"- Machine learning techniques (e.g., regression, classification)\n"
            f"- Big data tools (Hadoop, Spark)\n\n"
            f"Do not generate any additional conversation or explanations. Just provide the assessment in the requested format."
        )

        # Tokenize and pass the refined prompt to the LLM for evaluation
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        with torch.no_grad():
            outputs = self.model.generate(
                inputs["input_ids"],
                max_new_tokens=256,
                do_sample=False,  # Ensure deterministic output
                top_p=0.9
            )

        # Decode the LLM's response
        output = self.tokenizer.decode(outputs[0], skip_special_tokens=False)
        output = output.split(prompt)[1]
        print("Output: ", output)
        # Initialize a dictionary to hold missing information details
        missing_info = {}

        # Process the LLM's response (we assume it returns in the correct format)
        if "Education: Missing" in output:
            missing_info["education"] = "Can you tell me about your educational background?"
        if "Career Goals: Missing" in output:
            missing_info["career_goals"] = "What is your desired career role or industry?"
        if "Knowledge: Missing" in output:
            missing_info["knowledge"] = "What technical skills or programming languages are you familiar with?"

        # Check if the conversation is suitable for semantic search (i.e., all required information is provided)
        content_suitable = not any(key in missing_info for key in ["education", "career_goals", "knowledge"])

        return content_suitable, missing_info