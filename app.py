from dotenv import load_dotenv

load_dotenv()  # Load all the environment variables

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini Pro Vision API and get response
def get_gemini_repsonse(image, prompt):
    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content([image[0], prompt])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
# Initialize our streamlit app
st.set_page_config(page_title="Gemini Health App")

# Add custom CSS for background image and general styling
st.markdown(
    """
    <style>
    /* Background styling */
    .stApp {
        background-image: url('172947390913.png');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }

    /* Header styling */
    .Header {
        color: #ffffff;
        text-align: center;
        font-family: 'Arial', sans-serif;
    }

    /* Input field styling */
    .stTextInput {
        background-color: rgba(255, 255, 255, 0.8);
        border-radius: 10px;
        padding: 10px;
    }

    /* File uploader styling */
    .stFileUploader {
        background-color: rgba(255, 255, 255, 0.8);
        border-radius: 10px;
        padding: 10px;
    }

    /* Button styling */
    .stButton button {
        background-color: #28a745;
        color: white;
        font-size: 18px;
        padding: 10px 20px;
        border-radius: 10px;
        border: none;
        cursor: pointer;
    }

    /* Button hover effect */
    .stButton button:hover {
        background-color: #ffff;
    }

    /* Image display styling */
    img {
        border-radius: 15px;
        margin-top: 20px;
        size:fit;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.header("Welcome to SmartBite 🍽️")

# Removed the input prompt section

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Tell me the total calories 🍔🥗")

input_prompt = """
You are a professional nutritionist. Analyze the food items in the given image and perform a detailed assessment. For each food item identified, provide the following information:
use emoji for the uploaded photo
1. Name of the Food item
Additionally, calculate the total calorie count for the meal and offer suggestions on how to make the dish healthier if needed 
2. Exact calorie count per serving 
3. A clear evaluation of whether the food is healthy or unhealthy
4. Key health benefits and nutritional value of the food
5. Best time of day to consume this food for optimal health benefits (e.g., breakfast, lunch, post-workout)
6. Suggest serving size based on recognized dietary standards
7. Overall health rating (excellent, good, moderate, poor) based on the nutritional quality of the food with the help of 5 star rating n the form of emoji
8. Recommendations for seasonal alternatives that can enhance both taste and nutrition

Focus on personalized guidance, ensuring the assessment helps in building a balanced, nutrient-rich diet for overall well-being.
add emoji accordin to your wise
"""

if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_repsonse(image_data, input_prompt)
    st.subheader("The Response is")
    st.write(response)
