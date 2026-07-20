import streamlit as st
from ui_components import apply_modern_styles
import pandas as pd
import json
import base64
from datetime import datetime
import io
import time
import traceback
from PIL import Image

from ui_components import hero_section, page_header
from config.branding import APP_NAME, FOUNDER_NAME, SOCIAL_LINKS, FOUNDER_TITLE, FOUNDER_BIO
from config.courses import COURSES_BY_CATEGORY, RESUME_VIDEOS, INTERVIEW_VIDEOS
from config.job_roles import JOB_ROLES
from config.database import save_resume_data, save_analysis_data
from utils.resume_parser import ResumeParser

def render(app):
    """Render the about page"""
    # Apply modern styles
    import base64
    import os

    # Function to load image as base64
    def get_image_as_base64(file_path):
        try:
            with open(file_path, "rb") as image_file:
                encoded = base64.b64encode(image_file.read()).decode()
                return f"data:image/jpeg;base64,{encoded}"
        except:
            return None

    # Get image path and convert to base64
    image_path = os.path.join(
os.path.dirname(__file__),
"..",
 "assets",
 "heikal.png")
    image_base64 = get_image_as_base64(image_path)

    page_header("About Smart Resume AI", "A powerful AI-driven platform for optimizing your resume")

    st.html(f"""
        <div class="profile-section animate-fade-up">
            <img src="{image_base64 if image_base64 else ''}" alt="{FOUNDER_NAME}" class="profile-image">
            <h2 class="profile-name">{FOUNDER_NAME}</h2>
            <p class="profile-title">{FOUNDER_TITLE}</p>
            <p style="text-align: center; color: var(--color-text-secondary); max-width: 600px; margin: var(--space-3) auto;">{FOUNDER_BIO}</p>
            <div class="social-links">
                <a href="{SOCIAL_LINKS.get('linkedin', '#')}" class="social-link" target="_blank" title="LinkedIn">
                    <i class="fab fa-linkedin"></i>
                </a>
                <a href="{SOCIAL_LINKS.get('github', '#')}" class="social-link" target="_blank" title="GitHub">
                    <i class="fab fa-github"></i>
                </a>
            </div>
            <p class="bio-text">
                Hello! I'm a passionate Full Stack Developer with expertise in AI and Machine Learning.
                I created Smart Resume AI to revolutionize how job seekers approach their career journey.
                With my background in both software development and AI, I've designed this platform to
                provide intelligent, data-driven insights for resume optimization.
            </p>
        </div>
    """)

    st.html("""
        <div class="card card--accent animate-fade-up animate-delay-1" style="max-width: 800px; margin: var(--space-8) auto; text-align: center; padding: var(--space-8);">
            <i class="fas fa-lightbulb" style="font-size: var(--text-4xl); color: var(--color-accent); margin-bottom: var(--space-4);"></i>
            <h2 style="margin-bottom: var(--space-4);">Our Vision</h2>
            <p style="color: var(--color-text-secondary); line-height: var(--leading-loose); font-size: var(--text-lg); font-style: italic;">
                "Smart Resume AI represents my vision of democratizing career advancement through technology.
                By combining cutting-edge AI with intuitive design, this platform empowers job seekers at
                every career stage to showcase their true potential and stand out in today's competitive job market."
            </p>
        </div>
    """)

    st.html('<div class="feature-grid animate-fade-up animate-delay-2" style="max-width: 1200px; margin: 0 auto;">')
    
    # Feature 1
    st.html("""
        <div class="feature-card">
            <div class="feature-card__icon"><i class="fas fa-robot"></i></div>
            <h3 class="feature-card__title">AI-Powered Analysis</h3>
            <p class="feature-card__desc">Advanced AI algorithms provide detailed insights and suggestions to optimize your resume for maximum impact.</p>
        </div>
    """)
    
    # Feature 2
    st.html("""
        <div class="feature-card">
            <div class="feature-card__icon"><i class="fas fa-chart-line"></i></div>
            <h3 class="feature-card__title">Data-Driven Insights</h3>
            <p class="feature-card__desc">Make informed decisions with our analytics-based recommendations and industry insights.</p>
        </div>
    """)
    
    # Feature 3
    st.html("""
        <div class="feature-card">
            <div class="feature-card__icon"><i class="fas fa-shield-alt"></i></div>
            <h3 class="feature-card__title">Privacy First</h3>
            <p class="feature-card__desc">Your data security is our priority. We ensure your information is always protected and private.</p>
        </div>
    """)
    st.html('</div>')

    st.html("""
        <div class="flex-center animate-fade-in animate-delay-3" style="margin: var(--space-12) 0;">
            <div class="cta-accent">
                <!-- Using Streamlit navigation mechanism instead of raw HTML link -->
            </div>
        </div>
    """)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.html('<div class="cta-accent">')
        if st.button("Start Your Journey", key="about_start_btn", use_container_width=True):
            cleaned_name = "🔍 RESUME ANALYZER".lower().replace(" ", "_").replace("🔍", "").strip()
            st.session_state.page = cleaned_name
            st.rerun()
        st.html('</div>')
