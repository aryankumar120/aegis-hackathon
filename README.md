# 🛡️ Aegis: The Autonomous AI Talent Validation Platform
Live Demo: https://aegis-hackathon-demo.streamlit.app/

Aegis is an autonomous, multi-agent AI system designed to objectively measure a candidate's technical skill and "AI Fluency" in a simulated, real-world environment. This project was developed for the HackOmatic 2025: Agentic AI Hackathon.

# Explore the App:
  <img width="1459" height="789" alt="Screenshot 2025-09-20 at 7 59 32 PM" src="https://github.com/user-attachments/assets/56e42774-9d13-4331-9cc8-348723764ca1" />


# ► Project Demo
(This is where you would place a GIF showing the full workflow: generating a challenge, the candidate workspace, and the final dashboard.)

- The Problem: Measuring "AI Fluency"
- The hackathon sponsor, Calyptus, has a powerful mission: to provide companies with "rigorously vetted, AI-fluent talent." But how do you truly measure a developer's ability to leverage AI?

- A resume can list skills, but it can't prove them.

- A traditional coding test measures logic but misses the crucial element of how a developer uses AI tools to accelerate their work and solve problems more effectively.

- This creates a major bottleneck in modern technical hiring—it's subjective, inconsistent, and fails to identify truly elite, AI-native talent.

# The Solution: An Autonomous Assessment Platform
- Aegis solves this problem by creating a dynamic, end-to-end assessment pipeline powered by a team of collaborating AI agents. It goes beyond simple code validation to analyze the entire process, providing a holistic view of a candidate's abilities.

# ✨ Core Features
- Dynamic Challenge Generation: Creates unique, relevant technical challenges based on any job description.

- Interactive Candidate Workspace: A simulated environment with an integrated AI Assistant for a realistic assessment experience.

- Automated Code Validation: A secure sandbox environment runs the candidate's code to check for errors and correctness.

- Intelligent, Multi-Agent Evaluation: A sophisticated agent analyzes not just the final code, but how the candidate leveraged the AI assistant to get there.

- Data-Driven Results Dashboard: Presents a comprehensive evaluation with quantifiable metrics, including a unique "AI Fluency Score."

# 🤖 The Multi-Agent System
- Aegis is powered by a team of four specialized AI agents, each with a distinct role:

- The Architect Agent: Acts as an expert hiring manager, analyzing a job description to design a fair and relevant technical challenge.

- The Helper Agent: Functions as a senior teammate, providing intelligent assistance and guidance to the candidate during the assessment without giving away the solution.

- The Validator Tool: A secure code execution tool that runs the candidate's final submission and reports on its success or failure.

- The Assessor Agent: The core of our system. It synthesizes the code, the validation report, and the full AI chat transcript to produce a final, data-driven evaluation dashboard.

# 🛠️ Tech Stack
- Frontend: Streamlit

- LLM Provider: Groq (for high-speed Llama 3.1 inference)

- Core AI Framework: LangChain

- Language: Python

- Development: VS Code, Git/GitHub

# 🚀 Getting Started (Local Setup)
Follow these steps to run the project on your local machine.

1. Prerequisites
Python 3.9+

git installed on your machine

2. Clone the Repository
git clone [https://github.com/aryankumar120/aegis-hackathon.git](https://github.com/aryankumar120/aegis-hackathon.git)
cd aegis-hackathon

3. Set Up a Virtual Environment
It's highly recommended to use a virtual environment to manage dependencies.

# Create the virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

4. Install Dependencies
Install all the required libraries from the requirements.txt file.

pip install -r requirements.txt

5. Configure Your API Key
The application requires a Groq API key to function.

Create a file named .env in the root of the project directory.

Add your API key to this file in the following format:

GROQ_API_KEY="gsk_YourSecretKeyHere"

6. Run the Application
Once the setup is complete, you can run the Streamlit app with the following command:

streamlit run app.py

The application should now be running in your web browser!

# 🔮 Future Enhancements
- Support for Multiple Languages: Extend the Validator to run code in languages like JavaScript, Java, etc.

- Time Tracking: Implement a visible timer during the assessment and include "Completion Time" as a metric on the final dashboard.

- Historical Analysis: Add a database to store results, allowing recruiters to track candidate performance over time.

