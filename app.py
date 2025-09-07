# app.py

import streamlit as st
import requests
import json

# --- Page Configuration ---
st.set_page_config(
    page_title="SatyaCheck AI",
    page_icon="🤖",
    layout="wide"
)

# --- App Title and Description ---
st.title("SatyaCheck: Your AI Misinformation Detector 🕵️‍♂️")
st.markdown("Enter a piece of text or a URL of a news article to analyze its credibility and detect potential misinformation.")

# --- API URL ---
API_URL = "https://satyacheck-api-479538600351.us-central1.run.app/analyze/"

# --- User Input Area ---
user_input = st.text_area("Enter Text or URL here:", height=200)

# --- Analysis Button and Output ---
if st.button("Analyze"):
    if user_input:
        with st.spinner("Analyzing... This may take a moment."):
            try:
                # Prepare the data to send to the API
                payload = {"content": user_input}
                
                # Send the request to your FastAPI backend
                response = requests.post(API_URL, json=payload)
                response.raise_for_status() # Raise an exception for bad status codes
                
                # Get the analysis from the response
                analysis = response.json()
                
                # --- NEW LINES FOR DEBUGGING ---
                # These lines will display the raw JSON response from the API,
                # which will help us see the exact error message.
                st.subheader("Raw API Response (for debugging):")
                st.json(analysis)
                # ------------------------------

                # --- Display the Results ---
                st.subheader("Analysis Results")
                
                # Check if there's an error in the response before trying to display results
                if "error" not in analysis:
                    # Display the trust score
                    score = analysis.get("trust_score", 0)
                    st.metric("Trust Score", f"{score}/100")

                    # Display the summary
                    st.write("**Summary:**", analysis.get("summary", "N/A"))

                    # Display the red flags
                    flags = analysis.get("analysis_flags", [])
                    if flags:
                        st.write("**🚩 Red Flags Detected:**")
                        for flag in flags:
                            st.warning(flag.replace("_", " ").title())

                    # Display the detailed breakdown
                    st.write("**Educational Breakdown:**")
                    st.info(analysis.get("educational_breakdown", "N/A"))

                    # Display the bias rating
                    st.write("**Detected Bias:**", analysis.get("bias_rating", "N/A"))
                else:
                    st.error(f"The API returned an error: {analysis['error']}")


            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to the analysis API: {e}")
            except json.JSONDecodeError:
                st.error("Error: Could not decode the response from the API. The server might be down or having issues.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
    else:
        st.warning("Please enter some text or a URL to analyze.")
