import streamlit as st
import pandas as pd
import json
import base64
from datetime import datetime
import io
import time
import traceback
from PIL import Image

from ui_components import hero_section, page_header, apply_modern_styles, feature_card
from config.branding import APP_NAME, FOUNDER_NAME, SOCIAL_LINKS, FOUNDER_TITLE, FOUNDER_BIO
from config.courses import COURSES_BY_CATEGORY, RESUME_VIDEOS, INTERVIEW_VIDEOS
from config.job_roles import JOB_ROLES
from config.database import save_resume_data, save_analysis_data
from utils.resume_parser import ResumeParser

def render(app):
    # Hero Section (which we just rewrote in ui_components to be awesome)
    hero_section(
        "Resume intelligence, drawn like a dossier.",
        "Scan, tune, and ship a resume that reads cleanly to people and ATS systems alike.",
        "Smart Resume AI looks at structure, keywords, and signal strength together, then turns each upload into a clear next action instead of a vague score."
    )
    
    # Trust Strip
    st.html("""
        <div class="trust-strip animate-fade-in animate-delay-4">
            <div class="trust-strip__item"><i class="fas fa-check-circle"></i> ATS-Optimized</div>
            <div class="trust-strip__item"><i class="fas fa-lock"></i> Privacy First</div>
            <div class="trust-strip__item"><i class="fas fa-bolt"></i> Instant Feedback</div>
            <div class="trust-strip__item"><i class="fas fa-chart-bar"></i> Data Driven</div>
        </div>
    """)
    
    # Features Section
    st.html('<div class="feature-grid animate-fade-up animate-delay-2" style="margin-top: var(--space-8);">')
    
    feature_card(
        "fas fa-robot",
        "Signal detection",
        "Get instant feedback that highlights what a recruiter will notice first: clarity, relevance, and the places where the story breaks."
    )
    
    feature_card(
        "fas fa-magic",
        "Structure builder",
        "Create a cleaner resume layout with guided formatting, content prompts, and a flow that keeps the document easy to scan."
    )
    
    feature_card(
        "fas fa-chart-line",
        "Career signal map",
        "Track which skills, roles, and presentation choices are working so you can tune the next version with less guesswork."
    )
    
    st.html('</div>')
    
    # Call-to-Action with Streamlit navigation
    st.html('<div class="flex-center animate-fade-in" style="margin-top: var(--space-8); margin-bottom: var(--space-12);">')
    st.html('<div class="cta-accent">')
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Open the analyzer", key="get_started_btn", 
                    help="Click to start analyzing your resume",
                    type="primary",
                    use_container_width=True):
            cleaned_name = "🔍 RESUME ANALYZER".lower().replace(" ", "_").replace("🔍", "").strip()
            st.session_state.page = cleaned_name
            st.rerun()
    st.html('</div></div>')
