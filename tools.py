# in tools.py
import io
import sys
from contextlib import redirect_stdout

def code_executor(code: str) -> dict:
    """
    Executes a string of Python code and returns its output or errors.
    """
    # Use an in-memory text buffer to capture print statements
    buffer = io.StringIO()
    
    try:
        # Redirect standard output to our buffer
        with redirect_stdout(buffer):
            # Execute the code
            exec(code)
        
        # Get the content of the buffer
        output = buffer.getvalue()
        
        return {"status": "success", "output": output}
        
    except Exception as e:
        # If any error occurs during execution
        error_message = f"Error: {str(e)}"
        return {"status": "error", "output": error_message}