import streamlit as st

def page_header(title, subtitle=None):
    """Render a consistent premium page header"""
    st.html(
        f'''
        <div class="animate-fade-up" style="margin-bottom: var(--space-8);">
            <div class="section-kicker"><i class="fas fa-layer-group"></i> Smart Resume AI</div>
            <h1 class="text-gradient" style="margin-bottom: var(--space-2);">{title}</h1>
            {f'<p style="color: var(--color-text-secondary); font-size: var(--text-lg); max-width: 68ch;">{subtitle}</p>' if subtitle else ''}
        </div>
        '''
    )

def hero_section(title, subtitle=None, description=None):
    """Render an elite hero section with mesh gradient background"""
    if description and not subtitle:
        subtitle = description
        description = None
    
    st.html(
        f'''
        <div class="hero-container animate-fade-up">
            <div class="hero-grid">
                <div class="hero-copy">
                    <div class="section-kicker"><i class="fas fa-bolt"></i> AI-Powered Analysis</div>
                    <h1 class="hero-title text-gradient animate-delay-1">{title}</h1>
                    {f'<div class="hero-subtitle animate-delay-2">{subtitle}</div>' if subtitle else ''}
                    {f'<p class="hero-description animate-delay-3" style="color: var(--color-text-secondary); font-size: var(--text-base); max-width: 60ch;">{description}</p>' if description else ''}
                    
                    <div class="hero-stats-row animate-delay-3" style="margin-top: var(--space-6);">
                        <div class="hero-stat">
                            <span class="hero-stat__label">Analysis</span>
                            <span class="hero-stat__value">Deep Scan</span>
                        </div>
                        <div class="hero-stat">
                            <span class="hero-stat__label">Focus</span>
                            <span class="hero-stat__value">ATS & Keywords</span>
                        </div>
                        <div class="hero-stat">
                            <span class="hero-stat__label">Result</span>
                            <span class="hero-stat__value">Actionable Edits</span>
                        </div>
                    </div>
                </div>
                
                <div class="hero-panel animate-delay-2">
                    <div class="card card--glass">
                        <div class="section-kicker"><i class="fas fa-signal"></i> Live Reading Pane</div>
                        <h3 style="margin-bottom: var(--space-2);">Your resume, translated</h3>
                        <p style="color: var(--color-text-secondary); margin-bottom: var(--space-4); font-size: var(--text-sm);">We treat each upload like a dossier: clean structure, obvious strengths, and the gaps a recruiter will notice first.</p>
                        
                        <div class="progress-track">
                            <div class="progress-bar" style="width: 72%;"></div>
                        </div>
                    </div>
                    
                    <div class="grid-3" style="margin-top: var(--space-4);">
                        <div class="hero-stat">
                            <span class="hero-stat__label">Readability</span>
                            <span class="hero-stat__value" style="font-size: var(--text-xs);">Clear hierarchy</span>
                        </div>
                        <div class="hero-stat">
                            <span class="hero-stat__label">Keywords</span>
                            <span class="hero-stat__value" style="font-size: var(--text-xs);">Role Matched</span>
                        </div>
                        <div class="hero-stat">
                            <span class="hero-stat__label">Format</span>
                            <span class="hero-stat__value" style="font-size: var(--text-xs);">ATS-safe</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        '''
    )

def feature_card(icon, title, description):
    """Render a modern feature card"""
    st.html(f"""
        <div class="feature-card">
            <div class="feature-card__icon"><i class="{icon}"></i></div>
            <h3 class="feature-card__title">{title}</h3>
            <p class="feature-card__desc">{description}</p>
        </div>
    """)

def metric_card(label, value, delta=None, icon=None):
    """Render a modern metric card"""
    icon_html = f'<i class="{icon}"></i>' if icon else ''
    
    if delta:
        is_positive = "+" in str(delta) or "up" in str(delta).lower()
        trend_class = "metric-card__trend--up" if is_positive else "metric-card__trend--down"
        trend_icon = "fa-arrow-up" if is_positive else "fa-arrow-down"
        delta_html = f'<div class="metric-card__trend {trend_class}"><i class="fas {trend_icon}"></i>{delta}</div>'
    else:
        delta_html = ''
    
    st.html(f"""
        <div class="metric-card">
            <div class="flex-between">
                <span class="metric-card__label">{label}</span>
                <span style="color: var(--color-text-tertiary);">{icon_html}</span>
            </div>
            <div class="flex-between" style="align-items: flex-end; margin-top: var(--space-2);">
                <span class="metric-card__value">{value}</span>
                {delta_html}
            </div>
        </div>
    """)

def score_ring(score, label="Score"):
    """Render a CSS-only conic gradient score ring"""
    score_num = int(score) if str(score).isdigit() or isinstance(score, (int, float)) else 0
    
    # Determine color based on score
    if score_num >= 80:
        color = "var(--color-success)"
        status = "Excellent"
        status_color = "var(--color-success)"
    elif score_num >= 60:
        color = "var(--color-warning)"
        status = "Good"
        status_color = "var(--color-warning)"
    else:
        color = "var(--color-error)"
        status = "Needs Improvement"
        status_color = "var(--color-error)"

    st.html(f"""
        <div class="score-ring">
            <div class="score-ring__circle" style="background: conic-gradient({color} {score_num}%, rgba(255,255,255,0.05) 0);">
                <div class="score-ring__inner">
                    <span class="score-ring__number">{score_num}</span>
                    <span class="score-ring__label">{label}</span>
                </div>
            </div>
            <div class="score-ring__status" style="color: {status_color};">{status}</div>
        </div>
    """)

def section_divider(label=None):
    """Render a clean section divider with optional label"""
    if label:
        st.html(f"""
            <div style="display: flex; align-items: center; margin: var(--space-8) 0 var(--space-6);">
                <div style="flex-grow: 1; height: 1px; background: var(--color-border);"></div>
                <span style="padding: 0 var(--space-4); font-family: var(--font-mono); font-size: var(--text-xs); color: var(--color-text-tertiary); text-transform: uppercase; letter-spacing: var(--tracking-wide);">{label}</span>
                <div style="flex-grow: 1; height: 1px; background: var(--color-border);"></div>
            </div>
        """)
    else:
        st.html('<div style="height: 1px; background: var(--color-border); margin: var(--space-8) 0 var(--space-6);"></div>')


def template_card(title, description, image_url=None):
    """Render a premium template card"""
    image_html = f'<img src="{image_url}" style="width: 100%; border-radius: var(--radius-md); margin-bottom: var(--space-4);" />' if image_url else ''
    
    st.html(f"""
        <div class="card">
            {image_html}
            <h3 style="margin-bottom: var(--space-2);">{title}</h3>
            <p style="color: var(--color-text-secondary); font-size: var(--text-sm); margin: 0;">{description}</p>
        </div>
    """)

def feedback_card(name, feedback, rating):
    """Render a modern feedback card"""
    stars = "★" * int(rating) + "☆" * (5 - int(rating))
    
    st.html(f"""
        <div class="card">
            <div class="flex-between" style="margin-bottom: var(--space-3);">
                <div style="font-weight: 600; color: var(--color-text);">{name}</div>
                <div style="color: var(--color-accent); font-size: var(--text-sm); letter-spacing: 2px;">{stars}</div>
            </div>
            <p style="color: var(--color-text-secondary); font-size: var(--text-sm); margin: 0;">"{feedback}"</p>
        </div>
    """)

def alert(message, type="info"):
    """Display a premium alert banner"""
    types = {
        "info": {"class": "card--info", "icon": "fa-info-circle", "color": "var(--color-info)"},
        "success": {"class": "card--success", "icon": "fa-check-circle", "color": "var(--color-success)"},
        "warning": {"class": "card--warning", "icon": "fa-exclamation-triangle", "color": "var(--color-warning)"},
        "error": {"class": "card--error", "icon": "fa-times-circle", "color": "var(--color-error)"}
    }
    
    config = types.get(type, types["info"])
    
    st.html(f"""
        <div class="card {config['class']}" style="padding: var(--space-4); display: flex; align-items: flex-start; gap: var(--space-3); margin-bottom: var(--space-4);">
            <i class="fas {config['icon']}" style="color: {config['color']}; margin-top: 3px;"></i>
            <span style="color: var(--color-text); font-size: var(--text-sm);">{message}</span>
        </div>
    """)

# Legacy placeholders to prevent app crashes before all pages are migrated
def about_section(*args, **kwargs): pass
def loading_spinner(*args, **kwargs): pass
def progress_bar(*args, **kwargs): pass
def data_table(*args, **kwargs): pass
def apply_modern_styles(): pass
