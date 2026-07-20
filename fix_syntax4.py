with open("app.py", "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

bad1 = """                            st.error(
    f"?? This appears to be a {
        analysis['document_type']} document, not a resume!")"""
good1 = """                            st.error(f"?? This appears to be a {analysis['document_type']} document, not a resume!")"""

content = content.replace(bad1, good1)

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)
