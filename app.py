"""
Smart Resume AI - Main Application
"""
import time
from PIL import Image
from jobs.job_search import render_job_search
from datetime import datetime
from ui_components import (
    apply_modern_styles, hero_section, feature_card, about_section,
    page_header
)
from feedback.feedback import FeedbackManager
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt
from docx import Document
import io
import base64
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import requests
from dashboard.dashboard import DashboardManager
from config.courses import COURSES_BY_CATEGORY, RESUME_VIDEOS, INTERVIEW_VIDEOS, get_courses_for_role, get_category_for_role
from config.job_roles import JOB_ROLES
from config.database import (
    get_database_connection, save_resume_data, save_analysis_data,
    init_database, verify_admin, log_admin_action, save_ai_analysis_data,
    get_ai_analysis_stats, reset_ai_analysis_stats, get_detailed_ai_analysis_stats
)
from utils.ai_resume_analyzer import AIResumeAnalyzer
from utils.resume_builder import ResumeBuilder
from utils.resume_analyzer import ResumeAnalyzer
import traceback
import plotly.express as px
import pandas as pd
import json
import streamlit as st
from config.branding import APP_NAME, FOUNDER_NAME, FOUNDER_TITLE, FOUNDER_BIO, SOCIAL_LINKS
import datetime

# Set page config at the very beginning
st.set_page_config(
    page_title="Smart Resume AI",
    page_icon="🧾",
    layout="wide"
)



from app_pages import home, analyzer, builder, about, pricing, faq, testimonials, changelog, job_search, feedback_page, history

class ResumeApp:
    def __init__(self):
        """Initialize the application"""
        if 'form_data' not in st.session_state:
            st.session_state.form_data = {
                'personal_info': {
                    'full_name': '',
                    'email': '',
                    'phone': '',
                    'location': '',
                    'linkedin': '',
                    'portfolio': ''
                },
                'summary': '',
                'experiences': [],
                'education': [],
                'projects': [],
                'skills_categories': {
                    'technical': [],
                    'soft': [],
                    'languages': [],
                    'tools': []
                }
            }

        # Initialize navigation state
        if 'page' not in st.session_state:
            st.session_state.page = 'home'

        # Initialize admin state
        if 'is_admin' not in st.session_state:
            st.session_state.is_admin = False

        self.pages = {
            "Home": lambda: home.render(self),
            "Analyzer": lambda: analyzer.render(self),
            "Builder": lambda: builder.render(self),
            "Job Search": lambda: job_search.render(self),
            "Score History": lambda: history.render(self),
            "Pricing": lambda: pricing.render(self),
            "FAQ": lambda: faq.render(self),
            "Testimonials": lambda: testimonials.render(self),
            "Changelog": lambda: changelog.render(self),
            "Dashboard": self.render_dashboard,
            "Feedback": lambda: feedback_page.render(self),
            "About": lambda: about.render(self)
        }

        # Initialize dashboard manager
        self.dashboard_manager = DashboardManager()

        self.analyzer = ResumeAnalyzer()
        self.ai_analyzer = AIResumeAnalyzer()
        self.builder = ResumeBuilder()
        self.job_roles = JOB_ROLES

        # Initialize session state
        if 'user_id' not in st.session_state:
            st.session_state.user_id = 'default_user'
        if 'selected_role' not in st.session_state:
            st.session_state.selected_role = None

        # Initialize database
        init_database()

        # Load external CSS
        with open('style/style.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

        # Load Google Fonts and icon set for the redesigned UI
        st.markdown("""
            <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600;700&family=Fira+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
        """, unsafe_allow_html=True)

        if 'resume_data' not in st.session_state:
            st.session_state.resume_data = []
        if 'ai_analysis_stats' not in st.session_state:
            st.session_state.ai_analysis_stats = {
                'score_distribution': {},
                'total_analyses': 0,
                'average_score': 0
            }

    def load_lottie_url(self, url: str):
        """Load Lottie animation from URL"""
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    def apply_global_styles(self):
        """All styling is now handled by style/style.css — this method is intentionally minimal."""
        pass
        

        
    def add_footer(self):
        """Add a footer to all pages"""
        st.markdown("<hr style='margin-top: 50px; margin-bottom: 20px;'>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 3, 1])
        
        with col2:
            # GitHub star button with lottie animation
            st.markdown("""
            <div style='display: flex; justify-content: center; align-items: center; margin-bottom: 10px;'>
                
            </div>
            """, unsafe_allow_html=True)
            
            # Footer text
            st.markdown(f"""
            <div style="text-align: center; margin-top: 50px; padding-top: 20px; border-top: 1px solid var(--border-color);">
                <p>Powered by <b>Streamlit</b> and <b>Google Gemini AI</b> | Developed by <b>{FOUNDER_NAME}</b></p>
                <p>&#128274; <strong>Privacy First:</strong> Your resume data is secure, never sold, and only saved with explicit consent.</p>
            </div>
            """, unsafe_allow_html=True)

    def load_image(self, image_name):
        """Load image from static directory"""
        try:
            image_path = f"c:/Users/shree/Downloads/smart-resume-ai/{image_name}"
            with open(image_path, "rb") as f:
                image_bytes = f.read()
            encoded = base64.b64encode(image_bytes).decode()
            return f"data:image/png;base64,{encoded}"
        except Exception as e:
            print(f"Error loading image {image_name}: {e}")
            return None

    def export_to_excel(self):
        """Export resume data to Excel"""
        conn = get_database_connection()

        # Get resume data with analysis
        query = """
            SELECT
                rd.name, rd.email, rd.phone, rd.linkedin, rd.github, rd.portfolio,
                rd.summary, rd.target_role, rd.target_category,
                rd.education, rd.experience, rd.projects, rd.skills,
                ra.ats_score, ra.keyword_match_score, ra.format_score, ra.section_score,
                ra.missing_skills, ra.recommendations,
                rd.created_at
            FROM resume_data rd
            LEFT JOIN resume_analysis ra ON rd.id = ra.resume_id
        """

        try:
            # Read data into DataFrame
            df = pd.read_sql_query(query, conn)

            # Create Excel writer object
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Resume Data')

            return output.getvalue()
        except Exception as e:
            print(f"Error exporting to Excel: {str(e)}")
            return None
        finally:
            conn.close()

    def render_dashboard(self):
        """Render the dashboard page"""
        self.dashboard_manager.render_dashboard()



    def render_empty_state(self, icon, message):
        """Render an empty state with icon and message"""
        return f"""
            <div style='text-align: center; padding: 2rem; color: #666;'>
                <i class='{icon}' style='font-size: 2rem; margin-bottom: 1rem; color: #00bfa5;'></i>
                <p style='margin: 0;'>{message}</p>
            </div>
        """

    def analyze_resume(self, resume_text):
        """Analyze resume and store results"""
        analytics = self.analyzer.analyze_resume(resume_text)
        st.session_state.analytics_data = analytics
        return analytics

    def handle_resume_upload(self):
        """Handle resume upload and analysis"""
        uploaded_file = st.file_uploader(
            "Upload your resume", type=['pdf', 'docx'])

        if uploaded_file is not None:
            try:
                # Extract text from resume
                if uploaded_file.type == "application/pdf":
                    resume_text = extract_text_from_pdf(uploaded_file)
                else:
                    resume_text = extract_text_from_docx(uploaded_file)

                # Store resume data
                st.session_state.resume_data = {
                    'filename': uploaded_file.name,
                    'content': resume_text,
                    'upload_time': datetime.now().isoformat()
                }

                # Analyze resume
                analytics = self.analyze_resume(resume_text)

                return True
            except Exception as e:
                st.error(f"Error processing resume: {str(e)}")
                return False
        return False

    def main(self):
        """Main application entry point"""
        self.apply_global_styles()
        
        # Admin login/logout in sidebar
        with st.sidebar:
            # Sleek Compact Header
            st.html("""
            <div style="
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: var(--space-3) 0;
                margin-bottom: var(--space-6);
                border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            ">
                <div style="display: flex; align-items: center; gap: var(--space-3);">
                    <div style="display: flex; align-items: center; justify-content: center; width: 32px; height: 32px; border-radius: 8px; background: rgba(34, 211, 238, 0.1); border: 1px solid rgba(34, 211, 238, 0.2); box-shadow: 0 0 12px rgba(34,211,238,0.2);">
                        <i class="fas fa-bolt" style="color: #22d3ee; font-size: 14px;"></i>
                    </div>
                    <span style="font-weight: 700; font-size: var(--text-base); background: linear-gradient(90deg, #ffffff, #c7d2fe); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                        Smart Resume AI
                    </span>
                </div>
                <div style="padding: 2px 8px; font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; background: rgba(99, 102, 241, 0.1); color: #a5b4fc; border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 99px; box-shadow: 0 0 8px rgba(99,102,241,0.2);">
                    Pro
                </div>
            </div>
            """)
            
            # Navigation Groups
            nav_groups = {
                "MAIN": ["Home", "Dashboard", "Score History"],
                "TOOLS": ["Analyzer", "Builder", "Job Search"],
                "RESOURCES": ["Pricing", "FAQ", "Changelog", "Feedback", "About", "Testimonials"]
            }
            
            nav_icons = {
                "Home": "🏠", "Dashboard": "📊", "Score History": "🕰️",
                "Analyzer": "📄", "Builder": "✨", "Job Search": "🔍",
                "Pricing": "💳", "FAQ": "❓", "Testimonials": "💬",
                "Changelog": "📝", "Feedback": "📨", "About": "ℹ️"
            }
            
            # Helper to map page name to its internal state name
            def get_state_name(p_name):
                return p_name.lower().replace(" ", "_").strip()

            current_page = st.session_state.page

            # Render Grouped Navigation
            for group, items in nav_groups.items():
                st.html(f"""
                    <div style="
                        font-size: 11px;
                        font-weight: 600;
                        letter-spacing: 1.5px;
                        text-transform: uppercase;
                        color: var(--color-text-tertiary);
                        margin: var(--space-6) 0 var(--space-2) var(--space-2);
                    ">{group}</div>
                """)
                
                for page_name in items:
                    # Only render if the page exists in self.pages
                    if page_name in self.pages:
                        state_name = get_state_name(page_name)
                        is_active = (current_page == state_name)
                        btn_type = "primary" if is_active else "secondary"
                        icon = nav_icons.get(page_name, "▪")
                        
                        # We inject invisible tracking classes into the button via markdown isn't possible,
                        # but we can rely on Streamlit's primary/secondary types for styling.
                        if st.button(f"{icon} \u00A0 {page_name}", key=f"nav_{state_name}", use_container_width=True, type=btn_type):
                            st.session_state.page = state_name
                            st.rerun()

            # Modern Footer Section
            st.html("""
            <div style="
                margin-top: var(--space-4);
                padding-top: var(--space-4);
                border-top: 1px solid rgba(255, 255, 255, 0.05);
            "></div>
            """)
            if st.session_state.get('is_admin', False):
                st.html(f"""
                <div style="display: flex; align-items: center; gap: var(--space-3); padding: var(--space-2); margin-bottom: var(--space-3); background: rgba(255,255,255,0.02); border-radius: 8px;">
                    <div style="width: 32px; height: 32px; border-radius: 50%; background: var(--color-primary-subtle); display: flex; align-items: center; justify-content: center;">
                        <i class="fas fa-user-shield" style="color: var(--color-primary);"></i>
                    </div>
                    <div>
                        <div style="font-size: var(--text-sm); font-weight: 600; color: var(--color-text);">{st.session_state.get('current_admin_email').split('@')[0]}</div>
                        <div style="font-size: var(--text-xs); color: var(--color-text-tertiary);">Administrator</div>
                    </div>
                </div>
                """)
                if st.button("🚪 Logout", key="logout_button", use_container_width=True):
                    try:
                        log_admin_action(st.session_state.get('current_admin_email'), "logout")
                        st.session_state.is_admin = False
                        st.session_state.current_admin_email = None
                        st.success("Logged out successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error during logout: {str(e)}")
            else:
                with st.expander("👤 Admin Access"):
                    admin_email_input = st.text_input("Email", key="admin_email_input")
                    admin_password = st.text_input("Password", type="password", key="admin_password_input")
                    if st.button("Secure Login", key="login_button", use_container_width=True, type="primary"):
                            try:
                                if verify_admin(admin_email_input, admin_password):
                                    st.session_state.is_admin = True
                                    st.session_state.current_admin_email = admin_email_input
                                    log_admin_action(admin_email_input, "login")
                                    st.success("Login successful!")
                                    st.rerun()
                                else:
                                    st.error("Invalid credentials")
                            except Exception as e:
                                st.error(f"Login error: {str(e)}")
        
            # Display the repository notification in the sidebar

        # Force home page on first load
        if 'initial_load' not in st.session_state:
            st.session_state.initial_load = True
            st.session_state.page = 'home'
            st.rerun()
        
        # Get current page and render it
        current_page = st.session_state.get('page', 'home')
        
        # Create a mapping of cleaned page names to original names
        page_mapping = {name.lower().replace(" ", "_").replace("🏠", "").replace("🔍", "").replace("📝", "").replace("📊", "").replace("🎯", "").replace("💬", "").replace("ℹ️", "").strip(): name 
                       for name in self.pages.keys()}
        
        # Render the appropriate page
        if current_page in page_mapping:
            self.pages[page_mapping[current_page]]()
        else:
            # Default to home page if invalid page
            self.render_home()
    
        # Add footer to every page
        self.add_footer()

if __name__ == "__main__":
    app = ResumeApp()
    app.main()