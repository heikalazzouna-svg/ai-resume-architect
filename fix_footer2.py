with open("app.py", "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

import re

# Remove the Star this repo HTML block
star_pattern = r'# Add GitHub star button\s*st\.markdown\("""\s*<div style=\'display: flex; justify-content: center;.*?</svg>\s*<span style=\'color: white; font-size: 14px;\'>Star this repo</span>\s*</div>\s*</a>\s*</div>\s*""", unsafe_allow_html=True\)'
content = re.sub(star_pattern, '', content, flags=re.DOTALL)

# Fix corrupted lock emoji
content = content.replace("?? <strong>Privacy First:", "&#128274; <strong>Privacy First:")

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)
