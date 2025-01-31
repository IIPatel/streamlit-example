import os
import time
import openai
import streamlit as st
import json
import time

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

thread = client.beta.threads.create()

def submit_message(assistant_id, thread, user_message):
    client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=user_message
    )
    return client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )

def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run

def get_response(thread):
    return client.beta.threads.messages.list(thread_id=thread.id, order="asc")

def pretty_print(messages):
    responses = []
    for m in messages:
        if m.role == "assistant":
            responses.append(m.content[0].text.value)
    return "\n".join(responses)


# Streamlit UI for sidebar configuration
st.sidebar.title("Configuration")
entered_api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")

# Check if an API key is entered, then initialize the OpenAI client
client = None
if entered_api_key:
    with st.spinner('Initializing OpenAI Client...'):
        client = initialize_openai_client(entered_api_key)

# Sidebar for selecting the assistant
assistant_option = st.sidebar.selectbox(
    "Select an Assistant",
    ("Financial Assistant", "PDF Analyzer")
)

if assistant_option == "Financial Assistant":
    st.title("Financial Assistants :bar_chart:")

    # Description
    st.markdown("""
        This assistant is your go-to resource for financial insights and advice. Here's what you can do:
        - :page_facing_up: **Analyze financial statements** to understand your company's health.
        - :chart_with_upwards_trend: **Track market trends** and make informed investment decisions.
        - :moneybag: Receive tailored **investment advice** to maximize your portfolio's performance.
        - :bulb: **Explore various financial scenarios** and plan strategically for future ventures.

        Simply enter your financial query below and let the assistant guide you with actionable insights.
    """)
    user_query = st.text_input("Enter your financial query:")

    if st.button('Get Financial Insight') and client:
        with st.spinner('Fetching your financial insights...'):
            thread = client.beta.threads.create()
            run = submit_message("asst_PWxRJ5oOqEHx0CisVEBpFgKI", thread, user_query)
            run = wait_on_run(run, thread)
            response_messages = get_response(thread)
            response = pretty_print(response_messages)
            st.text_area("Response:", value=response, height=300)

                assistant = client.beta.assistants.update(
                    'asst_PWxRJ5oOqEHx0CisVEBpFgKI',
                    file_ids=[file_response.id],
                )
                thread = client.beta.threads.create()
                run = submit_message('asst_PWxRJ5oOqEHx0CisVEBpFgKI', thread, user_query)
                run = wait_on_run(run, thread)
                response_messages = get_response(thread)
                response = pretty_print(response_messages)
                st.text_area("Response:", value=response, height=300)
            except Exception as e:
                st.error(f"An error occurred: {e}")

# Show a message if the API key is not entered
if not client:
    st.warning("Please enter your OpenAI API key in the sidebar to use the app.")
