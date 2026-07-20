import streamlit as st
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
    page_header("Frequently Asked Questions", "Find answers to common questions")
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("How does the AI Resume Analyzer work?"):
        st.write("Our AI analyzes your resume against industry standards and specific job descriptions to provide a match score and actionable feedback.")
    with st.expander("Is my data secure?"):
        st.write("Yes. We use industry-standard encryption and only store your data if you explicitly opt-in.")
    with st.expander("Can I export my resume to PDF?"):
        st.write("PDF export is currently in development and will be available to all Pro users soon.")
