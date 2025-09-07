# core_analyzer.py (Final Production Version)

import vertexai
from vertexai.generative_models import GenerativeModel
import json
import requests
from bs4 import BeautifulSoup

# --- Configuration ---
PROJECT_ID = "satyacheck-hackathon"
LOCATION = "us-central1"

# --- Initialization ---
vertexai.init(project=PROJECT_ID, location=LOCATION)

# --- Core AI Analysis Function ---
def analyze_text(text_to_analyze):
    model = GenerativeModel("gemini-2.0-flash-001")

    prompt = f"""
    Act as an expert misinformation analyst. Your task is to analyze the following text for signs of manipulation, bias, and falsehood.
    Content to Analyze:
    ---
    {text_to_analyze[:10000]}
    ---
    Provide your analysis in a structured JSON format. The JSON object must have the following keys and value types:
    1. "trust_score": An integer between 0 and 100.
    2. "summary": A neutral, one-sentence summary of the main claim.
    3. "analysis_flags": An array of strings identifying specific manipulation techniques found.
    4. "educational_breakdown": A concise, easy-to-understand explanation for a non-expert.
    5. "bias_rating": A string describing any detected bias.
    Do not include any text or formatting outside of the JSON object.
    """
    try:
        response = model.generate_content([prompt])
        json_string = response.text.strip().replace("```json", "").replace("```", "").strip()
        analysis_result = json.loads(json_string)
        return analysis_result
    except Exception as e:
        print(f"Caught an exception during AI analysis: {e}")
        return {"error": f"The AI model could not process the text. Details: {str(e)}"}

# --- URL and Text Processing Function ---
def process_input(user_input):
    user_input = user_input.strip()
    if user_input.startswith(('http://', 'https://')):
        print(f"Detected URL: {user_input}")
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
            response = requests.get(user_input, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            paragraphs = soup.find_all('p')
            scraped_text = ' '.join([p.get_text() for p in paragraphs])
            
            if not scraped_text:
                return {"error": "Could not find any paragraph text in the article."}
            return analyze_text(scraped_text)
        except requests.exceptions.HTTPError as e:
             if e.response.status_code == 403:
                return {"error": "This website blocks automated scraping. Please try pasting the article text directly."}
             else:
                return {"error": f"Could not fetch the URL. The website returned status code: {e.response.status_code}"}
        except requests.exceptions.RequestException as e:
            return {"error": f"Could not fetch the URL. Error: {e}"}
    else:
        print(f"Detected plain text...")
        return analyze_text(user_input)
