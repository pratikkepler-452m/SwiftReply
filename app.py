import streamlit as st
import os
import database
import ai_engine

# Initialize Database
database.create_tables()

# Configure Streamlit Page
st.set_page_config(
    page_title="Swift Reply - AI Business Assistant",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Custom CSS
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

try:
    load_css("style.css")
except FileNotFoundError:
    pass # CSS file not found, will run without custom styles

# --- Session State Initialization ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "business_info" not in st.session_state:
    st.session_state.business_info = {
        "name": "Swift Reply",
        "industry": "AI SaaS",
        "services": "Next-Gen AI Conversations, Customer Support, Workflow Automation",
        "description": "We build billion-dollar AI experiences for modern startups.",
        "faq": "Q: Pricing? A: Enterprise grade.\nQ: Support? A: Infinite AI scale.",
        "tone": "Futuristic, Minimal, and Premium",
        "email": "hello@swiftreply.ai"
    }

if "chat_session" not in st.session_state:
    st.session_state.chat_session = None

if "show_lead_form" not in st.session_state:
    st.session_state.show_lead_form = False

# --- Sidebar: Business Configuration ---
with st.sidebar:
    st.markdown('''
    <div class="sidebar-logo-container">
        <svg width="32" height="32" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M42 20C42 15 36 12 32 12C26 12 22 16 22 22C22 30 42 32 42 42C42 48 38 52 32 52C26 52 22 48 22 42" stroke="#00D4FF" stroke-width="6" stroke-linecap="round"/>
            <path d="M32 6L32 14" stroke="#6C63FF" stroke-width="4" stroke-linecap="round"/>
            <path d="M32 50L32 58" stroke="#8B5CF6" stroke-width="4" stroke-linecap="round"/>
        </svg>
        <span class="sidebar-brand">Swift Reply</span>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown("### ⚙️ Engine Settings")
    with st.form("config_form"):
        st.session_state.business_info["name"] = st.text_input("Business Name", value=st.session_state.business_info["name"])
        st.session_state.business_info["industry"] = st.text_input("Industry", value=st.session_state.business_info["industry"])
        st.session_state.business_info["services"] = st.text_area("Services", value=st.session_state.business_info["services"], height=100)
        st.session_state.business_info["description"] = st.text_area("Company Description", value=st.session_state.business_info["description"], height=100)
        st.session_state.business_info["faq"] = st.text_area("FAQs", value=st.session_state.business_info["faq"], height=150)
        st.session_state.business_info["tone"] = st.selectbox(
            "Tone Style", 
            ["Professional and Friendly", "Strictly Professional", "Casual and Fun", "Persuasive and Sales-oriented"],
            index=0
        )
        st.session_state.business_info["email"] = st.text_input("Support Email", value=st.session_state.business_info["email"])
        
        submitted = st.form_submit_button("Update AI Knowledge")
        if submitted:
            # Re-initialize chat session with new configuration
            st.session_state.chat_session = None
            st.session_state.chat_history = []
            st.success("AI Knowledge Updated! Chat history cleared.")

    st.markdown("---")
    st.markdown("### 📊 Lead Management")
    if st.button("View Captured Leads"):
        st.session_state.view_leads = not st.session_state.get("view_leads", False)

# --- Main Area ---
st.markdown('''
<div class="orb orb-1"></div>
<div class="orb orb-2"></div>
<div class="hero-container">
    <svg class="hero-logo" width="80" height="80" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="neonGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#00D4FF" />
                <stop offset="50%" stop-color="#6C63FF" />
                <stop offset="100%" stop-color="#8B5CF6" />
            </linearGradient>
            <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
                <feGaussianBlur stdDeviation="4" result="blur" />
                <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>
        </defs>
        <path d="M42 20C42 15 36 12 32 12C26 12 22 16 22 22C22 30 42 32 42 42C42 48 38 52 32 52C26 52 22 48 22 42" stroke="url(#neonGrad)" stroke-width="6" stroke-linecap="round" filter="url(#glow)"/>
        <path d="M32 6L32 14" stroke="#00D4FF" stroke-width="4" stroke-linecap="round"/>
        <path d="M32 50L32 58" stroke="#8B5CF6" stroke-width="4" stroke-linecap="round"/>
    </svg>
    <div class="title-glow">Swift Reply</div>
    <div class="subtitle">AI Conversations, Reimagined.</div>
</div>
''', unsafe_allow_html=True)

# Admin: View Leads View
if st.session_state.get("view_leads", False):
    st.markdown("### 📇 Captured Leads")
    leads = database.get_all_leads()
    if leads:
        import pandas as pd
        df = pd.DataFrame(leads, columns=["ID", "Name", "Email", "Phone", "Timestamp", "Contact Method"])
        # Reorder to put Contact Method next to Phone, Timestamp at end
        df = df[["ID", "Name", "Email", "Phone", "Contact Method", "Timestamp"]]
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No leads captured yet.")
    st.markdown("---")

# Initialize Gemini Session
if st.session_state.chat_session is None:
    try:
        st.session_state.chat_session = ai_engine.create_chat_session(st.session_state.business_info)
        # Add an initial greeting message
        greeting = f"Hello! I am the AI assistant for {st.session_state.business_info['name']}. How can I help you today?"
        st.session_state.chat_history.append({"role": "assistant", "content": greeting})
    except Exception as e:
        st.error(f"Failed to initialize AI Engine: {str(e)}")

# --- Chat Interface ---
chat_container = st.container()

with chat_container:
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to history
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # Generate and Display AI Response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            if st.session_state.chat_session:
                response = ai_engine.generate_response(st.session_state.chat_session, prompt)
                st.markdown(response)
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                
                # Simple logic to trigger lead capture form (keyword based for MVP)
                lead_keywords = ["contact", "call", "email", "interested", "buy", "pricing quote", "more information"]
                if any(keyword in prompt.lower() for keyword in lead_keywords):
                    st.session_state.show_lead_form = True
            else:
                st.error("AI Engine not initialized. Please check API Key.")

# --- Lead Generation Form ---
if st.session_state.show_lead_form:
    st.markdown("---")
    st.markdown("### ✨ Let's Connect!")
    st.info("Would you like our team to get in touch with you? Please provide your details.")
    
    with st.form("lead_capture_form"):
        col1, col2 = st.columns(2)
        with col1:
            lead_name = st.text_input("Full Name")
            lead_phone = st.text_input("Phone Number")
        with col2:
            lead_email = st.text_input("Email Address")
            contact_method = st.selectbox(
                'How would you like to be contacted?',
                ('Email', 'Home phone', 'Mobile phone')
            )
            
        submit_lead = st.form_submit_button("Submit Details")
        
        if submit_lead:
            if lead_name and lead_email:
                database.save_lead(lead_name, lead_email, lead_phone, contact_method)
                st.success("Thank you! We have received your information and will contact you shortly.")
                st.session_state.show_lead_form = False
            else:
                st.warning("Please provide at least your Name and Email.")
