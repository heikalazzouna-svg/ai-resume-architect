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
    page_header("Success Stories", "See how we've helped others land their dream jobs")
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="bento-card">"The AI feedback was exactly what I needed. I landed interviews at top tech companies within weeks!"<br><br><b>- Sarah J., Software Engineer</b></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="bento-card">"The resume builder templates are clean and ATS-friendly. Highly recommended."<br><br><b>- Michael T., Product Manager</b></div>', unsafe_allow_html=True)
