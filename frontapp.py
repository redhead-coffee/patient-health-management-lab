import streamlit as st
import requests

API_URL = "http://localhost:8000/predict"

st.title("Insurance Charge Prediction")

st.markdown("Enter the details below to predict the insurance charge:")
age = st.number_input("Age", min_value=0, max_value=120, value=30)

sex = st.selectbox(
    "Sex",
    options=["male", "female"]
)

height = st.number_input(
    "Height (in cm)",
    min_value=0.0,
    value=170.0
)

weight = st.number_input(
    "Weight (in kg)",
    min_value=0.0,
    value=70.0
)

children = st.number_input(
    "Number of Children",
    min_value=0,
    value=0
)

smoker = st.selectbox(
    "Are you a smoker?",
    options=["yes", "no"]
)

region = st.selectbox(
    "Region",
    options=["northeast", "northwest", "southeast", "southwest"]
)

if st.button("Predict"):
    input_data = {
        "age": age,
        "sex": sex,
        "height": height,
        "weight": weight,
        "children": children,
        "smoker": smoker,
        "region": region
    }
    
    try:
        response = requests.post(API_URL, json=input_data)
        if response.status_code == 200:
            result = response.json()
            st.success(f"Predicted Insurance Charge: ${result['predicted_charge']:.2f}")
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    except requests.RequestException as e:
        st.error(f"Error occurred while making the API request: {e}")
