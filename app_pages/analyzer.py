import streamlit as st
import pandas as pd
import json
import base64
from datetime import datetime
import io
import time
import traceback
from PIL import Image

from ui_components import hero_section, page_header, apply_modern_styles, score_ring, metric_card, alert, section_divider
from config.branding import APP_NAME, FOUNDER_NAME, SOCIAL_LINKS, FOUNDER_TITLE, FOUNDER_BIO
from config.courses import COURSES_BY_CATEGORY, RESUME_VIDEOS, INTERVIEW_VIDEOS
from config.job_roles import JOB_ROLES
from config.database import save_resume_data, save_analysis_data, save_ai_analysis_data
from utils.resume_parser import ResumeParser
from utils.ai_resume_analyzer import AIResumeAnalyzer

def render(app):
    """Render the resume analyzer page"""
    apply_modern_styles()

    # Page Header
    page_header(
        "Resume Analyzer",
        "Get instant AI-powered feedback to optimize your resume"
    )

    # Create tabs for Normal Analyzer and AI Analyzer
    analyzer_tabs = st.tabs(["Standard Analyzer", "AI Analyzer"])

    with analyzer_tabs[0]:
        # Job Role Selection
        categories = list(app.job_roles.keys())
        selected_category = st.selectbox(
"Job Category", categories, key="standard_category")

        roles = list(app.job_roles[selected_category].keys())
        selected_role = st.selectbox(
"Specific Role", roles, key="standard_role")

        role_info = app.job_roles[selected_category][selected_role]

        # Display role information
        st.html(f"""
        <div class="card" style="margin: var(--space-4) 0;">
            <div class="section-kicker"><i class="fas fa-briefcase"></i> Role Profile</div>
            <h3 style="margin-bottom: var(--space-2);">{selected_role}</h3>
            <p style="color: var(--color-text-secondary); margin-bottom: var(--space-4);">{role_info['description']}</p>
            <h4 style="font-size: var(--text-sm); text-transform: uppercase; letter-spacing: 0.05em; color: var(--color-text-tertiary); margin-bottom: var(--space-2);">Required Skills:</h4>
            <div style="display: flex; flex-wrap: wrap; gap: var(--space-2);">
                {''.join([f'<span class="tag">{skill}</span>' for skill in role_info['required_skills']])}
            </div>
        </div>
        """)

        # File Upload
        uploaded_file = st.file_uploader(
"Upload your resume", type=[
    'pdf', 'docx'], key="standard_file")

        if not uploaded_file:
            # Display empty state with a prominent upload button
            st.markdown(
                app.render_empty_state(
                "fas fa-cloud-upload-alt",
                "Upload your resume to get started with standard analysis"
                ),
                unsafe_allow_html=True
            )
            # Add a prominent upload button
            st.html('<div class="flex-center animate-fade-in" style="margin: var(--space-8) 0;">')

        if uploaded_file:
            # Add a prominent analyze button
            analyze_standard = st.button("🔍 Analyze My Resume",
                                type="primary",
                                width='stretch',
                                key="analyze_standard_button")

            if analyze_standard:
                with st.spinner("Analyzing your document..."):
                    # Get file content
                    text = ""
                    try:
                        if uploaded_file.type == "application/pdf":
                            try:
                                text = app.analyzer.extract_text_from_pdf(uploaded_file)
                            except Exception as pdf_error:
                                st.error(f"PDF extraction failed: {str(pdf_error)}")
                                st.info("Trying alternative PDF extraction method...")
                                # Try AI analyzer as backup
                                try:
                                    text = app.ai_analyzer.extract_text_from_pdf(uploaded_file)
                                except Exception as backup_error:
                                    st.error(f"All PDF extraction methods failed: {str(backup_error)}")
                                    return
                        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                            try:
                                text = app.analyzer.extract_text_from_docx(uploaded_file)
                            except Exception as docx_error:
                                st.error(f"DOCX extraction failed: {str(docx_error)}")
                                # Try AI analyzer as backup
                                try:
                                    text = app.ai_analyzer.extract_text_from_docx(uploaded_file)
                                except Exception as backup_error:
                                    st.error(f"All DOCX extraction methods failed: {str(backup_error)}")
                                    return
                        else:
                            text = uploaded_file.getvalue().decode()
                            
                        if not text or text.strip() == "":
                            st.error("Could not extract any text from the uploaded file. Please try a different file.")
                            return
                    except Exception as e:
                        st.error(f"Error reading file: {str(e)}")
                        return

                    # Analyze the document
                    analysis = app.analyzer.analyze_resume({'raw_text': text}, role_info)
                    
                    # Check if analysis returned an error
                    if 'error' in analysis:
                        st.error(analysis['error'])
                        return

                    # Show snowflake effect
                    st.snow()

                    # Save resume data to database
                    resume_data = {
                        'personal_info': {
                            'name': analysis.get('name', ''),
                            'email': analysis.get('email', ''),
                            'phone': analysis.get('phone', ''),
                            'linkedin': analysis.get('linkedin', ''),
                            'github': analysis.get('github', ''),
                            'portfolio': analysis.get('portfolio', '')
                        },
                        'summary': analysis.get('summary', ''),
                        'target_role': selected_role,
                        'target_category': selected_category,
                        'education': analysis.get('education', []),
                        'experience': analysis.get('experience', []),
                        'projects': analysis.get('projects', []),
                        'skills': analysis.get('skills', []),
                        'template': ''
                    }

                    # Save to database
                    try:
                        resume_id = save_resume_data(resume_data)

                        # Save analysis data
                        analysis_data = {
                            'resume_id': resume_id,
                            'ats_score': analysis['ats_score'],
                            'keyword_match_score': analysis['keyword_match']['score'],
                            'format_score': analysis['format_score'],
                            'section_score': analysis['section_score'],
                            'missing_skills': ','.join(analysis['keyword_match']['missing_skills']),
                            'recommendations': ','.join(analysis['suggestions'])
                        }
                        save_analysis_data(resume_id, analysis_data)
                        st.success("Resume data saved successfully!")
                    except Exception as e:
                        st.error(f"Error saving to database: {str(e)}")
                        print(f"Database error: {e}")

                    # Show results based on document type
                    if analysis.get('document_type') != 'resume':
                        st.error(f"⚠️ This appears to be a {analysis['document_type']} document, not a resume!")
                        st.warning("Please upload a proper resume for ATS analysis.")
                        return
                    # Display results in a modern card layout
                col1, col2 = st.columns(2)

                with col1:
                    # ATS Score Card with circular progress
                    st.html('<div class="card animate-fade-up">')
                    st.html('<h3 style="margin-bottom: var(--space-4);">ATS Score</h3>')
                    score_ring(analysis['ats_score'], "ATS Score")
                    st.html('</div>')

                    # app.display_analysis_results(analysis_results)

                    # Skills Match Card
                    st.html('<div class="card animate-fade-up animate-delay-1" style="margin-top: var(--space-4);">')
                    st.html('<h3 style="margin-bottom: var(--space-4);">Skills Match</h3>')
                    
                    metric_card("Keyword Match", f"{int(analysis.get('keyword_match', {}).get('score', 0))}%", icon="fas fa-key")

                    if analysis['keyword_match']['missing_skills']:
                        st.html('<div style="margin-top: var(--space-4);"><h4 style="font-size: var(--text-sm); color: var(--color-error); margin-bottom: var(--space-2);">Missing Skills:</h4><div style="display: flex; flex-wrap: wrap; gap: var(--space-2);">')
                        for skill in analysis['keyword_match']['missing_skills']:
                            st.html(f'<span class="tag tag--error">{skill}</span>')
                        st.html('</div></div>')

                    st.html('</div>')

                with col2:
                    # Format Score Card
                    st.html('<div class="card animate-fade-up animate-delay-1">')
                    st.html('<h3 style="margin-bottom: var(--space-4);">Format Analysis</h3>')
                    
                    metric_card("Format Score", f"{int(analysis.get('format_score', 0))}%", icon="fas fa-file-alt")
                    metric_card("Section Score", f"{int(analysis.get('section_score', 0))}%", icon="fas fa-puzzle-piece")

                    st.html('</div>')

                    # Suggestions Card with improved UI
                    st.html('<div class="card animate-fade-up animate-delay-2" style="margin-top: var(--space-4);">')
                    st.html('<div class="section-kicker"><i class="fas fa-clipboard-check"></i> Recommendations</div><h3 style="margin-bottom: var(--space-4);">Improvement Suggestions</h3>')

                    def render_suggestion_block(icon, title, items):
                        if not items: return
                        st.html(f"""
                        <div style='background: rgba(255,255,255,0.02); padding: var(--space-4); border-radius: var(--radius-md); border: 1px solid var(--color-border); margin-bottom: var(--space-3);'>
                            <h4 style='color: var(--color-accent); margin-bottom: var(--space-3); font-size: var(--text-sm); display: flex; align-items: center; gap: var(--space-2);'><i class="{icon}"></i> {title}</h4>
                            <ul style='list-style: none; padding-left: 0; margin: 0; display: flex; flex-direction: column; gap: var(--space-2);'>
                        """)
                        for item in items:
                            st.html(f"<li style='display: flex; gap: var(--space-2); align-items: start;'><i class='fas fa-check' style='color: var(--color-success); margin-top: 4px; font-size: 12px;'></i> <span style='color: var(--color-text-secondary); font-size: var(--text-sm);'>{item}</span></li>")
                        st.html("</ul></div>")

                    render_suggestion_block("fas fa-address-card", "Contact Information", analysis.get('contact_suggestions', []))
                    render_suggestion_block("fas fa-user-tie", "Professional Summary", analysis.get('summary_suggestions', []))
                    
                    skills_sugs = analysis.get('skills_suggestions', [])
                    if analysis['keyword_match']['missing_skills']:
                        skills_sugs.append(f"Consider adding these relevant skills: {', '.join(analysis['keyword_match']['missing_skills'])}")
                    render_suggestion_block("fas fa-bolt", "Skills", skills_sugs)
                    
                    render_suggestion_block("fas fa-briefcase", "Work Experience", analysis.get('experience_suggestions', []))
                    render_suggestion_block("fas fa-graduation-cap", "Education", analysis.get('education_suggestions', []))
                    render_suggestion_block("fas fa-file-alt", "Formatting", analysis.get('format_suggestions', []))

                    st.html("</div>")

                    # Course Recommendations
                st.markdown("""
                    <div class="feature-card">
                        <h2>📚 Recommended Courses</h2>
                    """, unsafe_allow_html=True)

                    # Get courses based on role and category
                courses = get_courses_for_role(selected_role)
                if not courses:
                        category = get_category_for_role(selected_role)
                        courses = COURSES_BY_CATEGORY.get(
                            category, {}).get(selected_role, [])

                    # Display courses in a grid
                cols = st.columns(2)
                for i, course in enumerate(
                    courses[:6]):  # Show top 6 courses
                        with cols[i % 2]:
                            st.html(f"""
                            <div class="card" style="margin: var(--space-3) 0;">
                                <h4 style="margin-bottom: var(--space-2);">{course[0]}</h4>
                                <a href='{course[1]}' target='_blank' style="color: var(--color-accent); font-size: var(--text-sm); text-decoration: none; display: flex; align-items: center; gap: var(--space-2);"><i class="fas fa-external-link-alt"></i> View Course</a>
                            </div>
                            """)

                st.markdown("</div>", unsafe_allow_html=True)

                    # Learning Resources
                st.markdown("""
                    <div class="feature-card">
                        <h2>📺 Helpful Videos</h2>
                    """, unsafe_allow_html=True)

                tab1, tab2 = st.tabs(["Resume Tips", "Interview Tips"])

                with tab1:
                        # Resume Videos
                        for category, videos in RESUME_VIDEOS.items():
                            st.subheader(category)
                            cols = st.columns(2)
                            for i, video in enumerate(videos):
                                with cols[i % 2]:
                                    st.video(video[1])

                with tab2:
                        # Interview Videos
                        for category, videos in INTERVIEW_VIDEOS.items():
                            st.subheader(category)
                            cols = st.columns(2)
                            for i, video in enumerate(videos):
                                with cols[i % 2]:
                                    st.video(video[1])

                st.markdown("</div>", unsafe_allow_html=True)

    with analyzer_tabs[1]:
        st.html("""
        <div class="card" style="margin: var(--space-4) 0; border-top: 3px solid var(--color-accent);">
            <div class="section-kicker"><i class="fas fa-brain"></i> Pro Analysis</div>
            <h3 style="margin-bottom: var(--space-2);">AI-Powered Resume Analysis</h3>
            <p style="color: var(--color-text-secondary); margin-bottom: var(--space-3);">Get detailed insights from advanced AI models that analyze your resume and provide personalized recommendations.</p>
            <p style="color: var(--color-text); font-weight: 500;">Upload your resume to get AI-powered analysis and recommendations.</p>
        </div>
        """)

        # AI Model Selection
        ai_model = st.selectbox(
            "Select AI Model",
            ["Google Gemini"],
            help="Choose the AI model to analyze your resume"
        )
         
        # Add job description input option
        use_custom_job_desc = st.checkbox("Use custom job description", value=False, 
                                         help="Enable this to provide a specific job description for more targeted analysis")
        
        custom_job_description = ""
        if use_custom_job_desc:
            custom_job_description = st.text_area(
                "Paste the job description here",
                height=200,
                placeholder="Paste the full job description from the company here for more targeted analysis...",
                help="Providing the actual job description will help the AI analyze your resume specifically for this position"
            )
            
            alert("<strong>Pro Tip:</strong> Including the actual job description significantly improves the accuracy of the analysis and provides more relevant recommendations tailored to the specific position.", "success")
         
                    # Add AI Analyzer Stats in an expander
        with st.expander("📊 AI Analyzer Statistics", expanded=False):
            try:
                # Add a reset button for admin users
                if st.session_state.get('is_admin', False):
                    if st.button(
"🔄 Reset AI Analysis Statistics",
type="secondary",
 key="reset_ai_stats_button_2"):
                        from config.database import reset_ai_analysis_stats
                        result = reset_ai_analysis_stats()
                        if result["success"]:
                            st.success(result["message"])
                        else:
                            st.error(result["message"])
                        # Refresh the page to show updated stats
                        st.experimental_rerun()

                # Get detailed AI analysis statistics
                from config.database import get_detailed_ai_analysis_stats
                ai_stats = get_detailed_ai_analysis_stats()

                if ai_stats["total_analyses"] > 0:
                    # Create a more visually appealing layout
                    # Stats cards use the design system metric-card

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        metric_card("Total AI Analyses", str(ai_stats["total_analyses"]), icon="fas fa-chart-bar")

                    with col2:
                        metric_card("Average Resume Score", f"{ai_stats['average_score']}/100", icon="fas fa-star")

                    with col3:
                        # Create a gauge chart for average score
                        import plotly.graph_objects as go
                        fig = go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=ai_stats["average_score"],
                            domain={'x': [0, 1], 'y': [0, 1]},
                            title={
'text': "Score", 'font': {
    'size': 14, 'color': 'white'}},
                            gauge={
                                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "white"},
                                'bar': {'color': "#38ef7d" if ai_stats["average_score"] >= 80 else "#FFEB3B" if ai_stats["average_score"] >= 60 else "#FF5252"},
                                'bgcolor': "rgba(0,0,0,0)",
                                'borderwidth': 2,
                                'bordercolor': "white",
                                'steps': [
                                    {'range': [
                                        0, 40], 'color': 'rgba(255, 82, 82, 0.3)'},
                                    {'range': [
                                        40, 70], 'color': 'rgba(255, 235, 59, 0.3)'},
                                    {'range': [
                                        70, 100], 'color': 'rgba(56, 239, 125, 0.3)'}
                                ],
                            }
                        ))

                        fig.update_layout(
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)',
                            font={'color': "white"},
                            height=150,
                            margin=dict(l=10, r=10, t=30, b=10)
                        )

                        st.plotly_chart(fig, width='stretch')

                    # Display model usage with enhanced visualization
                    if ai_stats["model_usage"]:
                        st.markdown("### 🤖 Model Usage")
                        model_data = pd.DataFrame(ai_stats["model_usage"])

                        # Create a more colorful pie chart
                        import plotly.express as px
                        fig = px.pie(
                            model_data,
                            values="count",
                            names="model",
                            color_discrete_sequence=px.colors.qualitative.Bold,
                            hole=0.4
                        )

                        fig.update_traces(
                            textposition='inside',
                            textinfo='percent+label',
                            marker=dict(
line=dict(
    color='#000000',
     width=1.5))
                        )

                        fig.update_layout(
                            margin=dict(l=20, r=20, t=30, b=20),
                            height=300,
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)',
                            font=dict(color="#ffffff", size=14),
                            legend=dict(
                                orientation="h",
                                yanchor="bottom",
                                y=-0.1,
                                xanchor="center",
                                x=0.5
                            ),
                            title={
                                'text': 'AI Model Distribution',
                                'y': 0.95,
                                'x': 0.5,
                                'xanchor': 'center',
                                'yanchor': 'top',
                                'font': {'size': 18, 'color': 'white'}
                            }
                        )

                        st.plotly_chart(fig, width='stretch')

                    # Display top job roles with enhanced visualization
                    if ai_stats["top_job_roles"]:
                        st.markdown("### 🎯 Top Job Roles")
                        roles_data = pd.DataFrame(
                            ai_stats["top_job_roles"])

                        # Create a more colorful bar chart
                        fig = px.bar(
                            roles_data,
                            x="role",
                            y="count",
                            color="count",
                            color_continuous_scale=px.colors.sequential.Viridis,
                            labels={
"role": "Job Role", "count": "Number of Analyses"}
                        )

                        fig.update_traces(
                            marker_line_width=1.5,
                            marker_line_color="white",
                            opacity=0.9
                        )

                        fig.update_layout(
                            margin=dict(l=20, r=20, t=50, b=30),
                            height=350,
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)',
                            font=dict(color="#ffffff", size=14),
                            title={
                                'text': 'Most Analyzed Job Roles',
                                'y': 0.95,
                                'x': 0.5,
                                'xanchor': 'center',
                                'yanchor': 'top',
                                'font': {'size': 18, 'color': 'white'}
                            },
                            xaxis=dict(
                                title="",
                                tickangle=-45,
                                tickfont=dict(size=12)
                            ),
                            yaxis=dict(
                                title="Number of Analyses",
                                gridcolor="rgba(255, 255, 255, 0.1)"
                            ),
                            coloraxis_showscale=False
                        )

                        st.plotly_chart(fig, width='stretch')

                        # Add a timeline chart for analysis over time (mock
                        # data for now)
                        st.markdown("### 📈 Analysis Trend")
                        st.info(
                            "This is a conceptual visualization. To implement actual time-based analysis, additional data collection would be needed.")

                        # Create mock data for timeline
                        import datetime
                        import numpy as np

                        today = datetime.datetime.now()
                        dates = [
(today -
datetime.timedelta(
    days=i)).strftime('%Y-%m-%d') for i in range(7)]
                        dates.reverse()

                        # Generate some random data that sums to
                        # total_analyses
                        total = ai_stats["total_analyses"]
                        if total > 7:
                            values = np.random.dirichlet(
                                np.ones(7)) * total
                            values = [round(v) for v in values]
                            # Adjust to make sure sum equals total
                            diff = total - sum(values)
                            values[-1] += diff
                        else:
                            values = [0] * 7
                            for i in range(total):
                                values[-(i % 7) - 1] += 1

                        trend_data = pd.DataFrame({
                            'Date': dates,
                            'Analyses': values
                        })

                        fig = px.line(
                            trend_data,
                            x='Date',
                            y='Analyses',
                            markers=True,
                            line_shape='spline',
                            color_discrete_sequence=["#38ef7d"]
                        )

                        fig.update_traces(
                            line=dict(width=3),
                            marker=dict(
size=8, line=dict(
    width=2, color='white'))
                        )

                        fig.update_layout(
                            margin=dict(l=20, r=20, t=50, b=30),
                            height=300,
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)',
                            font=dict(color="#ffffff", size=14),
                            title={
                                'text': 'Analysis Activity (Last 7 Days)',
                                'y': 0.95,
                                'x': 0.5,
                                'xanchor': 'center',
                                'yanchor': 'top',
                                'font': {'size': 18, 'color': 'white'}
                            },
                            xaxis=dict(
                                title="",
                                gridcolor="rgba(255, 255, 255, 0.1)"
                            ),
                            yaxis=dict(
                                title="Number of Analyses",
                                gridcolor="rgba(255, 255, 255, 0.1)"
                            )
                        )

                        st.plotly_chart(fig, width='stretch')

                    # Display score distribution if available
                    if ai_stats["score_distribution"]:
                        section_divider("Score Distribution Analysis")

                        score_data = pd.DataFrame(
                            ai_stats["score_distribution"])

                        # Create a more visually appealing bar chart for
                        # score distribution
                        fig = px.bar(
                            score_data,
                            x="range",
                            y="count",
                            color="range",
                            color_discrete_map={
                                "0-20": "#FF5252",
                                "21-40": "#FF7043",
                                "41-60": "#FFEB3B",
                                "61-80": "#8BC34A",
                                "81-100": "#38ef7d"
                            },
                            labels={
"range": "Score Range",
 "count": "Number of Resumes"},
                            text="count"  # Display count values on bars
                        )

                        fig.update_traces(
                            marker_line_width=2,
                            marker_line_color="white",
                            opacity=0.9,
                            textposition='outside',
                            textfont=dict(
color="white", size=14, family="Arial, sans-serif"),
                            hovertemplate="<b>Score Range:</b> %{x}<br><b>Number of Resumes:</b> %{y}<extra></extra>"
                        )

                        # Add a gradient background to the chart
                        fig.update_layout(
                            margin=dict(l=20, r=20, t=50, b=30),
                            height=400,  # Increase height for better visibility
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)',
                            font=dict(
color="#ffffff", size=14, family="Arial, sans-serif"),
                            # title={
                            #     # 'text': 'Resume Score Distribution',
                            #     'y': 0.95,
                            #     'x': 0.5,
                            #     'xanchor': 'center',
                            #     'yanchor': 'top',
                            #     'font': {'size': 22, 'color': 'white', 'family': 'Arial, sans-serif', 'weight': 'bold'}
                            # },
                            xaxis=dict(
                                title=dict(
text="Score Range", font=dict(
    size=16, color="white")),
                                categoryorder="array",
                                categoryarray=[
"0-20", "21-40", "41-60", "61-80", "81-100"],
                                tickfont=dict(size=14, color="white"),
                                gridcolor="rgba(255, 255, 255, 0.1)"
                            ),
                            yaxis=dict(
                                title=dict(
text="Number of Resumes", font=dict(
    size=16, color="white")),
                                tickfont=dict(size=14, color="white"),
                                gridcolor="rgba(255, 255, 255, 0.1)",
                                zeroline=False
                            ),
                            showlegend=False,
                            bargap=0.2,  # Adjust gap between bars
                            shapes=[
                                # Add gradient background
                                dict(
                                    type="rect",
                                    xref="paper",
                                    yref="paper",
                                    x0=0,
                                    y0=0,
                                    x1=1,
                                    y1=1,
                                    fillcolor="rgba(26, 26, 44, 0.5)",
                                    layer="below",
                                    line_width=0,
                                )
                            ]
                        )

                        # Add annotations for insights
                        if len(score_data) > 0:
                            max_count_idx = score_data["count"].idxmax()
                            max_range = score_data.iloc[max_count_idx]["range"]
                            max_count = score_data.iloc[max_count_idx]["count"]

                            fig.add_annotation(
                                x=0.5,
                                y=1.12,
                                xref="paper",
                                yref="paper",
                                text=f"Most resumes fall in the {max_range} score range",
                                showarrow=False,
                                font=dict(size=14, color="#FFEB3B"),
                                bgcolor="rgba(0,0,0,0.5)",
                                bordercolor="#FFEB3B",
                                borderwidth=1,
                                borderpad=4,
                                opacity=0.8
                            )

                        st.plotly_chart(fig, width='stretch')

                        st.html('<p style="color: var(--color-text-tertiary); text-align: center; font-style: italic; font-size: var(--text-sm); margin-top: var(--space-3);">This chart shows the distribution of resume scores across different ranges, helping identify common performance levels.</p>')

                    # Display recent analyses if available
                    if ai_stats["recent_analyses"]:
                        section_divider("Recent Resume Analyses")

                        # Build the table rows
                        table_rows = ""
                        for analysis_item in ai_stats["recent_analyses"]:
                            a_score = analysis_item["score"]
                            s_class = "tag--success" if a_score >= 80 else "tag--accent" if a_score >= 60 else "tag--error"
                            model_name = analysis_item["model"]
                            try:
                                from datetime import datetime
                                date_obj = datetime.strptime(analysis_item["date"], "%Y-%m-%d %H:%M:%S")
                                formatted_date = date_obj.strftime("%b %d, %Y")
                            except Exception:
                                formatted_date = analysis_item["date"]
                            table_rows += f'''
                            <tr>
                                <td><span class="tag">{model_name}</span></td>
                                <td><span class="tag {s_class}">{a_score}/100</span></td>
                                <td><span style="color: var(--color-text-secondary);">{analysis_item["job_role"]}</span></td>
                                <td><span style="color: var(--color-text-tertiary); font-size: var(--text-xs);">{formatted_date}</span></td>
                            </tr>
                            '''

                        st.html(f'''
                        <div class="card" style="overflow-x: auto;">
                        <table class="data-table">
                            <thead>
                            <tr>
                                <th>AI Model</th>
                                <th>Score</th>
                                <th>Job Role</th>
                                <th>Date</th>
                            </tr>
                            </thead>
                            <tbody>
                            {table_rows}
                            </tbody>
                        </table>
                        <p style="color: var(--color-text-tertiary); text-align: center; font-style: italic; margin-top: var(--space-4); font-size: var(--text-xs);">Most recent resume analyses performed by AI models.</p>
                        </div>
                        ''')
                else:
                    st.info(
                        "No AI analysis data available yet. Upload and analyze resumes to see statistics here.")
            except Exception as e:
                st.error(f"Error loading AI analysis statistics: {str(e)}")

        # Job Role Selection for AI Analysis
        categories = list(app.job_roles.keys())
        selected_category = st.selectbox(
"Job Category", categories, key="ai_category")

        roles = list(app.job_roles[selected_category].keys())
        selected_role = st.selectbox("Specific Role", roles, key="ai_role")

        role_info = app.job_roles[selected_category][selected_role]

        # Display role information
        st.html(f"""
        <div class="card" style="margin: var(--space-4) 0;">
            <div class="section-kicker"><i class="fas fa-briefcase"></i> Role Profile</div>
            <h3 style="margin-bottom: var(--space-2);">{selected_role}</h3>
            <p style="color: var(--color-text-secondary); margin-bottom: var(--space-4);">{role_info['description']}</p>
            <h4 style="font-size: var(--text-sm); text-transform: uppercase; letter-spacing: 0.05em; color: var(--color-text-tertiary); margin-bottom: var(--space-2);">Required Skills:</h4>
            <div style="display: flex; flex-wrap: wrap; gap: var(--space-2);">
                {''.join([f'<span class="tag">{skill}</span>' for skill in role_info['required_skills']])}
            </div>
        </div>
        """)

        # File Upload for AI Analysis
        uploaded_file = st.file_uploader(
"Upload your resume", type=[
    'pdf', 'docx'], key="ai_file")

        if not uploaded_file:
        # Display empty state with a prominent upload button
            st.markdown(
            app.render_empty_state(
        "fas fa-robot",
                    "Upload your resume to get AI-powered analysis and recommendations"
    ),
    unsafe_allow_html=True
)
        else:
            # Add a prominent analyze button
            analyze_ai = st.button("🤖 Analyze with AI",
                            type="primary",
                            width='stretch',
                            key="analyze_ai_button")

            if analyze_ai:
                with st.spinner(f"Analyzing your resume with {ai_model}..."):
                    # Get file content
                    text = ""
                    try:
                        if uploaded_file.type == "application/pdf":
                            text = app.analyzer.extract_text_from_pdf(
                                uploaded_file)
                        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                            text = app.analyzer.extract_text_from_docx(
                                uploaded_file)
                        else:
                            text = uploaded_file.getvalue().decode()
                    except Exception as e:
                        st.error(f"Error reading file: {str(e)}")
                        st.stop()

                    # Analyze with AI
                    try:
                        # Show a loading animation
                        with st.spinner("🧠 AI is analyzing your resume..."):
                            progress_bar = st.progress(0)
                            
                            # Get the selected model
                            selected_model = "Google Gemini"
                            
                            # Update progress
                            progress_bar.progress(10)
                            
                            # Extract text from the resume
                            analyzer = AIResumeAnalyzer()
                            if uploaded_file.type == "application/pdf":
                                resume_text = analyzer.extract_text_from_pdf(
                                    uploaded_file)
                            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                                resume_text = analyzer.extract_text_from_docx(
                                    uploaded_file)
                            else:
                                # For text files or other formats
                                resume_text = uploaded_file.getvalue().decode('utf-8')
                            
                            # Initialize the AI analyzer (moved after text extraction)
                            progress_bar.progress(30)
                            
                            # Get the job role
                            job_role = selected_role if selected_role else "Not specified"
                            
                            # Update progress
                            progress_bar.progress(50)
                            
                            # Analyze the resume with Google Gemini
                            if use_custom_job_desc and custom_job_description:
                                # Use custom job description for analysis
                                analysis_result = analyzer.analyze_resume_with_gemini(
                                    resume_text, job_role=job_role, job_description=custom_job_description)
                                # Show that custom job description was used
                                st.session_state['used_custom_job_desc'] = True
                            else:
                                # Use standard role-based analysis
                                analysis_result = analyzer.analyze_resume_with_gemini(
                                    resume_text, job_role=job_role)
                                st.session_state['used_custom_job_desc'] = False

                            
                            # Update progress
                            progress_bar.progress(80)
                            
                            # Save the analysis to the database
                            if analysis_result and "error" not in analysis_result:
                                # Extract the resume score
                                resume_score = analysis_result.get(
                                    "resume_score", 0)
                                
                                # Save to database
                                save_ai_analysis_data(
                                    None,  # No user_id needed
                                    {
                                        "model_used": selected_model,
                                        "resume_score": resume_score,
                                        "job_role": job_role
                                    }
                                )
                            # show snowflake effect
                            st.snow()

                            # Complete the progress
                            progress_bar.progress(100)
                            
                            # Display the analysis result
                            if analysis_result and "error" not in analysis_result:
                                st.success("✅ Analysis complete!")
                                
                                # Extract data from the analysis
                                full_response = analysis_result.get(
                                    "analysis", "")
                                resume_score = analysis_result.get(
                                    "resume_score", 0)
                                ats_score = analysis_result.get(
                                    "ats_score", 0)
                                model_used = analysis_result.get(
                                    "model_used", selected_model)
                                
                                # Store the full response in session state for download
                                st.session_state['full_analysis'] = full_response
                                
                                # Display the analysis in a nice format
                                section_divider("Full Analysis Report")
                                
                                # Get current date
                                from datetime import datetime
                                current_date = datetime.now().strftime("%B %d, %Y")
                                
                                # Create a modern styled header for the report
                                custom_jd_html = '<span class="tag tag--success" style="margin-top: var(--space-2);"><i class="fas fa-check"></i> Custom Job Description Used</span>' if st.session_state.get('used_custom_job_desc', False) else ''
                                score_status = "Excellent" if resume_score >= 80 else "Good" if resume_score >= 60 else "Needs Improvement"
                                st.html(f"""
                                <div class="card" style="margin-bottom: var(--space-6);">
                                    <div class="section-kicker"><i class="fas fa-file-medical-alt"></i> AI Analysis Report</div>
                                    <h2 style="margin-bottom: var(--space-4);">Resume Analysis Report</h2>
                                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: var(--space-4);">
                                        <div>
                                            <span style="color: var(--color-text-tertiary); font-size: var(--text-xs); text-transform: uppercase; letter-spacing: 0.05em;">Job Role</span>
                                            <p style="color: var(--color-text); font-weight: 500;">{job_role if job_role else 'Not specified'}</p>
                                        </div>
                                        <div>
                                            <span style="color: var(--color-text-tertiary); font-size: var(--text-xs); text-transform: uppercase; letter-spacing: 0.05em;">Analysis Date</span>
                                            <p style="color: var(--color-text); font-weight: 500;">{current_date}</p>
                                        </div>
                                        <div>
                                            <span style="color: var(--color-text-tertiary); font-size: var(--text-xs); text-transform: uppercase; letter-spacing: 0.05em;">AI Model</span>
                                            <p style="color: var(--color-text); font-weight: 500;">{model_used}</p>
                                        </div>
                                        <div>
                                            <span style="color: var(--color-text-tertiary); font-size: var(--text-xs); text-transform: uppercase; letter-spacing: 0.05em;">Overall Score</span>
                                            <p style="color: var(--color-text); font-weight: 500;">{resume_score}/100 — {score_status}</p>
                                            {custom_jd_html}
                                        </div>
                                    </div>
                                </div>
                                """)
                                
                                # Add gauge charts for scores
                                import plotly.graph_objects as go
                                
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    # Resume Score Gauge
                                    fig1 = go.Figure(go.Indicator(
                                        mode="gauge+number",
                                        value=resume_score,
                                        domain={'x': [0, 1], 'y': [0, 1]},
                                        title={'text': "Resume Score", 'font': {'size': 16}},
                                        gauge={
                                            'axis': {'range': [0, 100], 'tickwidth': 1},
                                            'bar': {'color': "#06b6d4" if resume_score >= 80 else "#FFA500" if resume_score >= 60 else "#FF4444"},
                                            'bgcolor': "white",
                                            'borderwidth': 2,
                                            'bordercolor': "gray",
                                            'steps': [
                                                {'range': [0, 40], 'color': 'rgba(255, 68, 68, 0.2)'},
                                                {'range': [40, 60], 'color': 'rgba(255, 165, 0, 0.2)'},
                                                {'range': [60, 80], 'color': 'rgba(255, 214, 0, 0.2)'},
                                                {'range': [80, 100], 'color': 'rgba(76, 175, 80, 0.2)'}
                                            ],
                                            'threshold': {
                                                'line': {'color': "red", 'width': 4},
                                                'thickness': 0.75,
                                                'value': 60
                                            }
                                        }
                                    ))
                                    
                                    fig1.update_layout(
                                        height=250,
                                        margin=dict(l=20, r=20, t=50, b=20),
                                    )
                                    
                                    st.plotly_chart(fig1, width='stretch')
                                    
                                    status = "Excellent" if resume_score >= 80 else "Good" if resume_score >= 60 else "Needs Improvement"
                                    st.markdown(f"<div style='text-align: center; font-weight: bold;'>{status}</div>", unsafe_allow_html=True)
                                
                                with col2:
                                    # ATS Score Gauge
                                    fig2 = go.Figure(go.Indicator(
                                        mode="gauge+number",
                                        value=ats_score,
                                        domain={'x': [0, 1], 'y': [0, 1]},
                                        title={'text': "ATS Optimization Score", 'font': {'size': 16}},
                                        gauge={
                                            'axis': {'range': [0, 100], 'tickwidth': 1},
                                            'bar': {'color': "#06b6d4" if ats_score >= 80 else "#FFA500" if ats_score >= 60 else "#FF4444"},
                                            'bgcolor': "white",
                                            'borderwidth': 2,
                                            'bordercolor': "gray",
                                            'steps': [
                                                {'range': [0, 40], 'color': 'rgba(255, 68, 68, 0.2)'},
                                                {'range': [40, 60], 'color': 'rgba(255, 165, 0, 0.2)'},
                                                {'range': [60, 80], 'color': 'rgba(255, 214, 0, 0.2)'},
                                                {'range': [80, 100], 'color': 'rgba(76, 175, 80, 0.2)'}
                                            ],
                                            'threshold': {
                                                'line': {'color': "red", 'width': 4},
                                                'thickness': 0.75,
                                                'value': 60
                                            }
                                        }
                                    ))
                                    
                                    fig2.update_layout(
                                        height=250,
                                        margin=dict(l=20, r=20, t=50, b=20),
                                    )
                                    
                                    st.plotly_chart(fig2, width='stretch')
                                    
                                    status = "Excellent" if ats_score >= 80 else "Good" if ats_score >= 60 else "Needs Improvement"
                                    st.markdown(f"<div style='text-align: center; font-weight: bold;'>{status}</div>", unsafe_allow_html=True)

                                # Add Job Description Match Score if custom job description was used
                                if st.session_state.get('used_custom_job_desc', False) and custom_job_description:
                                    # Extract job match score from analysis result or calculate it
                                    job_match_score = analysis_result.get("job_match_score", 0)
                                    if not job_match_score and "job_match" in analysis_result:
                                        job_match_score = analysis_result["job_match"].get("score", 0)
                                    
                                    # If we have a job match score, display it
                                    if job_match_score:
                                        st.markdown("""
                                        <h3 style="background: linear-gradient(90deg, #4d7c0f, #84cc16); color: white; padding: 10px; border-radius: 5px; margin-top: 20px;">
                                            <i class="fas fa-handshake"></i> Job Description Match Analysis
                                        </h3>
                                        """, unsafe_allow_html=True)
                                        
                                        col1, col2 = st.columns(2)
                                        
                                        with col1:
                                            # Job Match Score Gauge
                                            fig3 = go.Figure(go.Indicator(
                                                mode="gauge+number",
                                                value=job_match_score,
                                                domain={'x': [0, 1], 'y': [0, 1]},
                                                title={'text': "Job Match Score", 'font': {'size': 16}},
                                                gauge={
                                                    'axis': {'range': [0, 100], 'tickwidth': 1},
                                                    'bar': {'color': "#06b6d4" if job_match_score >= 80 else "#FFA500" if job_match_score >= 60 else "#FF4444"},
                                                    'bgcolor': "white",
                                                    'borderwidth': 2,
                                                    'bordercolor': "gray",
                                                    'steps': [
                                                        {'range': [0, 40], 'color': 'rgba(255, 68, 68, 0.2)'},
                                                        {'range': [40, 60], 'color': 'rgba(255, 165, 0, 0.2)'},
                                                        {'range': [60, 80], 'color': 'rgba(255, 214, 0, 0.2)'},
                                                        {'range': [80, 100], 'color': 'rgba(76, 175, 80, 0.2)'}
                                                    ],
                                                    'threshold': {
                                                        'line': {'color': "red", 'width': 4},
                                                        'thickness': 0.75,
                                                        'value': 60
                                                    }
                                                }
                                            ))
                                            
                                            fig3.update_layout(
                                                height=250,
                                                margin=dict(l=20, r=20, t=50, b=20),
                                            )
                                            
                                            st.plotly_chart(fig3, width='stretch')
                                            
                                            match_status = "Excellent Match" if job_match_score >= 80 else "Good Match" if job_match_score >= 60 else "Low Match"
                                            st.markdown(f"<div style='text-align: center; font-weight: bold;'>{match_status}</div>", unsafe_allow_html=True)
                                        
                                        with col2:
                                            st.markdown("""
                                            <div style="background-color: #262730; padding: 20px; border-radius: 10px; height: 100%;">
                                                <h4 style="color: #ffffff; margin-bottom: 15px;">What This Means</h4>
                                                <p style="color: #ffffff;">This score represents how well your resume matches the specific job description you provided.</p>
                                                <ul style="color: #ffffff; padding-left: 20px;">
                                                    <li><strong>80-100:</strong> Excellent match - your resume is highly aligned with this job</li>
                                                    <li><strong>60-79:</strong> Good match - your resume matches many requirements</li>
                                                    <li><strong>Below 60:</strong> Consider tailoring your resume more specifically to this job</li>
                                                </ul>
                                            </div>
                                            """, unsafe_allow_html=True)
                                

                                # Format the full response with better styling
                                formatted_analysis = full_response
                                
                                # Replace section headers with styled headers
                                section_styles = {
                                    "## Overall Assessment": '<div class="report-section"><h3><i class="fas fa-chart-line"></i> Overall Assessment</h3><div class="section-content">',
                                    "## Professional Profile Analysis": '<div class="report-section"><h3><i class="fas fa-user-tie"></i> Professional Profile Analysis</h3><div class="section-content">',
                                    "## Skills Analysis": '<div class="report-section"><h3><i class="fas fa-tools"></i> Skills Analysis</h3><div class="section-content">',
                                    "## Experience Analysis": '<div class="report-section"><h3><i class="fas fa-briefcase"></i> Experience Analysis</h3><div class="section-content">',
                                    "## Education Analysis": '<div class="report-section"><h3><i class="fas fa-graduation-cap"></i> Education Analysis</h3><div class="section-content">',
                                    "## Key Strengths": '<div class="report-section"><h3><i class="fas fa-check-circle"></i> Key Strengths</h3><div class="section-content">',
                                    "## Areas for Improvement": '<div class="report-section"><h3><i class="fas fa-exclamation-circle"></i> Areas for Improvement</h3><div class="section-content">',
                                    "## ATS Optimization Assessment": '<div class="report-section"><h3><i class="fas fa-robot"></i> ATS Optimization Assessment</h3><div class="section-content">',
                                    "## Recommended Courses": '<div class="report-section"><h3><i class="fas fa-book"></i> Recommended Courses</h3><div class="section-content">',
                                    "## Resume Score": '<div class="report-section"><h3><i class="fas fa-star"></i> Resume Score</h3><div class="section-content">',
                                    "## Role Alignment Analysis": '<div class="report-section"><h3><i class="fas fa-bullseye"></i> Role Alignment Analysis</h3><div class="section-content">',
                                    "## Job Match Analysis": '<div class="report-section"><h3><i class="fas fa-handshake"></i> Job Match Analysis</h3><div class="section-content">',
                                }
                                
                                # Apply the styling to each section
                                for section, style in section_styles.items():
                                    if section in formatted_analysis:
                                        formatted_analysis = formatted_analysis.replace(
                                            section, style)
                                        # Add closing div tags
                                        next_section = False
                                        for next_sec in section_styles.keys():
                                            if next_sec != section and next_sec in formatted_analysis.split(style)[1]:
                                                split_text = formatted_analysis.split(style)[1].split(next_sec)
                                                formatted_analysis = formatted_analysis.split(style)[0] + style + split_text[0] + "</div></div>" + next_sec + "".join(split_text[1:])
                                                next_section = True
                                                break
                                        if not next_section:
                                            formatted_analysis = formatted_analysis + "</div></div>"
                                
                                # Remove any extra closing div tags that might have been added
                                formatted_analysis = formatted_analysis.replace("</div></div></div></div>", "</div></div>")
                                
                                # Ensure we don't have any orphaned closing tags at the end
                                if formatted_analysis.endswith("</div>"):
                                    # Count opening and closing div tags
                                    open_tags = formatted_analysis.count("<div")
                                    close_tags = formatted_analysis.count("</div>")
                                    
                                    # If we have more closing than opening tags, remove the extras
                                    if close_tags > open_tags:
                                        excess = close_tags - open_tags
                                        formatted_analysis = formatted_analysis[:-6 * excess]
                                
                                # Clean up any visible HTML tags that might appear in the text
                                formatted_analysis = formatted_analysis.replace("&lt;/div&gt;", "")
                                formatted_analysis = formatted_analysis.replace("&lt;div&gt;", "")
                                formatted_analysis = formatted_analysis.replace("<div>", "<div>")  # Ensure proper opening
                                formatted_analysis = formatted_analysis.replace("</div>", "</div>")  # Ensure proper closing
                                
                                # The .report-section and .section-content styles
                                # now live in style.css — no inline <style> needed.

                                # Display the formatted analysis
                                st.markdown(f"""
                                <div class="card" style="padding: var(--space-5);">
                                    {formatted_analysis}
                                </div>
                                """, unsafe_allow_html=True)

                                # Create a PDF report
                                pdf_buffer = app.ai_analyzer.generate_pdf_report(
                                    analysis_result={
                                        "score": resume_score,
                                        "ats_score": ats_score,
                                        "model_used": model_used,
                                        "full_response": full_response,
                                        "strengths": analysis_result.get("strengths", []),
                                        "weaknesses": analysis_result.get("weaknesses", []),
                                        "used_custom_job_desc": st.session_state.get('used_custom_job_desc', False),
                                        "custom_job_description": custom_job_description if st.session_state.get('used_custom_job_desc', False) else ""
                                    },
                                    candidate_name=st.session_state.get(
                                        'candidate_name', 'Candidate'),
                                    job_role=selected_role
                                )

                                # PDF download button
                                if pdf_buffer:
                                    st.download_button(
                                        label="📊 Download PDF Report",
                                        data=pdf_buffer,
                                        file_name=f"resume_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                                        mime="application/pdf",
                                        width='stretch',
                                        on_click=lambda: st.balloons()
                                    )
                                else:
                                    st.error("PDF generation failed. Please try again later.")
                            else:
                                st.error(f"Analysis failed: {analysis_result.get('error', 'Unknown error')}")
                    except Exception as ai_error:
                        st.error(f"Error during AI analysis: {str(ai_error)}")
                        import traceback as tb
                        st.code(tb.format_exc())
