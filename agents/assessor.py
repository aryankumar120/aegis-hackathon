import json
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough

def create_assessor_agent(model_name="llama-3.3-70b-versatile"):
    """
    Creates and returns the Assessor Agent chain.
    This agent evaluates the candidate's submission and returns a structured JSON object.
    """
    assessor_template = """
    ROLE: You are 'Aegis Assessor', a world-class technical hiring manager. Your analysis is objective, fair, and insightful.

    TASK: Evaluate a job candidate's submission and provide your analysis as a JSON object.

    CONTEXT: The candidate's code was run in a sandboxed environment that DOES NOT have external libraries like pandas or matplotlib. You MUST NOT penalize the candidate for `ModuleNotFoundError`. Your job is to evaluate the LOGIC of the code, assuming the libraries were present.

    EVIDENCE: You will receive a block of text containing a 'Code Execution Report', the 'Final Solution' code, and the 'AI Assistant Chat Transcript'.

    INSTRUCTIONS:
    1.  Analyze all evidence holistically.
    2.  Provide scores for 'Technical Skill' and 'AI Fluency' on a scale of 1 to 10.
    3.  Write a brief, insightful summary for 'Code Validation', 'Strengths', and 'Weaknesses'.
    4.  Format your entire output as a single, valid JSON object. DO NOT add any text or formatting before or after the JSON object.

    JSON SCHEMA:
    {{
      "technical_score": <integer>,
      "ai_fluency_score": <integer>,
      "code_validation_summary": "<string>",
      "strengths": "<string>",
      "weaknesses": "<string>"
    }}

    Now, analyze the following evidence and provide your response in the specified JSON format.
    ---
    EVIDENCE:
    {evidence}
    ---
    """

    prompt = PromptTemplate(
        template=assessor_template,
        input_variables=["evidence"],
    )

    llm = ChatGroq(model_name=model_name, temperature=0.1)

    chain = (
        {"evidence": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain

