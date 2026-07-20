import re

with open("app.py", "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

# Replace multiline f-string brackets
# f" ... { \n ... \n } ... "
pattern = r'f"([^"]*?)\{\s*\n\s*([^}\n]*?)\s*\n\s*\}'
content = re.sub(pattern, r'f"\1{\2}', content)

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)
