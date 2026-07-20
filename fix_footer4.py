with open("app.py", "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

# I will find the exact block and replace it
import re

content = re.sub(r'<a href=\'\{SOCIAL_LINKS\[\'github\'\]\}\' target=\'_blank\' style=\'text-decoration: none;\'>.*?Star this repo.*?</a>', '', content, flags=re.DOTALL)

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)
