with open("app.py", "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'Hunterdii' in line or 'Het Patel' in line:
        lines[i] = ""

with open("app.py", "w", encoding="utf-8") as f:
    f.writelines(lines)
