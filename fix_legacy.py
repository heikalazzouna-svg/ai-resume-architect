import re

with open("app.py", "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

# Remove all st.toast related to Hunterdii
content = re.sub(r'st\.toast\([^)]*Hunterdii[^)]*\)', '', content)

# Remove the HTML list items pointing to Hunterdii repos
content = re.sub(r'<li><a href="https://github\.com/Hunterdii/[^"]*"[^>]*>.*?</a></li>\s*', '', content)

# Replace any remaining Hunterdii GitHub links with FOUNDER_NAME/SOCIAL_LINKS 
content = content.replace("https://github.com/Hunterdii/Smart-AI-Resume-Analyzer", "{SOCIAL_LINKS['github']}")
content = content.replace("mailto:hunterdii9879@gmail.com", "{SOCIAL_LINKS.get('email', '#')}")

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)
