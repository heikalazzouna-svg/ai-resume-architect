with open("app.py", "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'document_type' in line and 'This appears to be' in lines[i-1]:
        # Merge i-1, i, i+1
        merged = lines[i-1].strip() + " " + lines[i].strip() + " " + lines[i+1].strip()
        merged = merged.replace('st.error( f"', 'st.error(f"').replace('} document, not a resume!")', '} document, not a resume!")\n')
        lines[i-1] = "                            " + merged
        lines[i] = ""
        lines[i+1] = ""

with open("app.py", "w", encoding="utf-8") as f:
    f.writelines(lines)
