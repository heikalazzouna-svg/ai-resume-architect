import streamlit as st
import pandas as pd
import json
import base64
from datetime import datetime
import io
import time
import traceback
from PIL import Image

from ui_components import hero_section, page_header, apply_modern_styles, section_divider, alert
from config.branding import APP_NAME, FOUNDER_NAME, SOCIAL_LINKS, FOUNDER_TITLE, FOUNDER_BIO
from config.courses import COURSES_BY_CATEGORY, RESUME_VIDEOS, INTERVIEW_VIDEOS
from config.job_roles import JOB_ROLES
from config.database import save_resume_data, save_analysis_data
from utils.resume_parser import ResumeParser

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER


def create_pdf_resume(resume_data):
    """Generate a professional PDF resume from structured resume_data dict."""
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                            leftMargin=2 * cm, rightMargin=2 * cm,
                            topMargin=1.5 * cm, bottomMargin=1.5 * cm)

    styles = getSampleStyleSheet()
    accent = HexColor("#06b6d4")

    # Custom styles
    styles.add(ParagraphStyle("ResName", parent=styles["Title"],
                              fontSize=22, leading=26, textColor=HexColor("#1e293b"),
                              alignment=TA_CENTER, spaceAfter=4))
    styles.add(ParagraphStyle("ResContact", parent=styles["Normal"],
                              fontSize=10, leading=13, textColor=HexColor("#64748b"),
                              alignment=TA_CENTER, spaceAfter=10))
    styles.add(ParagraphStyle("SectionHead", parent=styles["Heading2"],
                              fontSize=13, leading=16, textColor=accent,
                              spaceBefore=14, spaceAfter=6,
                              borderWidth=0))
    styles.add(ParagraphStyle("Body", parent=styles["Normal"],
                              fontSize=10, leading=14, textColor=HexColor("#334155")))
    styles.add(ParagraphStyle("BulletItem", parent=styles["Normal"],
                              fontSize=10, leading=14, textColor=HexColor("#334155"),
                              leftIndent=12, bulletIndent=0))

    story = []
    pi = resume_data.get("personal_info", {})

    # --- Header ---
    story.append(Paragraph(pi.get("full_name", "Your Name"), styles["ResName"]))
    contact_parts = [p for p in [
        pi.get("email"), pi.get("phone"),
        pi.get("linkedin"), pi.get("github"), pi.get("portfolio")
    ] if p]
    if contact_parts:
        story.append(Paragraph(" | ".join(contact_parts), styles["ResContact"]))
    story.append(HRFlowable(width="100%", thickness=1, color=accent, spaceAfter=10))

    # --- Summary ---
    summary = resume_data.get("summary", "")
    if summary:
        story.append(Paragraph("PROFESSIONAL SUMMARY", styles["SectionHead"]))
        story.append(Paragraph(summary, styles["Body"]))

    # --- Experience ---
    experience = resume_data.get("experience", [])
    if isinstance(experience, str):
        try:
            experience = eval(experience)
        except Exception:
            experience = []
    if experience:
        story.append(Paragraph("EXPERIENCE", styles["SectionHead"]))
        for exp in experience:
            if isinstance(exp, dict):
                title_line = f"<b>{exp.get('title', '')}</b> at {exp.get('company', '')}  ({exp.get('duration', '')})"
                story.append(Paragraph(title_line, styles["Body"]))
                desc = exp.get("description", "")
                if desc:
                    for line in desc.split("\n"):
                        if line.strip():
                            story.append(Paragraph(f"&bull; {line.strip()}", styles["BulletItem"]))
                story.append(Spacer(1, 6))

    # --- Education ---
    education = resume_data.get("education", [])
    if isinstance(education, str):
        try:
            education = eval(education)
        except Exception:
            education = []
    if education:
        story.append(Paragraph("EDUCATION", styles["SectionHead"]))
        for edu in education:
            if isinstance(edu, dict):
                edu_line = f"<b>{edu.get('degree', '')}</b> - {edu.get('school', '')}  ({edu.get('year', '')})"
                story.append(Paragraph(edu_line, styles["Body"]))
                story.append(Spacer(1, 4))

    # --- Skills ---
    skills = resume_data.get("skills", [])
    if isinstance(skills, str):
        try:
            skills = eval(skills)
        except Exception:
            skills = []
    if skills:
        story.append(Paragraph("SKILLS", styles["SectionHead"]))
        skills_text = ", ".join(str(s) for s in skills)
        story.append(Paragraph(skills_text, styles["Body"]))

    # --- Projects ---
    projects = resume_data.get("projects", [])
    if isinstance(projects, str):
        try:
            projects = eval(projects)
        except Exception:
            projects = []
    if projects:
        story.append(Paragraph("PROJECTS", styles["SectionHead"]))
        for proj in projects:
            if isinstance(proj, dict):
                proj_line = f"<b>{proj.get('name', '')}</b>"
                story.append(Paragraph(proj_line, styles["Body"]))
                desc = proj.get("description", "")
                if desc:
                    story.append(Paragraph(desc, styles["BulletItem"]))
                story.append(Spacer(1, 4))

    doc.build(story)
    buf.seek(0)
    return buf


def render(app):
    page_header("Resume Builder", "Create an ATS-friendly resume in minutes")

    # Template selection
    template_options = ["Modern", "Professional", "Minimal", "Creative"]
    selected_template = st.selectbox("Select Resume Template", template_options)
    
    st.html(f'<div class="card card--success" style="padding: var(--space-3); margin-top: var(--space-2);"><i class="fas fa-palette" style="color: var(--color-success); margin-right: 8px;"></i> Currently using: <span style="font-weight: 600;">{selected_template} Template</span></div>')

    # Personal Information
    section_divider("Personal Information")

    col1, col2 = st.columns(2)
    with col1:
        # Get existing values from session state
        existing_name = st.session_state.form_data['personal_info']['full_name']
        existing_email = st.session_state.form_data['personal_info']['email']
        existing_phone = st.session_state.form_data['personal_info']['phone']

        # Input fields with existing values
        full_name = st.text_input("Full Name", value=existing_name)
        email = st.text_input(
"Email",
value=existing_email,
 key="email_input")
        phone = st.text_input("Phone", value=existing_phone)

        # Immediately update session state after email input
        if 'email_input' in st.session_state:
            st.session_state.form_data['personal_info']['email'] = st.session_state.email_input

    with col2:
        # Get existing values from session state
        existing_location = st.session_state.form_data['personal_info']['location']
        existing_linkedin = st.session_state.form_data['personal_info']['linkedin']
        existing_portfolio = st.session_state.form_data['personal_info']['portfolio']

        # Input fields with existing values
        location = st.text_input("Location", value=existing_location)
        linkedin = st.text_input("LinkedIn URL", value=existing_linkedin)
        portfolio = st.text_input(
"Portfolio Website", value=existing_portfolio)

    # Update personal info in session state
    st.session_state.form_data['personal_info'] = {
        'full_name': full_name,
        'email': email,
        'phone': phone,
        'location': location,
        'linkedin': linkedin,
        'portfolio': portfolio
    }

    # Professional Summary
    section_divider("Professional Summary")
    summary = st.text_area("Professional Summary", value=st.session_state.form_data.get('summary', ''), height=150,
                         help="Write a brief summary highlighting your key skills and experience")

    # Experience Section
    section_divider("Work Experience")
    if 'experiences' not in st.session_state.form_data:
        st.session_state.form_data['experiences'] = []

    if st.button("Add Experience"):
        st.session_state.form_data['experiences'].append({
            'company': '',
            'position': '',
            'start_date': '',
            'end_date': '',
            'description': '',
            'responsibilities': [],
            'achievements': []
        })

    for idx, exp in enumerate(st.session_state.form_data['experiences']):
        with st.expander(f"Experience {idx + 1}", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                exp['company'] = st.text_input(
"Company Name",
key=f"company_{idx}",
value=exp.get(
    'company',
     ''))
                exp['position'] = st.text_input(
"Position", key=f"position_{idx}", value=exp.get(
    'position', ''))
            with col2:
                exp['start_date'] = st.text_input(
"Start Date", key=f"start_date_{idx}", value=exp.get(
    'start_date', ''))
                exp['end_date'] = st.text_input(
"End Date", key=f"end_date_{idx}", value=exp.get(
    'end_date', ''))

            exp['description'] = st.text_area("Role Overview", key=f"desc_{idx}",
                                            value=exp.get(
                                                'description', ''),
                                            help="Brief overview of your role and impact")

            # Responsibilities
            st.markdown("##### Key Responsibilities")
            resp_text = st.text_area("Enter responsibilities (one per line)",
                                   key=f"resp_{idx}",
                                   value='\n'.join(
                                       exp.get('responsibilities', [])),
                                   height=100,
                                   help="List your main responsibilities, one per line")
            exp['responsibilities'] = [r.strip()
                                               for r in resp_text.split('\n') if r.strip()]

            # Achievements
            st.markdown("##### Key Achievements")
            achv_text = st.text_area("Enter achievements (one per line)",
                                   key=f"achv_{idx}",
                                   value='\n'.join(
                                       exp.get('achievements', [])),
                                   height=100,
                                   help="List your notable achievements, one per line")
            exp['achievements'] = [a.strip()
                                           for a in achv_text.split('\n') if a.strip()]

            if st.button("Remove Experience", key=f"remove_exp_{idx}"):
                st.session_state.form_data['experiences'].pop(idx)
                st.rerun()

    # Projects Section
    section_divider("Projects")
    if 'projects' not in st.session_state.form_data:
        st.session_state.form_data['projects'] = []

    if st.button("Add Project"):
        st.session_state.form_data['projects'].append({
            'name': '',
            'technologies': '',
            'description': '',
            'responsibilities': [],
            'achievements': [],
            'link': ''
        })

    for idx, proj in enumerate(st.session_state.form_data['projects']):
        with st.expander(f"Project {idx + 1}", expanded=True):
            proj['name'] = st.text_input(
"Project Name",
key=f"proj_name_{idx}",
value=proj.get(
    'name',
     ''))
            proj['technologies'] = st.text_input("Technologies Used", key=f"proj_tech_{idx}",
                                               value=proj.get(
                                                   'technologies', ''),
                                               help="List the main technologies, frameworks, and tools used")

            proj['description'] = st.text_area("Project Overview", key=f"proj_desc_{idx}",
                                             value=proj.get(
                                                 'description', ''),
                                             help="Brief overview of the project and its goals")

            # Project Responsibilities
            st.markdown("##### Key Responsibilities")
            proj_resp_text = st.text_area("Enter responsibilities (one per line)",
                                        key=f"proj_resp_{idx}",
                                        value='\n'.join(
                                            proj.get('responsibilities', [])),
                                        height=100,
                                        help="List your main responsibilities in the project")
            proj['responsibilities'] = [r.strip()
                                                for r in proj_resp_text.split('\n') if r.strip()]

            # Project Achievements
            st.markdown("##### Key Achievements")
            proj_achv_text = st.text_area("Enter achievements (one per line)",
                                        key=f"proj_achv_{idx}",
                                        value='\n'.join(
                                            proj.get('achievements', [])),
                                        height=100,
                                        help="List the project's key achievements and your contributions")
            proj['achievements'] = [a.strip()
                                            for a in proj_achv_text.split('\n') if a.strip()]

            proj['link'] = st.text_input("Project Link (optional)", key=f"proj_link_{idx}",
                                       value=proj.get('link', ''),
                                       help="Link to the project repository, demo, or documentation")

            if st.button("Remove Project", key=f"remove_proj_{idx}"):
                st.session_state.form_data['projects'].pop(idx)
                st.rerun()

    # Education Section
    section_divider("Education")
    if 'education' not in st.session_state.form_data:
        st.session_state.form_data['education'] = []

    if st.button("Add Education"):
        st.session_state.form_data['education'].append({
            'school': '',
            'degree': '',
            'field': '',
            'graduation_date': '',
            'gpa': '',
            'achievements': []
        })

    for idx, edu in enumerate(st.session_state.form_data['education']):
        with st.expander(f"Education {idx + 1}", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                edu['school'] = st.text_input(
"School/University",
key=f"school_{idx}",
value=edu.get(
    'school',
     ''))
                edu['degree'] = st.text_input(
"Degree", key=f"degree_{idx}", value=edu.get(
    'degree', ''))
            with col2:
                edu['field'] = st.text_input(
"Field of Study",
key=f"field_{idx}",
value=edu.get(
    'field',
     ''))
                edu['graduation_date'] = st.text_input("Graduation Date", key=f"grad_date_{idx}",
                                                     value=edu.get('graduation_date', ''))

            edu['gpa'] = st.text_input(
"GPA (optional)",
key=f"gpa_{idx}",
value=edu.get(
    'gpa',
     ''))

            # Educational Achievements
            st.markdown("##### Achievements & Activities")
            edu_achv_text = st.text_area("Enter achievements (one per line)",
                                       key=f"edu_achv_{idx}",
                                       value='\n'.join(
                                           edu.get('achievements', [])),
                                       height=100,
                                       help="List academic achievements, relevant coursework, or activities")
            edu['achievements'] = [a.strip()
                                           for a in edu_achv_text.split('\n') if a.strip()]

            if st.button("Remove Education", key=f"remove_edu_{idx}"):
                st.session_state.form_data['education'].pop(idx)
                st.rerun()

    # Skills Section
    section_divider("Skills")
    if 'skills_categories' not in st.session_state.form_data:
        st.session_state.form_data['skills_categories'] = {
            'technical': [],
            'soft': [],
            'languages': [],
            'tools': []
        }

    col1, col2 = st.columns(2)
    with col1:
        tech_skills = st.text_area("Technical Skills (one per line)",
                                 value='\n'.join(
st.session_state.form_data['skills_categories']['technical']),
                                 height=150,
                                 help="Programming languages, frameworks, databases, etc.")
        st.session_state.form_data['skills_categories']['technical'] = [
            s.strip() for s in tech_skills.split('\n') if s.strip()]

        soft_skills = st.text_area("Soft Skills (one per line)",
                                 value='\n'.join(
st.session_state.form_data['skills_categories']['soft']),
                                 height=150,
                                 help="Leadership, communication, problem-solving, etc.")
        st.session_state.form_data['skills_categories']['soft'] = [
            s.strip() for s in soft_skills.split('\n') if s.strip()]

    with col2:
        languages = st.text_area("Languages (one per line)",
                               value='\n'.join(
st.session_state.form_data['skills_categories']['languages']),
                               height=150,
                               help="Programming or human languages with proficiency level")
        st.session_state.form_data['skills_categories']['languages'] = [
            l.strip() for l in languages.split('\n') if l.strip()]

        tools = st.text_area("Tools & Technologies (one per line)",
                           value='\n'.join(
st.session_state.form_data['skills_categories']['tools']),
                           height=150,
                           help="Development tools, software, platforms, etc.")
        st.session_state.form_data['skills_categories']['tools'] = [
            t.strip() for t in tools.split('\n') if t.strip()]

    # Update form data in session state
    st.session_state.form_data.update({
        'summary': summary
    })

    # Generate Resume button
    if st.button("Generate Resume 📄", type="primary"):
        print("Validating form data...")
        print(f"Session state form data: {st.session_state.form_data}")
        print(f"Email input value: {st.session_state.get('email_input', '')}")

        # Get the current values from form
        current_name = st.session_state.form_data['personal_info']['full_name'].strip(
        )
        current_email = st.session_state.email_input if 'email_input' in st.session_state else ''

        print(f"Current name: {current_name}")
        print(f"Current email: {current_email}")

        # Validate required fields
        if not current_name:
            st.error("⚠️ Please enter your full name.")
            return

        if not current_email:
            st.error("⚠️ Please enter your email address.")
            return

        # Update email in form data one final time
        st.session_state.form_data['personal_info']['email'] = current_email

        try:
            print("Preparing resume data...")
            # Prepare resume data with current form values
            resume_data = {
                "personal_info": st.session_state.form_data['personal_info'],
                "summary": st.session_state.form_data.get('summary', '').strip(),
                "experience": st.session_state.form_data.get('experiences', []),
                "education": st.session_state.form_data.get('education', []),
                "projects": st.session_state.form_data.get('projects', []),
                "skills": st.session_state.form_data.get('skills_categories', {
                    'technical': [],
                    'soft': [],
                    'languages': [],
                    'tools': []
                }),
                "template": selected_template
            }

            print(f"Resume data prepared: {resume_data}")

            try:
                # Generate resume
                resume_buffer = app.builder.generate_resume(resume_data)
                if resume_buffer:
                    try:
                        # Save resume data to database
                        if save_builder_consent:
                            save_resume_data(resume_data)

                        # Offer the resume for download
                        st.success("Resume generated successfully!")

                        # Show snowflake effect
                        st.snow()

                        dl_col1, dl_col2 = st.columns(2)
                        with dl_col1:
                            st.download_button(
                                label="Download DOCX",
                                data=resume_buffer,
                                file_name=f"{current_name.replace(' ', '_')}_resume.docx",
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                on_click=lambda: st.balloons()
                            )
                        with dl_col2:
                            try:
                                pdf_buffer = create_pdf_resume(resume_data)
                                st.download_button(
                                    label="Download PDF",
                                    data=pdf_buffer,
                                    file_name=f"{current_name.replace(' ', '_')}_resume.pdf",
                                    mime="application/pdf",
                                    on_click=lambda: st.balloons()
                                )
                            except Exception as pdf_err:
                                st.warning(f"PDF generation failed: {pdf_err}")
                    except Exception as db_error:
                        print(f"Warning: Failed to save to database: {str(db_error)}")
                        # Still allow download even if database save fails
                        st.warning(
                            "⚠️ Resume generated but couldn't be saved to database")
                        
                        # Show balloons effect
                        st.balloons()

                        st.download_button(
                            label="Download Resume 📥",
                            data=resume_buffer,
                            file_name=f"{current_name.replace(' ', '_')}_resume.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            on_click=lambda: st.balloons()
                        )
                else:
                    st.error(
                        "❌ Failed to generate resume. Please try again.")
                    print("Resume buffer was None")
            except Exception as gen_error:
                print(f"Error during resume generation: {str(gen_error)}")
                print(f"Full traceback: {traceback.format_exc()}")
                st.error(f"❌ Error generating resume: {str(gen_error)}")

        except Exception as e:
            print(f"Error preparing resume data: {str(e)}")
            print(f"Full traceback: {traceback.format_exc()}")
            st.error(f"❌ Error preparing resume data: {str(e)}")
