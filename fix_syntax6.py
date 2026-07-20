with open("app.py", "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'document_type' in line and 'This appears to be' in lines[i-1]:
        # Cleanly build the merged line
        merged = f"                            st.error(f\"\u26A0\uFE0F This appears to be a {{analysis['document_type']}} document, not a resume!\")\n"
        lines[i-1] = merged
        lines[i] = ""
        lines[i+1] = ""

with open("app.py", "w", encoding="utf-8") as f:
    f.writelines(lines)
