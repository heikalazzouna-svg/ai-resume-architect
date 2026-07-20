import streamlit as st
from feedback.feedback import FeedbackManager
import pandas as pd
import json
import base64
from datetime import datetime
import io
import time
import traceback
from PIL import Image

from ui_components import hero_section, page_header, apply_modern_styles
from config.branding import APP_NAME, FOUNDER_NAME, SOCIAL_LINKS, FOUNDER_TITLE, FOUNDER_BIO
from config.courses import COURSES_BY_CATEGORY, RESUME_VIDEOS, INTERVIEW_VIDEOS
from config.job_roles import JOB_ROLES
from config.database import save_resume_data, save_analysis_data
from utils.resume_parser import ResumeParser

def render(app):
    """Render the feedback page"""
    apply_modern_styles()
    
    # Page Header
    page_header(
        "Feedback & Suggestions",
        "Help us improve by sharing your thoughts"
    )
    
    # Initialize feedback manager
    feedback_manager = FeedbackManager()
    
    # Create tabs for form and stats
    form_tab, stats_tab = st.tabs(["Submit Feedback", "Feedback Stats"])
    
    with form_tab:
        feedback_manager.render_feedback_form()
        
    with stats_tab:
        feedback_manager.render_feedback_stats()
