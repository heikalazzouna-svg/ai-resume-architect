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
    page_header("Simple, Transparent Pricing", "Choose the plan that fits your career goals")
    st.html('<div style="margin-bottom: var(--space-8);"></div>')
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.html("""
            <div class="card animate-fade-up">
                <div class="section-kicker">Basic</div>
                <div style="font-size: var(--text-5xl); font-weight: 700; margin-bottom: var(--space-2); color: var(--color-text);">Free</div>
                <p style="color: var(--color-text-secondary); margin-bottom: var(--space-6);">For getting started</p>
                <ul style="list-style: none; padding: 0; margin: 0 0 var(--space-8) 0; display: flex; flex-direction: column; gap: var(--space-3);">
                    <li style="display: flex; gap: var(--space-2);"><i class="fas fa-check" style="color: var(--color-success); margin-top: 4px;"></i> <span>Basic Resume Analysis</span></li>
                    <li style="display: flex; gap: var(--space-2);"><i class="fas fa-check" style="color: var(--color-success); margin-top: 4px;"></i> <span>1 Template</span></li>
                    <li style="display: flex; gap: var(--space-2);"><i class="fas fa-check" style="color: var(--color-success); margin-top: 4px;"></i> <span>Community Support</span></li>
                </ul>
            </div>
        """)
        st.button("Current Plan", key="plan_free", use_container_width=True, disabled=True)
        
    with col2:
        st.html("""
            <div class="card card--accent animate-fade-up animate-delay-1" style="transform: scale(1.02); box-shadow: var(--shadow-md);">
                <div class="flex-between" style="margin-bottom: var(--space-2);">
                    <div class="section-kicker" style="margin: 0;">Pro</div>
                    <span class="tag tag--accent">Most Popular</span>
                </div>
                <div style="font-size: var(--text-5xl); font-weight: 700; margin-bottom: var(--space-2); color: var(--color-text);">$9<span style="font-size: var(--text-base); color: var(--color-text-tertiary); font-weight: 400;">/mo</span></div>
                <p style="color: var(--color-text-secondary); margin-bottom: var(--space-6);">For active job seekers</p>
                <ul style="list-style: none; padding: 0; margin: 0 0 var(--space-8) 0; display: flex; flex-direction: column; gap: var(--space-3);">
                    <li style="display: flex; gap: var(--space-2);"><i class="fas fa-check" style="color: var(--color-success); margin-top: 4px;"></i> <span>AI Resume Analysis</span></li>
                    <li style="display: flex; gap: var(--space-2);"><i class="fas fa-check" style="color: var(--color-success); margin-top: 4px;"></i> <span>All Templates</span></li>
                    <li style="display: flex; gap: var(--space-2);"><i class="fas fa-check" style="color: var(--color-success); margin-top: 4px;"></i> <span>Cover Letter Gen</span></li>
                    <li style="display: flex; gap: var(--space-2);"><i class="fas fa-check" style="color: var(--color-success); margin-top: 4px;"></i> <span>Priority Support</span></li>
                </ul>
            </div>
        """)
        st.html('<div class="cta-accent">')
        st.button("Upgrade to Pro", key="plan_pro", type="primary", use_container_width=True)
        st.html('</div>')
        
    with col3:
        st.html("""
            <div class="card animate-fade-up animate-delay-2">
                <div class="section-kicker">Elite</div>
                <div style="font-size: var(--text-5xl); font-weight: 700; margin-bottom: var(--space-2); color: var(--color-text);">$29<span style="font-size: var(--text-base); color: var(--color-text-tertiary); font-weight: 400;">/mo</span></div>
                <p style="color: var(--color-text-secondary); margin-bottom: var(--space-6);">For career acceleration</p>
                <ul style="list-style: none; padding: 0; margin: 0 0 var(--space-8) 0; display: flex; flex-direction: column; gap: var(--space-3);">
                    <li style="display: flex; gap: var(--space-2);"><i class="fas fa-check" style="color: var(--color-success); margin-top: 4px;"></i> <span>Everything in Pro</span></li>
                    <li style="display: flex; gap: var(--space-2);"><i class="fas fa-check" style="color: var(--color-success); margin-top: 4px;"></i> <span>Mock Interviews</span></li>
                    <li style="display: flex; gap: var(--space-2);"><i class="fas fa-check" style="color: var(--color-success); margin-top: 4px;"></i> <span>1-on-1 Coaching</span></li>
                </ul>
            </div>
        """)
        st.button("Contact Us", key="plan_elite", use_container_width=True)
