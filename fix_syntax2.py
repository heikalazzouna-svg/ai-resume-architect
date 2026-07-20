with open("app.py", "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

bad1 = """                                file_name=f"{
    current_name.replace(
        ' ', '_')}_resume.docx","""
good1 = """                                file_name=f"{current_name.replace(' ', '_')}_resume.docx","""

bad2 = """                            print(
    f"Warning: Failed to save to database: {
        str(db_error)}")"""
good2 = """                            print(f"Warning: Failed to save to database: {str(db_error)}")"""

content = content.replace(bad1, good1).replace(bad2, good2)

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)
