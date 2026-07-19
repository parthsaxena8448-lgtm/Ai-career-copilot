import google.generativeai as genai
import streamlit as st

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-flash-latest")
response = model.generate_content("Say hello in one sentence.")

print(response.text)