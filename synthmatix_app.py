import streamlit as st
import requests
import json

# Define the function to call the GPT-4 API
def call_gpt4(api_key, prompt):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }
    
    data = {
        'prompt': prompt,
        'max_tokens': 150
    }
    
    response = requests.post('https://api.openai.com/v1/engines/davinci-codex/completions', headers=headers, data=json.dumps(data))
    return response.json()['choices'][0]['text']

# Define the function to call the DALL-E API
def call_dalle(api_key, prompt):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }
    
    data = {
        'prompt': prompt,
        'n': 1,
        'size': '1024x1024'
    }
    
    response = requests.post('https://api.openai.com/v1/images/generations', headers=headers, data=json.dumps(data))
    return response.json()['data'][0]['url']

# Streamlit app main function
def main():
    st.title('SynthMatix: AI-Driven Material Design')

    # User input for API key
    api_key = st.text_input("Enter your API key:")

    # User input for material properties
    properties_prompt = st.text_input("Enter the desired properties for the new material (e.g., lightweight, durable, high thermal conductivity):")

    # Button to trigger material generation
    if st.button('Generate Material Description'):
        if api_key and properties_prompt:
            # GPT-4 prompt
            gpt_prompt = " "  # Add your GPT-4 prompt here
            material_description = call_gpt4(api_key, gpt_prompt)
            st.subheader("Material Description")
            st.write(material_description)

            # DALL-E prompt
            dalle_prompt = " "  # Add your DALL-E prompt here
            material_image_url = call_dalle(api_key, dalle_prompt)
            st.subheader("Material Visualization")
            st.image(material_image_url, caption="Generated Material Visualization")
        else:
            st.error("Please enter both an API key and the desired properties to generate the material description.")

if __name__ == "__main__":
    main()
