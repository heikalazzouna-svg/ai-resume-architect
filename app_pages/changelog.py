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
    page_header("Changelog", "Latest updates and improvements")
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### v1.1.0 - Identity & Polish")
    st.markdown("- Unified design tokens to premium cyan/indigo")
    st.markdown("- Added Pricing, FAQ, and Testimonial pages")
    st.markdown("- Improved Resume Builder UX")
    st.markdown("### v1.0.0 - Initial Release")
    st.markdown("- Basic Resume Analysis")
    st.markdown("- Resume Builder")
