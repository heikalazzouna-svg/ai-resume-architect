import os

# 1. Update config/branding.py
with open("config/branding.py", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace('"https://linkedin.com/in/heikal-azzouna"', '"https://www.linkedin.com/in/heikal-azzouna-8a379338b/"')

with open("config/branding.py", "w", encoding="utf-8") as f:
    f.write(content)

# 2. Update app_pages/about.py
with open("app_pages/about.py", "r", encoding="utf-8") as f:
    about_content = f.read()

# Fix image path and name
about_content = about_content.replace('"assets",\n "124852522.jpeg"', '"..",\n "assets",\n "heikal.png"')

# Remove old developer link and email link entirely, keeping only the dynamic linkedin one
old_links_block = """                <a href="https://www.linkedin.com/in/patel-hetkumar-sandipbhai-8b110525a/" class="social-link" target="_blank">
                    <i class="fab fa-linkedin"></i>
                </a>
                <a href="{SOCIAL_LINKS.get('email', '#')}" class="social-link" target="_blank">
                    <i class="fas fa-envelope"></i>
                </a>"""
about_content = about_content.replace(old_links_block, "")

# The file might have different spacing so let's use a regex or string replacement that works
import re
about_content = re.sub(r'<a href="https://www.linkedin.com/in/patel-hetkumar-sandipbhai-8b110525a/".*?</a>', '', about_content, flags=re.DOTALL)
about_content = re.sub(r'<a href="\{SOCIAL_LINKS\.get\(\'email\', \'#\'\)\}".*?</a>', '', about_content, flags=re.DOTALL)

with open("app_pages/about.py", "w", encoding="utf-8") as f:
    f.write(about_content)

print("Fixes applied.")
