import streamlit as st
import requests
import json
from PIL import Image
from io import BytesIO

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
    image_data = response.json()['data'][0]['url']
    image_response = requests.get(image_data)
    image = Image.open(BytesIO(image_response.content))
    return image

# Streamlit app main function
def main():
    st.set_page_config(page_title='SynthMatix', layout='wide')
    
    # Sidebar for API key input
    st.sidebar.title('Settings')
    api_key = st.sidebar.text_input("Enter your API key:", type="password")

    # Main header
    st.title('SynthMatix: AI-Driven Material Design')

    # Columns for layout
    col1, col2 = st.columns(2)

    with col1:
        st.subheader('Material Properties')
        properties_prompt = st.text_area("Enter the desired properties for the new material (e.g., lightweight, durable, high thermal conductivity):", height=150)
        generate_button = st.button('Generate Material Description')

    with col2:
        st.subheader('Generated Material')
        if generate_button and api_key and properties_prompt:
            # GPT-4 prompt for generating material description
            gpt_prompt = f"Create a comprehensive description for a new material with the following properties: {properties_prompt}. The material should be suitable for use in renewable energy applications, such as solar panels or wind turbines."
            material_description = call_gpt4(api_key, gpt_prompt)
            st.write(material_description)

            # DALL-E prompt for visualizing the material
            dalle_prompt = f"Visualize a futuristic material with the following characteristics: {properties_prompt}. This material is designed for high efficiency in renewable energy applications."
            material_image = call_dalle(api_key, dalle_prompt)
            st.image(material_image, caption="Generated Material Visualization")

        else:
            st.error("Please enter both an API key and the desired properties to generate the material description.")

if __name__ == "__main__":
    main()
