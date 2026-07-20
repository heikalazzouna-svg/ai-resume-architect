import streamlit as st
import plotly.graph_objects as go
from datetime import datetime

from ui_components import page_header, apply_modern_styles
from config.database import get_analysis_history


def render(app):
    """Render the Score History page."""
    page_header("Score History", "Track how your resume improves over time")

    st.markdown("""
    <div class="bento-card" style="margin-bottom: 2rem;">
        <p style="color: var(--text-secondary); margin: 0;">
            Enter the email address you used when analysing your resume to see
            your ATS score progression over time.
        </p>
    </div>
    """, unsafe_allow_html=True)

    email = st.text_input(
        "Your email address",
        placeholder="e.g. you@example.com",
        key="history_email_input",
    )

    if not email:
        st.info("Enter your email above to view your analysis history.")
        return

    history = get_analysis_history(email)

    if not history:
        st.warning("No analysis records found for this email. Try analysing a resume first!")
        return

    # --- Summary metrics ---
    latest = history[-1]
    first = history[0]
    delta = round(latest['ats_score'] - first['ats_score'], 1) if len(history) > 1 else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Latest ATS Score", f"{latest['ats_score']:.0f}", delta=f"{delta:+.0f}" if delta else None)
    col2.metric("Analyses", len(history))
    col3.metric("Best Score", f"{max(h['ats_score'] for h in history):.0f}")
    col4.metric("Format Score", f"{latest['format_score']:.0f}")

    # --- Score progression chart ---
    st.markdown("### Score Progression")

    dates = [h['analyzed_at'] for h in history]
    ats_scores = [h['ats_score'] for h in history]
    keyword_scores = [h['keyword_match_score'] for h in history]
    format_scores = [h['format_score'] for h in history]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates, y=ats_scores, name="ATS Score",
        mode="lines+markers",
        line=dict(color="#06b6d4", width=3),
        marker=dict(size=8),
    ))
    fig.add_trace(go.Scatter(
        x=dates, y=keyword_scores, name="Keyword Match",
        mode="lines+markers",
        line=dict(color="#4f46e5", width=2, dash="dot"),
        marker=dict(size=6),
    ))
    fig.add_trace(go.Scatter(
        x=dates, y=format_scores, name="Format Score",
        mode="lines+markers",
        line=dict(color="#a855f7", width=2, dash="dash"),
        marker=dict(size=6),
    ))

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis_title="Date",
        yaxis_title="Score",
        yaxis=dict(range=[0, 105]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        margin=dict(l=40, r=20, t=40, b=40),
        height=400,
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- Detailed history table ---
    st.markdown("### Analysis Details")
    for i, record in enumerate(reversed(history)):
        with st.expander(f"Analysis #{len(history) - i} - ATS {record['ats_score']:.0f} - {record['analyzed_at']}", expanded=(i == 0)):
            mc1, mc2, mc3 = st.columns(3)
            mc1.metric("ATS Score", f"{record['ats_score']:.0f}")
            mc2.metric("Keyword Match", f"{record['keyword_match_score']:.0f}")
            mc3.metric("Format Score", f"{record['format_score']:.0f}")

            if record.get('missing_skills'):
                st.markdown("**Missing Skills:**")
                skills = record['missing_skills'].split(',')
                st.markdown(", ".join(f"`{s.strip()}`" for s in skills if s.strip()))

            if record.get('recommendations'):
                st.markdown("**Recommendations:**")
                recs = record['recommendations'].split(',')
                for rec in recs:
                    if rec.strip():
                        st.markdown(f"- {rec.strip()}")
