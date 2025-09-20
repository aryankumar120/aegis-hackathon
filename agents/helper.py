from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough

def create_helper_agent(model_name="llama-3.3-70b-versatile"):
    """
    Creates and returns the Helper Agent chain.
    This agent answers the candidate's questions during the assessment.
    """
    helper_template = """
    ROLE: You are an expert-level programmer and a helpful AI assistant.

    TASK: Your task is to answer a job candidate's question about a technical challenge they are working on.
    Be helpful and provide accurate information, code snippets, and explanations.

    IMPORTANT: DO NOT give away the final answer to the overall challenge. Your goal is to help them
    with specific technical questions, just like a senior colleague would. Guide them, but don't do the work for them.

    Here is the candidate's question:
    {question}
    """
    
    prompt = PromptTemplate(
        template=helper_template,
        input_variables=["question"],
    )

    llm = ChatGroq(model_name=model_name, temperature=0.3)
    
    chain = (
        {"question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain