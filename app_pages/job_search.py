import streamlit as st
from jobs.job_search import render_job_search
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
    """Render the job search page"""
    render_job_search()
