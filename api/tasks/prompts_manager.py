from huggingface_hub import InferenceClient
from .utils import scrape_JSON
from langchain.chains import LLMChain
import openai
import ast



def handle_prompt(messages):

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    print(response['choices'][0]['message']['content'])
    return ast.literal_eval(response['choices'][0]['message']['content'])