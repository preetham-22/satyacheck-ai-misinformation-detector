import streamlit as st
import requests
import json
import time

# --- Part 3: Global Design System ---
PRIMARY_COLOR = "#0A3D62"  # Navy
BACKGROUND_COLOR = "#FDFEFE"  # Off-White
TEXT_COLOR = "#2C3E50"  # Charcoal
ACCENT_COLOR = "#00B894"  # Green
WARNING_COLOR = "#F1C40F"  # Yellow
INFO_BOX_BG = "rgba(52, 152, 219, 0.1)" # Light Blue

# Set Streamlit page configuration
st.set_page_config(
    page_title="SatyaCheck: Navigate the Noise. Find the Truth.",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

        html, body, [class*="st-"] {{
            font-family: 'Inter', sans-serif;
            color: {TEXT_COLOR};
            background-color: {BACKGROUND_COLOR};
        }}
        .stButton>button {{
            background-color: {PRIMARY_COLOR};
            color: {BACKGROUND_COLOR};
            border-radius: 8px;
            border: none;
            padding: 10px 20px;
            font-size: 16px;
            font-weight: 600;
            transition: all 0.2s ease-in-out;
            cursor: pointer;
        }}
        .stButton>button:hover {{
            background-color: {ACCENT_COLOR};
            color: {PRIMARY_COLOR};
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: {PRIMARY_COLOR};
            font-weight: 700;
        }}
        .stMarkdown h1 {{
            font-size: 3.5em; /* Larger hero headline */
            line-height: 1.1;
        }}
        .stMarkdown h2 {{
            font-size: 2.5em;
            margin-top: 1.5em;
            margin-bottom: 0.8em;
        }}
        .stMarkdown h3 {{
            font-size: 1.8em;
            margin-top: 1em;
        }}
        .stMarkdown p {{
            font-size: 1.1em;
            line-height: 1.6;
        }}
        .stTextInput>div>div>input, .stTextArea>div>div>textarea {{
            border-radius: 8px;
            border: 1px solid #D1D9E6;
            padding: 10px;
            box-shadow: inset 0 1px 3px rgba(0,0,0,0.06);
            transition: all 0.2s ease-in-out;
        }}
        .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {{
            border-color: {PRIMARY_COLOR};
            box-shadow: 0 0 0 2px rgba(10, 61, 98, 0.2);
            outline: none;
        }}
        .feature-card {{
            background-color: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.05);
            text-align: center;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            transition: transform 0.2s ease-in-out;
        }}
        .feature-card:hover {{
            transform: translateY(-5px);
        }}
        .feature-card h3 {{
            color: {ACCENT_COLOR};
            margin-bottom: 10px;
        }}
        .check-item {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 10px;
            font-weight: 600;
            color: {PRIMARY_COLOR};
        }}
        .check-item svg {{
            color: {ACCENT_COLOR};
            font-size: 1.2em;
        }}
        .info-box {{
            background-color: {INFO_BOX_BG};
            border-left: 5px solid {PRIMARY_COLOR};
            padding: 20px;
            border-radius: 8px;
            margin-top: 20px;
            margin-bottom: 20px;
        }}
        .tag {{
            display: inline-block;
            background-color: {WARNING_COLOR};
            color: {TEXT_COLOR};
            padding: 5px 12px;
            border-radius: 20px;
            margin: 5px;
            font-size: 0.9em;
            font-weight: 600;
        }}
        .stMetric {{
            background-color: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            margin-bottom: 20px;
        }}
        .stMetric > div > div:first-child {{
            font-size: 1.2em;
            color: {PRIMARY_COLOR};
            font-weight: 600;
        }}
        .stMetric > div > div:last-child {{
            font-size: 3em;
            font-weight: 700;
            color: {ACCENT_COLOR};
        }}
        footer {{ visibility: hidden; }} /* Hide default Streamlit footer */
    </style>
""", unsafe_allow_html=True)

# Backend API URL
BACKEND_API_URL = "https://satyacheck-api-479538600351.us-central1.run.app/analyze/"

# --- Helper Functions ---
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# --- Part 4: The Landing Page ---
def render_landing_page():
    # Hero Section
    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown(f"<h1>Navigate the Noise.<br>Find the Truth.</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size:1.4em;'>SatyaCheck is a free AI tool for the Indian digital community. Instantly analyze news articles and social media messages to detect misinformation, scams, and manipulation before you trust or share.</p>", unsafe_allow_html=True)

        if st.button("Analyze Your First Article Now", key="hero_cta"):
            st.session_state.page = "app"
            st.experimental_rerun()

        st.markdown(f"""
            <div style='margin-top: 20px;'>
                <div class='check-item'>✔ Free to Use</div>
                <div class='check-item'>✔ AI-Powered Analysis</div>
                <div class='check-item'>✔ Instant Results</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        # Abstract Visual
        st.markdown(
            """
            <div style="
                background: linear-gradient(135deg, rgba(10, 61, 98, 0.8), rgba(0, 184, 148, 0.8));
                border-radius: 20px;
                height: 350px;
                width: 100%;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-size: 3em;
                font-weight: bold;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                box-shadow: 0 10px 30px rgba(0,0,0,0.15);
            ">
                🔍 AI Insights
            </div>
            """, unsafe_allow_html=True
        )

    st.markdown("---") # Separator

    # Features Section
    st.markdown("<h2>Your Personal Digital Literacy Coach</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:1.1em; text-align: center; margin-bottom: 40px;'>Empowering you to navigate the digital world with confidence.</p>", unsafe_allow_html=True)

    feature_cols = st.columns(4)
    features = [
        {"title": "Instant Trust Score", "description": "Get a clear, concise rating of the content's reliability."},
        {"title": "Red Flag Detection", "description": "Identify propaganda, clickbait, and other manipulative tactics."},
        {"title": "The Educational Breakdown", "description": "Understand *why* content is suspicious, enhancing your digital literacy."},
        {"title": "Uncover Hidden Bias", "description": "Reveals underlying political, commercial, or ideological slants."}
    ]

    for i, feature in enumerate(features):
        with feature_cols[i]:
            st.markdown(f"""
                <div class="feature-card">
                    <h3>{feature['title']}</h3>
                    <p>{feature['description']}</p>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("---") # Separator

    # Final CTA
    st.markdown(f"""
        <div style="
            background-color: {PRIMARY_COLOR};
            padding: 50px 30px;
            border-radius: 12px;
            text-align: center;
            color: {BACKGROUND_COLOR};
            margin-top: 50px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        ">
            <h2 style="color: {BACKGROUND_COLOR}; margin-bottom: 20px;">A Safer Digital India Starts with You.</h2>
            <p style='font-size:1.2em; margin-bottom: 30px;'>Join the movement to build a more informed and resilient online community.</p>
            <button class='stButton' style='background-color:{ACCENT_COLOR}; color:{PRIMARY_COLOR};' onclick="window.parent.document.querySelector('[data-testid=stButton]>button').click();">Launch SatyaCheck for Free</button>
        </div>
    """, unsafe_allow_html=True)

    # Need to simulate the button click for the HTML button
    if st.button("Launch SatyaCheck for Free", key="final_cta_hidden", use_container_width=True):
        st.session_state.page = "app"
        st.experimental_rerun()


    # Footer
    st.markdown(f"""
        <div style="
            text-align: center;
            margin-top: 60px;
            padding-top: 30px;
            border-top: 1px solid #e0e0e0;
            color: #777;
            font-size: 0.9em;
        ">
            <p><strong>SatyaCheck</strong> – Combatting misinformation for a digitally literate India.</p>
        </div>
    """, unsafe_allow_html=True)

# --- Part 5: The Application Page ---
def render_app_page():
    # Header
    col_header_btn, col_header_title = st.columns([1, 5])
    with col_header_btn:
        if st.button("← Back to Home", key="back_to_home"):
            st.session_state.page = "landing"
            st.experimental_rerun()
    with col_header_title:
        st.markdown(f"<h1 style='text-align: center; font-size: 2.5em;'>SatyaCheck Analysis Tool</h1>", unsafe_allow_html=True)

    st.markdown("---")

    # Input Component
    st.markdown(f"<p style='font-size:1.1em; text-align: center; margin-bottom: 20px;'>Paste your WhatsApp forward, news URL, or any suspicious text below and let SatyaCheck analyze it for you.</p>", unsafe_allow_html=True)
    user_input = st.text_area(
        "Content to Analyze:",
        height=250,
        placeholder="Paste your WhatsApp forward, news URL, or any suspicious text here...",
        key="user_content_input"
    )

    analyze_button = st.button("Analyze with AI", key="analyze_button", use_container_width=True)

    # Backend Connection and Output
    if analyze_button and user_input:
        with st.spinner("Analyzing content... This might take a moment as our AI processes the information."):
            try:
                payload = {"content": user_input}
                headers = {"Content-Type": "application/json"}
                response = requests.post(BACKEND_API_URL, json=payload, headers=headers)
                response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
                analysis_result = response.json()

                if "error" in analysis_result:
                    st.error(f"**Analysis Error:** {analysis_result['error']}")
                else:
                    st.session_state.last_analysis = analysis_result
                    st.session_state.show_results = True

            except requests.exceptions.ConnectionError:
                st.error("**Connection Error:** Could not connect to the SatyaCheck API. Please check your internet connection or try again later.")
            except requests.exceptions.Timeout:
                st.error("**Timeout Error:** The request to the SatyaCheck API timed out. This might be due to network issues or a very long analysis.")
            except requests.exceptions.RequestException as e:
                st.error(f"**An unexpected error occurred during API call:** {e}")
            except json.JSONDecodeError:
                st.error("**API Response Error:** Could not decode the JSON response from the API. The server might have returned an invalid response.")
    elif analyze_button and not user_input:
        st.warning("Please paste some content or a URL to analyze.")

    # Display Results
    if st.session_state.get("show_results") and st.session_state.get("last_analysis"):
        results = st.session_state.last_analysis
        st.markdown("---")
        st.markdown("<h2>Analysis Results:</h2>", unsafe_allow_html=True)

        # Trust Score
        st.metric(label="Overall Trust Score (0-100)", value=f"{results.get('trust_score', 'N/A')}")

        # Summary
        if results.get('summary'):
            st.markdown(f"<p style='font-style: italic; font-size: 1.1em;'><blockquote>{results['summary']}</blockquote></p>", unsafe_allow_html=True)

        st.markdown("<h3>Red Flags Detected:</h3>", unsafe_allow_html=True)
        if results.get('analysis_flags'):
            flag_html = "".join([f"<span class='tag'>{flag}</span>" for flag in results['analysis_flags']])
            st.markdown(f"<div>{flag_html}</div>", unsafe_allow_html=True)
        else:
            st.info("No significant red flags detected in this content.")

        # Educational Breakdown
        st.markdown("<h3>The Educational Breakdown:</h3>", unsafe_allow_html=True)
        if results.get('educational_breakdown'):
            st.markdown(f"<div class='info-box'><p>{results['educational_breakdown']}</p></div>", unsafe_allow_html=True)
        else:
            st.info("No detailed educational breakdown available for this content.")

        # Bias Rating
        st.markdown("<h3>Detected Bias:</h3>", unsafe_allow_html=True)
        if results.get('bias_rating'):
            st.markdown(f"<p><strong>{results['bias_rating']}</strong></p>", unsafe_allow_html=True)
        else:
            st.info("Bias rating not available.")

        # Reset Button
        st.markdown("---")
        if st.button("Analyze New Content", key="reset_analysis", use_container_width=True):
            st.session_state.user_content_input = "" # Clear the text area
            st.session_state.show_results = False
            st.session_state.last_analysis = None
            st.experimental_rerun()


# --- Main Application Logic ---
if __name__ == "__main__":
    if "page" not in st.session_state:
        st.session_state.page = "landing"
    if "show_results" not in st.session_state:
        st.session_state.show_results = False
    if "last_analysis" not in st.session_state:
        st.session_state.last_analysis = None
    if "user_content_input" not in st.session_state:
        st.session_state.user_content_input = ""

    if st.session_state.page == "landing":
        render_landing_page()
    elif st.session_state.page == "app":
        render_app_page()