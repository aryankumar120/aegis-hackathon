import streamlit as st
import os
import time
import json
from dotenv import load_dotenv
from agents.architect import create_architect_agent
from agents.assessor import create_assessor_agent
from agents.helper import create_helper_agent
from tools import code_executor

# --- Page Configuration ---
st.set_page_config(
    page_title="Aegis Demo",
    layout="wide"
)

# --- Custom Styling for Dashboard ---
st.markdown("""
<style>
    /* Increase header font sizes for the dashboard */
    h3 {
        font-size: 26px !important;
    }
    h4 {
        font-size: 20px !important;
    }
    /* Increase metric label font size */
    div[data-testid="stMetricLabel"] {
        font-size: 18px !important;
    }
    /* Ensure summary containers have a minimum height to look balanced */
    div[data-testid="stVerticalBlock"] div[data-testid="stVerticalBlock"] div[data-testid="stVerticalBlock"] div.st-emotion-cache-12w0qpk {
        min-height: 200px;
    }
</style>
""", unsafe_allow_html=True)


# --- Load API Keys ---
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("GROQ_API_KEY not found. Please create a .env file and add your key.")
    st.stop()

# --- Initialize Session State ---
if 'stage' not in st.session_state:
    st.session_state.stage = 'generate'
if 'challenge' not in st.session_state:
    st.session_state.challenge = None
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'evaluation' not in st.session_state:
    st.session_state.evaluation = None
if 'start_time' not in st.session_state:
    st.session_state.start_time = None

# --- Helper functions ---
def set_stage(stage_name):
    st.session_state.stage = stage_name
    if stage_name == 'assessment':
        st.session_state.start_time = time.time()

def reset_app():
    st.session_state.stage = 'generate'
    st.session_state.challenge = None
    st.session_state.messages = []
    st.session_state.evaluation = None
    st.session_state.start_time = None


# =================================================================================================
# --- STAGE 1: GENERATE CHALLENGE (Recruiter View) ---
# =================================================================================================
if st.session_state.stage == 'generate':
    st.title("🛡️ Aegis: The Autonomous AI Talent Validation Platform")
    st.write("Welcome! This platform allows you to generate a custom assessment, have a candidate complete it with AI assistance, and receive an automated evaluation of their performance and AI fluency.")
    
    st.subheader("1. Define the Job Role")
    job_description = st.text_area(
        "Paste the Job Description here:",
        height=200,
        placeholder="e.g., Senior Data Analyst with experience in Python, SQL, and Power BI..."
    )

    if st.button("Generate Assessment", type="primary"):
        if job_description:
            with st.spinner("🤖 Architect Agent is designing the challenge..."):
                architect_agent = create_architect_agent()
                st.session_state.challenge = architect_agent.invoke(job_description)
        else:
            st.warning("Please paste a job description first.")

    if st.session_state.challenge:
        st.divider()
        st.subheader("📝 Generated Challenge")
        st.markdown(st.session_state.challenge)
        st.button("Start Assessment", type="primary", on_click=set_stage, args=('assessment',))

# =================================================================================================
# --- STAGE 2: ASSESSMENT WORKSPACE (Candidate View) ---
# =================================================================================================
elif st.session_state.stage == 'assessment':
    st.header("Assessment in Progress")

    with st.expander("📌 View Challenge Details", expanded=True):
        st.markdown(st.session_state.challenge)

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Candidate Workspace")
        solution_code = st.text_area("", height=500, placeholder="Write your code or notes here...", key="solution_code")

    with col2:
        st.subheader("🤖 AI Assistant")
        chat_container = st.container(height=500, border=True)
        with chat_container:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

        if prompt := st.chat_input("Ask for help or clarification..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.spinner("Assistant is thinking..."):
                helper_agent = create_helper_agent()
                response = helper_agent.invoke(prompt)
                st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()

    st.divider()
    
    if st.button("Submit Final Assessment", type="primary"):
        final_solution = st.session_state.get("solution_code", "")
        
        with st.spinner("🤖 Validator Agent is running the code..."):
            validation_result = code_executor(final_solution)

        with st.spinner("🤖 Assessor Agent is reviewing the submission..."):
            chat_history = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages])
            evidence = f"""
            ## Code Execution Report from Validator Agent:
            Status: {validation_result['status']}
            Output:
            {validation_result['output']}
            ---
            ## Final Solution Submitted by Candidate:
            ```python
            {final_solution}
            ```
            ---
            ## AI Assistant Chat Transcript:
            {chat_history}
            """
            assessor_agent = create_assessor_agent()
            evaluation_json_str = assessor_agent.invoke(evidence)
            
            try:
                evaluation_data = json.loads(evaluation_json_str)
                evaluation_data['code_accepted'] = validation_result['status'] == 'success'
                st.session_state.evaluation = evaluation_data
            except (json.JSONDecodeError, TypeError):
                st.session_state.evaluation = {"error": "Failed to parse evaluation.", "raw_output": evaluation_json_str}
        
        set_stage('results')
        st.rerun()

# =================================================================================================
# --- STAGE 3: RESULTS DASHBOARD (Recruiter View) ---
# =================================================================================================
elif st.session_state.stage == 'results':
    st.header("📊 Assessment Dashboard")
    st.info("The Validator has run the code and the Assessor has completed its review.")

    if st.session_state.evaluation and 'error' not in st.session_state.evaluation:
        eval_data = st.session_state.evaluation
        
        # --- Top Row Metrics ---
        st.markdown("<h3>Key Metrics</h3>", unsafe_allow_html=True)
        
        accuracy = f"{eval_data.get('technical_score', 0) * 10}%"
        code_accepted = "✔️ Accepted" if eval_data.get('code_accepted') else "❌ Rejected"
        technical_score = f"{eval_data.get('technical_score', 0)} / 10"
        ai_score = f"{eval_data.get('ai_fluency_score', 0)} / 10"

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Accuracy", accuracy)
        col2.metric("Code Validation", code_accepted)
        col3.metric("Technical Score", technical_score)
        col4.metric("AI Fluency Score", ai_score)
        
        st.divider()
        
        # --- Bottom Row: Summaries ---
        st.markdown("<h3>Detailed Summaries</h3>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            with st.container(border=True):
                st.markdown("<h4>Code Validation Summary</h4>", unsafe_allow_html=True)
                st.info(f"{eval_data.get('code_validation_summary', 'No summary provided.')}")
            
        with col2:
            with st.container(border=True):
                st.markdown("<h4>Strengths</h4>", unsafe_allow_html=True)
                st.success(f"{eval_data.get('strengths', 'No strengths identified.')}")
            
        with col3:
            with st.container(border=True):
                st.markdown("<h4>Weaknesses</h4>", unsafe_allow_html=True)
                st.warning(f"{eval_data.get('weaknesses', 'No weaknesses identified.')}")
    
    else:
        st.error("There was an error generating the assessment report.")
        if st.session_state.evaluation and 'raw_output' in st.session_state.evaluation:
            st.code(st.session_state.evaluation['raw_output'])

    st.button("Start New Assessment", type="primary", on_click=reset_app)

