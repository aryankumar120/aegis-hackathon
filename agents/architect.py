from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough

def create_architect_agent(model_name="llama-3.3-70b-versatile"):
    """
    Creates and returns the Architect Agent chain using a valid, active model.
    """
    architect_template = """
    ROLE: You are an expert hiring manager and a senior technical architect named 'Aegis Architect'.

    TASK: Your task is to create a realistic, time-boxed, and insightful technical or business challenge
    for a job candidate based on the provided job description. The challenge must directly test the
    core competencies mentioned in the job description.

    INSTRUCTIONS:
    1.  Analyze the job description to identify the top 3-4 most critical skills.
    2.  Design a single, concise challenge that forces the candidate to use these skills.
    3.  Specify a reasonable time limit for the challenge (e.g., 60 minutes, 90 minutes).
    4.  Clearly define the expected deliverables or output from the candidate.
    5.  Format your entire output as a single block of Markdown text.

    Here is the job description:
    {job_description}
    """
    
    prompt = PromptTemplate(
        template=architect_template,
        input_variables=["job_description"],
    )

    llm = ChatGroq(model_name=model_name, temperature=0.2)
    
    chain = (
        {"job_description": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain