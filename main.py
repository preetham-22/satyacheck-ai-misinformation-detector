# main.py

from fastapi import FastAPI
from pydantic import BaseModel
import core_analyzer # Import our analysis script

# Create a FastAPI app instance
app = FastAPI()

# Define the structure of the request body
class RequestBody(BaseModel):
    content: str

# Define our API's root endpoint for a quick test
@app.get("/")
def read_root():
    return {"message": "SatyaCheck API is running!"}

# Define the main analysis endpoint
@app.post("/analyze/")
async def analyze_content(request: RequestBody):
    """
    Receives text or a URL, processes it using our core_analyzer,
    and returns the JSON analysis.
    """
    user_content = request.content
    analysis_result = core_analyzer.process_input(user_content)
    return analysis_result