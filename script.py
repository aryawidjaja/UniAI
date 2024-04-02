import os
import json
import openai
import pandas as pd
from openai import OpenAI, OpenAIError

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("The OPENAI_API_KEY environment variable is not set.")

# Set the OpenAI API key for the client
openai.api_key = OPENAI_API_KEY
model = "ft:gpt-3.5-turbo-1106:uniad:initial-vocab:98r2JvJf"
client = OpenAI(timeout=30)

def generate_vocab(subject, grade, level, topic, amount):
    function_answer_vocabulary = [
        {
            "name": "generate_vocabulary",
            "description": f"Act as an {subject} for {grade} student in level {level} in Singapore Syllabus, generate vocabularies for given queries in {subject} language.",
            "parameters": {
            "type": "object",
            "properties": {
                "answer": {
                    "type": "array",
                    "description": f"Generate {subject} vocabularies about {topic}. IMPORTANT: Make sure these {topic} vocabularies met the cognitive side of {level} level {grade} student.",
                    "items": {
                    "type": "string"
                }
                },
            },
            "answer": [
                "answer"
            ]
        }
        }]

    function_explanation_vocabulary = [
        {
            "name": "generate_vocabulary",
            "description": f"Act as an {subject} for {grade} student in level {level} in Singapore Syllabus, explain each vocabularies in the given list.",
            "parameters": {
            "type": "object",
            "properties": {
                "definition": {
                    "type": "string",
                    "description": f"""Give a fun definitions on the given vocabulary. Make sure your tone as soft as you are a cheerful teacher for {grade} student, and your explanation should align with the {level} English for {grade} student.
                    e.g. A crane is a very tall machine used to pick up and move heavy things that are too big for us to carry, like big pipes. Cars are for driving, planes fly in the sky, and trucks carry things on the road, but cranes do the heavy lifting.""",
                },
                "example": {
                    "type": "string",
                    "description": f"""Give a fun and exciting example of sentence that using given vocabulary.
                    Adjust your tone as soft as you are a cheerful {grade} teacher. Make sure your tone and example align with the {level} English for {grade} student.""",
                },
            },
            "required": [
                "definition",
                "example"
            ]
        }
        }]

    # Initialize variables
    answer = []
    desired_amount = int(amount)  # Make sure 'amount' is defined and is an integer
    attempts = 0
    max_attempts = 5  # Set a maximum number of attempts to avoid infinite loops

    while not answer or len(answer) != desired_amount and attempts < max_attempts:
        try:
            answerCompletion = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": f"You are UniAI, a Singaporean {subject} teacher for {grade} student. Help student to learn {grade} English. Refers to Singaporean education system. Answer in JSON"
                    },
                    {
                        "role": "user",
                        "content": f"Make a list of {amount} vocabularies in {subject} language about {topic} for level {level} {grade} student. ANSWER IN {subject} LANGUAGE",
                    },
                ],
                response_format={"type": "json_object"},
                functions=function_answer_vocabulary,
                max_tokens=4096,
                temperature=0.8,
                presence_penalty=0.6,
                top_p=0.8
            )

            output_answer = answerCompletion.choices[0].message.function_call.arguments
            answer = json.loads(output_answer).get('answer', '')

            # Check if 'answer' is a list and contains the desired amount of items
            if isinstance(answer, list) and len(answer) == desired_amount:
                break  # Exit loop if conditions are met
            else:
                answer = []  # Reset answer for the next iteration
                print("Lack of amount vocabularies generated. Retrying...")

        except OpenAIError as e:
            print(f"Error: {e}")
            print("Retrying...")

        attempts += 1  # Increment attempt counter

        if attempts == max_attempts:
            print("Maximum attempts reached, proceeding with the last received answer.")

    explanations = []

    for vocab in answer:
        explanationCompletion = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": f"You are UniAI, adjust your tone as you are {subject} teacher for {grade} student. Help student to learn about vocabularies by giving them the definition and example on how to use them. Refers to Singaporean education system. Answer in JSON"
                },
                {
                    "role": "user",
                    "content": f"This question is for {grade} grade {level} level, therefore adjust your tone as soft as you are talking to the {level} {grade} students. Explain this vocabulary and gives engaging example: {vocab}",
                },
            ],
            response_format={"type": "json_object"},
            functions=function_explanation_vocabulary,
            max_tokens=4096,
            temperature=0.8,
            presence_penalty=0.6,
            top_p=0.8
        )

        output_explanation = explanationCompletion.choices[0].message.function_call.arguments
        definition = json.loads(output_explanation).get('definition', '')
        example = json.loads(output_explanation).get('example', '')

        # Store each vocabulary, its definition, and example as a dictionary in the list
        explanations.append({
            "Vocabulary": vocab,
            "Definition": definition,
            "Example": example
        })
        result = explanations
        
    return result
