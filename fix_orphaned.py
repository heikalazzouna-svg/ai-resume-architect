with open("app.py", "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

# Cleanly remove orphaned lines ending with ', icon="??")' or just spaces and that text.
for i in range(len(lines)):
    if '", icon="??")' in lines[i] and 'st.toast' not in lines[i]:
        lines[i] = ""

with open("app.py", "w", encoding="utf-8") as f:
    f.writelines(lines)
