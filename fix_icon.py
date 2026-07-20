import re

with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

# Remove icon argument from page_header calls
# e.g., page_header("Resume Builder", "Create an ATS-friendly resume in minutes", icon="??") -> page_header("Resume Builder", "Create an ATS-friendly resume in minutes")
content = re.sub(r'page_header\((.*?),\s*icon="[^"]*"\)', r'page_header(\1)', content)

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)
