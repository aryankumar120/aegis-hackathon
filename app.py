import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

st.set_page_config(page_title="Aegis Demo", layout="wide")

st.title("🛡️ Aegis: The Autonomous AI Talent Validation Platform")
st.write("Welcome to the MVP for the HackOmatic 2025 Hackathon!")

# Check if the API key is loaded
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    st.success("Google API Key loaded successfully! We are ready to build.")
else:
    st.error("Google API Key not found. Please create a .env file and add your GOOGLE_API_KEY.")

# --- UI Components for the App ---
st.subheader("1. Define the Job Role")
job_description = st.text_area("Paste the Job Description here:", height=200)

if st.button("Generate Assessment", type="primary"):
    if job_description:
        with st.spinner("Architect Agent is designing the challenge..."):
            # This is where we will call our first agent in the next step!
            st.write("Challenge generation logic will be implemented here.")
    else:
        st.warning("Please paste a job description first.")