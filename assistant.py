# Step 1: Install and import the streamlit module
import openai
import streamlit as st

# Step 2: Create a text input widget
user_input = st.text_input("Enter your query:")

# Step 3: Display the Assistant's response
if user_input:
    # Use the same code as before to create and run the Assistant
    assistant = openai.Assistant.create(
    name="Simple Assistant",
    instructions="You are a simple assistant that can run Python code and search the web.",
    tools=[{"type": "code_interpreter"}, {"type": "retrieval"}],
    model="gpt-4-turbo-preview"
)
    thread = openai.Thread.create()
    message = openai.Message.create(
    thread=thread.id,
    text="I am a user. What can you do?"
)
    run = openai.Run.create(
    assistant=assistant.id,
    thread=thread.id
)
    # Use the streamlit.write function to show the response
    st.write(run.messages[-1].text)

# Step 4: Wrap the code in a loop
while True:
    # Repeat steps 2 and 3 until the user exits
    user_input = st.text_input("Enter your query:")
    if user_input:
        message = openai.Message.create(...)
        run = openai.Run.create(...)
        st.write(run.messages[-1].text)
    else:
        break
