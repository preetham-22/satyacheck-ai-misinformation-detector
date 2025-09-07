SatyaCheck: AI-Powered Misinformation Detector
SatyaCheck is a web application designed to combat the spread of misinformation in India by providing users with an AI-powered tool to analyze the credibility of text and news articles. This project was built for a Generative AI hackathon.

The Problem
The rapid spread of fake news and misinformation poses a severe threat, leading to social unrest, public health crises, and financial scams. Simple fact-checking is not enough; users need to be educated on why a piece of content might be misleading to build long-term digital literacy.

Our Solution
SatyaCheck is a user-friendly tool that goes beyond simple fact-checking. It leverages the advanced reasoning capabilities of Google's Gemini model to provide a multi-faceted analysis, including:

Trust Score: An at-a-glance credibility rating.

Red Flag Detection: Identifies specific manipulation tactics like emotional language, lack of sources, and logical fallacies.

Educational Breakdown: The core feature. It explains in simple terms why the content is suspicious, teaching users to develop critical thinking skills.

Bias Detection: Identifies potential political or commercial bias.

Tech Stack
Frontend: Streamlit

Backend: FastAPI on Google Cloud Run

AI Model: Google Gemini on Vertex AI

Deployment: Docker, Google Cloud Build, Artifact Registry

How to Run the Frontend
The backend is a live API already deployed on Google Cloud Run. To run the user-facing web application on your local machine, follow these steps:

Clone the repository:

git clone [https://github.com/preetham-22/SatyaCheck-Hackathon.git](https://github.com/preetham-22/SatyaCheck-Hackathon.git)
cd SatyaCheck-Hackathon

Create and activate a virtual environment:

# Create the environment
python -m venv venv

# Activate on Windows
.\venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate

Install the required packages:

pip install -r requirements.txt

Run the Streamlit application:

streamlit run app.py

A new tab should open in your browser with the application running.