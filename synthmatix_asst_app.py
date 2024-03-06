import os
import time
import openai
import streamlit as st
import json

def initialize_openai_client(api_key):
    return openai.OpenAI(api_key=api_key)

from openai import OpenAI
client = OpenAI(api_key=OPENAI_KEY)

assistant = client.beta.assistants.create(
    name = "Finance Insight Analyst",
    instructions = "You are a helpful  financial analyst expert and, focusing on management discussions and financial results. help people learn about financial needs and guid them towards fincial literacy.",
    tools = [{"type":"code_interpreter"}, {"type": "retrieval"}],
    model = "gpt-4-1106-preview"



def show_json(obj):
    print(json.dumps(json.loads(obj.model_dump_json()), indent=4))

show_json(assistant)