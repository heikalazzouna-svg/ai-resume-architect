import glob

for filepath in glob.glob("pages/*.py"):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    content = content.replace("from utils.resume_parser import extract_text_from_pdf, extract_text_from_docx", "from utils.resume_parser import ResumeParser")
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
