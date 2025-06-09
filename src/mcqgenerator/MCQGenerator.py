from langchain.prompts import PromptTemplate
from langchain.chains import SequentialChain
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Access API key
api_key = os.getenv("GOOGLE_API_KEY")

# Create a quiz generation prompt template
quiz_generation_template = """
You are an expert quiz creator specializing in creating multiple-choice questions (MCQs) for {subject} students at {tone} level.

Based on the following text, create {number} multiple-choice questions that test the understanding of key concepts.

TEXT: {text}

For each question:
1. Frame a clear question
2. Provide 4 options labeled as A, B, C, and D with only one correct answer
3. Indicate the correct answer

Format your response as a valid JSON object matching this exact structure:
{response_json}

Ensure your response contains ONLY the JSON object and nothing else.
"""

quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "number", "subject", "tone", "response_json"],
    template=quiz_generation_template
)

# Create an evaluation prompt template
evaluation_template = """
You are an expert in evaluating multiple-choice questions (MCQs) for accuracy.

Please evaluate the following {number} MCQs for {subject} at {tone} level.
Make sure each question:
1. Has a clearly defined correct answer
2. Is relevant to the subject matter
3. Has no factual errors
4. Is grammatically correct

If you find any errors or possible improvements, please suggest modifications.

MCQs:
{quiz}

Format your response as a JSON object similar to the input, but with any necessary corrections.
"""

evaluation_prompt = PromptTemplate(
    input_variables=["number", "subject", "tone", "quiz"],
    template=evaluation_template
)

# Initialize the LLM
def get_llm():
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.3)
    return llm

# Create a runnable sequence for generating and evaluating MCQs
def create_generate_evaluate_chain():
    llm = get_llm()
    
    # Create the quiz generation runnable
    quiz_generator = quiz_generation_prompt | llm
    
    # Create the chain
    generate_evaluate_chain = quiz_generator
    
    return generate_evaluate_chain

# Create the chain
generate_evaluate_chain = create_generate_evaluate_chain()

