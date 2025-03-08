import streamlit as st 
import requests
import json
import pandas as pd
from PIL import Image

# CSS for button styling
st.markdown("""
    <style>
    .stButton button {
        background-color: #28a745;
        color: white;
        font-size: 20px;
        padding: 15px 50px;
        border-radius: 10px;
        border: none;
        width: 300px;
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    .stButton button:hover {
        background-color: #218838;
        color:black;
    }
    </style>
""", unsafe_allow_html=True)

# Logo and Title
image = "./images/logo.jpg"

col1, col2 = st.columns([1.5, 7])
with col1:
    st.image(image, width=400)
with col2:
    st.title("Penguin Classification Model")
    st.write("Penguin Species Classification: A Classification Model Based on Key Features.")

# Create a container with two columns
container = st.container()
col1, col2 = container.columns([1, 1])

# Left column: Feature selection
with col1:
    st.subheader("Select Input Features")
    island = st.selectbox("Island", ["Biscoe", "Dream", "Torgersen"])
    sex = st.selectbox("Sex", ["male", "female"])
    bill_length_mm = st.number_input("Bill Length (mm)", min_value=32.1, max_value=59.6, step=0.1)
    bill_depth_mm = st.number_input("Bill Depth (mm)", min_value=13.1, max_value=21.5, step=0.1)
    flipper_length_mm = st.number_input("Flipper Length (mm)", min_value=172, max_value=231, step=1)
    body_mass_g = st.number_input("Body Mass (gm)", min_value=2700, max_value=6300, step=1)
    
    if st.button("Predict"):
        # Prepare input features
        input_features = {
            "island": island,
            "sex": sex,
            "bill_length_mm": bill_length_mm,
            "bill_depth_mm": bill_depth_mm,
            "flipper_length_mm": flipper_length_mm,
            "body_mass_g": body_mass_g
        }
        
        # Make API request
        res = requests.post(url="http://127.0.0.1:8000/", json=input_features)
        
        # Display prediction results in the right column
        with col2:
            if res.status_code == 200:
                prediction = res.json()
                species = prediction['prediction'][0]
                st.subheader(f"Predicted Species: {species}")
                
                # Display image based on prediction
                if species == "Adelie":
                    image_path = "./images/adelie.webp"
                elif species == "Gentoo":
                    image_path = "./images/Gentoo.jpg"
                else:
                    image_path = "./images/Chinstrap.jpg"
                
                st.image(Image.open(image_path), caption=f"{species} Penguin", use_container_width=True)
            else:
                st.error(f"Error: {res.status_code} - {res.text}")
