# Fix home.py
with open("app_pages/home.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "from ui_components import" in line and "apply_modern_styles" in line:
        if "feature_card" not in line:
            lines[i] = line.strip() + ", feature_card\n"
        break
with open("app_pages/home.py", "w", encoding="utf-8") as f:
    f.writelines(lines)

# Fix job_search.py
with open("app_pages/job_search.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
# insert after first line
lines.insert(1, "from jobs.job_search import render_job_search\n")
with open("app_pages/job_search.py", "w", encoding="utf-8") as f:
    f.writelines(lines)

# Fix feedback_page.py
with open("app_pages/feedback_page.py", "r", encoding="utf-8") as f:
    lines = f.readlines()
lines.insert(1, "from feedback.feedback import FeedbackManager\n")
with open("app_pages/feedback_page.py", "w", encoding="utf-8") as f:
    f.writelines(lines)

print("Fixed imports")
