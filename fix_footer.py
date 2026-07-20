with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

# Replace the hardcoded footer (line 492-502 approx) with the correct one
import re
footer_pattern = r'# Footer text\s*st\.markdown\("""\s*<p style=\'text-align: center;\'>\s*Powered by.*?Every star counts!.*?</p>\s*"""\s*,\s*unsafe_allow_html=True\s*\)'

new_footer = """# Footer text
            st.markdown(f\"\"\"
            <div style="text-align: center; margin-top: 50px; padding-top: 20px; border-top: 1px solid var(--border-color);">
                <p>Powered by <b>Streamlit</b> and <b>Google Gemini AI</b> | Developed by <b>{FOUNDER_NAME}</b></p>
                <p>?? <strong>Privacy First:</strong> Your resume data is secure, never sold, and only saved with explicit consent.</p>
            </div>
            \"\"\", unsafe_allow_html=True)"""

content = re.sub(footer_pattern, new_footer, content, flags=re.DOTALL)

# Replace the Star this repo button
star_pattern = r'# Add GitHub star button\s*st\.markdown\("""\s*<div style="display: flex;.*?</div>\s*"""\s*,\s*unsafe_allow_html=True\s*\)'
content = re.sub(star_pattern, '', content, flags=re.DOTALL)

# Replace the Profile Section in About
about_pattern = r'# Profile Section.*?<a href="https://github.com/Hunterdii" class="social-link" target="_blank">.*?</a>'

new_about = """# Profile Section
        st.markdown(f\"\"\"
            <div class="profile-section">
                <img src="{image_base64 if image_base64 else ''}"
                     alt="{FOUNDER_NAME}"
                     class="profile-image">
                <h2 class="profile-name">{FOUNDER_NAME}</h2>
                <p class="profile-title">{FOUNDER_TITLE}</p>
                <p style="text-align: center; color: var(--text-secondary); max-width: 600px; margin: 10px auto;">{FOUNDER_BIO}</p>
                <div class="social-links">
                    <a href="{SOCIAL_LINKS['linkedin']}" class="social-link" target="_blank">
                        <i class="fab fa-linkedin"></i>
                    </a>"""

content = re.sub(about_pattern, new_about, content, flags=re.DOTALL)

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)
