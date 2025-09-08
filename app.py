import streamlit as st
import requests
import json
import time

# Page configuration
st.set_page_config(
    page_title="SatyaCheck - Navigate the Noise. Find the Truth.",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    /* Color Variables */
    :root {
        --primary-color: #0A3D62;
        --background-color: #FDFEFE;
        --text-color: #2C3E50;
        --accent-color: #00B894;
        --warning-color: #F1C40F;
        --info-bg: rgba(52, 152, 219, 0.1);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Hero Section Styling */
    .hero-section {
        background: linear-gradient(135deg, #0A3D62 0%, #00B894 100%);
        padding: 4rem 2rem;
        border-radius: 20px;
        margin-bottom: 3rem;
        color: white;
        text-align: center;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        line-height: 1.2;
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        font-weight: 400;
        margin-bottom: 2rem;
        opacity: 0.9;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
    }
    
    .hero-visual {
        width: 100%;
        height: 300px;
        background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.3) 100%);
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-top: 2rem;
        position: relative;
        overflow: hidden;
    }
    
    .hero-visual::before {
        content: '';
        position: absolute;
        width: 200%;
        height: 200%;
        background: 
            radial-gradient(circle at 20% 50%, rgba(0,184,148,0.3) 0%, transparent 50%),
            radial-gradient(circle at 80% 50%, rgba(10,61,98,0.3) 0%, transparent 50%);
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translate(0, 0) rotate(0deg); }
        50% { transform: translate(-10px, -10px) rotate(180deg); }
    }
    
    .hero-icon {
        font-size: 4rem;
        z-index: 1;
        position: relative;
    }
    
    /* Feature Cards */
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid #f0f0f0;
        height: 100%;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
    }
    
    .feature-icon {
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, #0A3D62, #00B894);
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 1.5rem;
        font-size: 1.5rem;
        color: white;
    }
    
    .feature-title {
        font-size: 1.4rem;
        font-weight: 600;
        color: #0A3D62;
        margin-bottom: 1rem;
    }
    
    .feature-description {
        color: #7f8c8d;
        line-height: 1.6;
        font-size: 1rem;
    }
    
    /* Steps Section */
    .steps-section {
        background: #f8f9fa;
        padding: 4rem 2rem;
        border-radius: 20px;
        margin: 3rem 0;
    }
    
    .steps-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 700;
        color: #2C3E50;
        margin-bottom: 1rem;
    }
    
    .steps-subtitle {
        text-align: center;
        color: #7f8c8d;
        font-size: 1.2rem;
        margin-bottom: 3rem;
    }
    
    .step-card {
        text-align: center;
        padding: 2rem 1rem;
    }
    
    .step-number {
        width: 80px;
        height: 80px;
        background: linear-gradient(135deg, #0A3D62, #00B894);
        border-radius: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1.5rem;
        font-size: 1.5rem;
        color: white;
    }
    
    .step-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #2C3E50;
        margin-bottom: 1rem;
    }
    
    .step-description {
        color: #7f8c8d;
        line-height: 1.6;
    }
    
    /* CTA Section */
    .cta-section {
        background: linear-gradient(135deg, #0A3D62 0%, #00B894 100%);
        padding: 4rem 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin: 3rem 0;
    }
    
    .cta-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    .cta-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
        margin-bottom: 2rem;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 3rem 2rem;
        color: #7f8c8d;
        border-top: 1px solid #ecf0f1;
        margin-top: 3rem;
    }
    
    .footer-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #0A3D62;
        margin-bottom: 0.5rem;
    }
    
    /* App Page Styling */
    .app-header {
        background: linear-gradient(90deg, #0A3D62 0%, #00B894 100%);
        padding: 1rem 2rem;
        margin: -1rem -1rem 2rem -1rem;
        color: white;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .app-title {
        font-size: 1.5rem;
        font-weight: 600;
    }
    
    .analysis-container {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin-bottom: 2rem;
    }
    
    .analysis-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2C3E50;
        margin-bottom: 1rem;
    }
    
    .results-container {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin-top: 2rem;
    }
    
    .trust-score {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #00B894, #0A3D62);
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
    }
    
    .trust-score-value {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .trust-score-label {
        font-size: 1.2rem;
        opacity: 0.9;
    }
    
    .flag-pill {
        display: inline-block;
        background: #F1C40F;
        color: #2C3E50;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        margin: 0.25rem;
        font-weight: 500;
        font-size: 0.9rem;
    }
    
    .educational-box {
        background: rgba(52, 152, 219, 0.1);
        padding: 2rem;
        border-radius: 15px;
        border-left: 5px solid #3498db;
        margin: 1rem 0;
    }
    
    .educational-box h4 {
        color: #2C3E50;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    .summary-box {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #00B894;
        font-style: italic;
        color: #2C3E50;
        margin: 1rem 0;
    }
    
    .checkmark-list {
        list-style: none;
        padding: 0;
        margin: 1.5rem 0;
    }
    
    .checkmark-list li {
        padding: 0.5rem 0;
        position: relative;
        padding-left: 2rem;
        color: white;
    }
    
    .checkmark-list li::before {
        content: "✓";
        position: absolute;
        left: 0;
        color: #00B894;
        font-weight: bold;
        font-size: 1.2rem;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #00B894, #0A3D62) !important;
        color: white !important;
        border: none !important;
        padding: 0.75rem 2rem !important;
        border-radius: 50px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(0,184,148,0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(0,184,148,0.4) !important;
    }
    
    .secondary-button {
        background: transparent !important;
        color: white !important;
        border: 2px solid white !important;
        padding: 0.75rem 2rem !important;
        border-radius: 50px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .secondary-button:hover {
        background: white !important;
        color: #0A3D62 !important;
    }
    
    /* Loading Animation */
    .loading-container {
        text-align: center;
        padding: 3rem;
    }
    
    .loading-spinner {
        border: 4px solid #f3f3f3;
        border-top: 4px solid #00B894;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        animation: spin 1s linear infinite;
        margin: 0 auto 1rem;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
        }
        
        .hero-subtitle {
            font-size: 1.1rem;
        }
        
        .steps-title, .cta-title {
            font-size: 2rem;
        }
        
        .feature-card {
            margin-bottom: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'landing'

if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None

if 'analyzing' not in st.session_state:
    st.session_state.analyzing = False

# API Configuration
API_URL = "https://satyacheck-api-479538600351.us-central1.run.app/analyze/"

def analyze_content(content):
    """Send content to the backend API for analysis"""
    try:
        payload = {"content": content}
        response = requests.post(API_URL, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        return {"error": "Analysis timed out. Please try again with shorter content."}
    except requests.exceptions.RequestException as e:
        return {"error": f"Connection error: {str(e)}"}
    except json.JSONDecodeError:
        return {"error": "Invalid response from analysis service."}

def render_landing_page():
    """Render the landing page"""
    
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <div style="display: flex; align-items: center; justify-content: space-between; max-width: 1200px; margin: 0 auto;">
            <div style="flex: 1; text-align: left; padding-right: 2rem;">
                <h1 class="hero-title">Navigate the<br><span style="color: #00B894;">Noise</span>. Find the<br><span style="color: #00B894;">Truth</span>.</h1>
                <p class="hero-subtitle" style="text-align: left; margin-left: 0;">SatyaCheck is a free AI tool for the Indian digital community. Instantly analyze news articles and social media messages to detect misinformation, scams, and manipulation before you trust or share.</p>
                <div style="margin: 2rem 0;">
                    <ul class="checkmark-list">
                        <li>✓ Free to Use</li>
                        <li>✓ AI-Powered Analysis</li>
                        <li>✓ Instant Results</li>
                    </ul>
                </div>
            </div>
            <div style="flex: 1;">
                <div class="hero-visual">
                    <div class="hero-icon">🔍</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # CTA Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Launch SatyaCheck Tool", key="hero_cta", use_container_width=True):
            st.session_state.page = 'app'
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Three Simple Steps Section
    st.markdown("""
    <div class="steps-section">
        <h2 class="steps-title">Three Simple Steps to Certainty</h2>
        <p class="steps-subtitle">SatyaCheck makes it easy to verify any content you encounter online</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="step-card">
            <div class="step-number">📋</div>
            <h3 class="step-title">1. Paste Anything</h3>
            <p class="step-description">Copy any suspicious text—a WhatsApp forward, a social media post, or a news article URL—and paste it into our tool.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="step-card">
            <div class="step-number">🧠</div>
            <h3 class="step-title">2. Analyze with AI</h3>
            <p class="step-description">Our advanced AI, powered by Google's Gemini, reads the content in seconds. It checks for emotional language, unverifiable claims, logical fallacies, and other red flags.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="step-card">
            <div class="step-number">📚</div>
            <h3 class="step-title">3. Understand the 'Why'</h3>
            <p class="step-description">Receive an instant, easy-to-read report. We don't just give you a score; we give you an educational breakdown so you can learn to spot misinformation yourself.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Features Section
    st.markdown("""
    <div style="margin: 4rem 0;">
        <h2 style="text-align: center; font-size: 2.5rem; font-weight: 700; color: #2C3E50; margin-bottom: 1rem;">Your Personal Digital Literacy Coach</h2>
        <p style="text-align: center; color: #7f8c8d; font-size: 1.2rem; margin-bottom: 3rem;">Advanced AI-powered features designed to educate and protect you from misinformation</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🛡️</div>
            <h3 class="feature-title">Instant Trust Score</h3>
            <p class="feature-description">Provides an at-a-glance credibility rating from 0 to 100, helping you make a quick initial judgment.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎓</div>
            <h3 class="feature-title">The Educational Breakdown</h3>
            <p class="feature-description">This is the core of SatyaCheck. We provide a detailed but simple explanation of the red flags found. This feature is designed to empower you with the critical thinking skills needed to navigate the modern internet safely.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">⚠️</div>
            <h3 class="feature-title">Red Flag Detection</h3>
            <p class="feature-description">Our AI is trained to identify specific manipulation techniques, such as Urgency Tactics, Ad Hominem attacks, and the use of loaded language. We show you exactly which tactics are being used.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">👁️</div>
            <h3 class="feature-title">Uncover Hidden Bias</h3>
            <p class="feature-description">The tool analyzes the tone and framing of the text to identify potential political, commercial, or other forms of bias, helping you see the bigger picture.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Final CTA Section
    st.markdown("""
    <div class="cta-section">
        <h2 class="cta-title">A Safer Digital India Starts with You.</h2>
        <p class="cta-subtitle">Take the first step. Analyze a message and see the truth for yourself.</p>
        <div style="display: flex; justify-content: center; gap: 1rem; margin-top: 2rem;">
            <div style="display: flex; gap: 2rem; align-items: center;">
                <span>💯 100% Free</span>
                <span>⚡ Instant Results</span>
                <span>🚫 No Registration</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Launch SatyaCheck for Free", key="final_cta", use_container_width=True):
            st.session_state.page = 'app'
            st.rerun()
    
    # Footer
    st.markdown("""
    <div class="footer">
        <h3 class="footer-title">SatyaCheck 🔍</h3>
        <p>Empowering India with the tools to navigate digital misinformation and build a more informed society.</p>
        <br>
        <div style="display: flex; justify-content: center; gap: 2rem; margin: 2rem 0;">
            <div>
                <strong>Learn More</strong><br>
                About SatyaCheck<br>
                How It Works<br>
                Digital Literacy Guide<br>
                Privacy Policy
            </div>
            <div>
                <strong>Get in Touch</strong><br>
                Building a safer digital India, one analysis at a time.<br>
                support@satyacheck.in<br>
                Contact Us
            </div>
        </div>
        <p style="margin-top: 2rem; padding-top: 2rem; border-top: 1px solid #ecf0f1;">
            © 2024 SatyaCheck. Made with ❤️ for a more informed India. All rights reserved.
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_app_page():
    """Render the application page"""
    
    # App Header
    st.markdown("""
    <div class="app-header">
        <div class="app-title">SatyaCheck 🔍</div>
        <div style="color: rgba(255,255,255,0.8);">AI-Powered Analysis</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Back to Home button
    if st.button("← Back to Home", key="back_to_home"):
        st.session_state.page = 'landing'
        st.session_state.analysis_result = None
        st.session_state.analyzing = False
        st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Main analysis container
    st.markdown("""
    <div class="analysis-container">
        <h2 class="analysis-title">Analyze Content for Misinformation</h2>
        <p style="color: #7f8c8d; margin-bottom: 2rem;">Paste any suspicious text, news article, or social media content below</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Input section
    user_content = st.text_area(
        "",
        placeholder="Paste your WhatsApp forward, news URL, or any suspicious text here...",
        height=200,
        key="content_input"
    )
    
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        analyze_button = st.button(
            "🧠 Analyze Content",
            key="analyze_button",
            disabled=not user_content.strip() or st.session_state.analyzing,
            use_container_width=True
        )
    
    # Handle analysis
    if analyze_button and user_content.strip():
        st.session_state.analyzing = True
        st.session_state.analysis_result = None
        st.rerun()
    
    # Show loading state
    if st.session_state.analyzing:
        st.markdown("""
        <div class="loading-container">
            <div class="loading-spinner"></div>
            <h3>Analyzing your content...</h3>
            <p>Our AI is examining the text for misinformation patterns, bias, and manipulation techniques.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Perform the analysis
        result = analyze_content(user_content.strip())
        st.session_state.analysis_result = result
        st.session_state.analyzing = False
        st.rerun()
    
    # Display results
    if st.session_state.analysis_result:
        result = st.session_state.analysis_result
        
        if "error" in result:
            st.error(f"❌ Analysis Error: {result['error']}")
            st.info("💡 Try pasting the content directly instead of using a URL, or check if the URL is accessible.")
        else:
            st.markdown('<div class="results-container">', unsafe_allow_html=True)
            
            # Trust Score
            trust_score = result.get('trust_score', 'N/A')
            if trust_score != 'N/A':
                try:
                    score_value = int(trust_score)
                    score_color = "#e74c3c" if score_value < 30 else "#f39c12" if score_value < 70 else "#27ae60"
                except:
                    score_value = trust_score
                    score_color = "#3498db"
                
                st.markdown(f"""
                <div class="trust-score" style="background: linear-gradient(135deg, {score_color}, #0A3D62);">
                    <div class="trust-score-value">{score_value}</div>
                    <div class="trust-score-label">Trust Score (0-100)</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Summary
            summary = result.get('summary', '')
            if summary:
                st.markdown("### 📋 Analysis Summary")
                st.markdown(f'<div class="summary-box">{summary}</div>', unsafe_allow_html=True)
            
            # Red Flags
            flags = result.get('analysis_flags', [])
            if flags:
                st.markdown("### 🚩 Detected Red Flags")
                flags_html = ""
                for flag in flags:
                    flags_html += f'<span class="flag-pill">{flag}</span>'
                st.markdown(flags_html, unsafe_allow_html=True)
            
            # Educational Breakdown (Main feature)
            breakdown = result.get('educational_breakdown', '')
            if breakdown:
                st.markdown("""
                <div class="educational-box">
                    <h4>🎓 Educational Breakdown - Learn to Spot Misinformation</h4>
                    <p style="line-height: 1.6; margin: 0;">{}</p>
                </div>
                """.format(breakdown), unsafe_allow_html=True)
            
            # Bias Rating
            bias = result.get('bias_rating', '')
            if bias:
                st.markdown("### 👁️ Detected Bias")
                st.markdown(f"**Bias Assessment:** {bias}")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Reset button
            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns([2, 1, 2])
            with col2:
                if st.button("🔄 Analyze Another", key="reset_button", use_container_width=True):
                    st.session_state.analysis_result = None
                    st.session_state.analyzing = False
                    st.rerun()
    
    # Default state - no results yet
    elif not st.session_state.analyzing:
        st.markdown("""
        <div style="text-align: center; padding: 4rem 2rem; color: #7f8c8d;">
            <div style="font-size: 4rem; margin-bottom: 2rem;">🧠</div>
            <h3>Your detailed analysis report will appear here</h3>
            <p>Paste any content above and click "Analyze Content" to get started</p>
        </div>
        """, unsafe_allow_html=True)

# Main app logic
def main():
    if st.session_state.page == 'landing':
        render_landing_page()
    elif st.session_state.page == 'app':
        render_app_page()

if __name__ == "__main__":
    main()