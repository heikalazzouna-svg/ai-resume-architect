import glob
import re

for filepath in glob.glob("app_pages/*.py"):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    print(f"\n--- {filepath} ---")
    
    # Check for apply_modern_styles
    if "apply_modern_styles(" in content and "apply_modern_styles" not in content[:content.find("def ")]:
        print("MISSING: apply_modern_styles")
        
    # Check for feature_card
    if "feature_card(" in content and "feature_card" not in content[:content.find("def ")]:
        print("MISSING: feature_card")
        
    # Check for render_job_search
    if "render_job_search(" in content and "render_job_search" not in content[:content.find("def ")]:
        print("MISSING: render_job_search")
        
    # Check for FeedbackManager
    if "FeedbackManager(" in content and "FeedbackManager" not in content[:content.find("def ")]:
        print("MISSING: FeedbackManager")
        
    # Check for any other obvious ones (render_feedback, render_activity_section, etc)
    functions = ["render_feedback", "render_activity_section", "render_analytics_section", "render_suggestions_section", "st_lottie", "load_lottie_url"]
    for func in functions:
        if f"{func}(" in content and func not in content[:content.find("def ")]:
            print(f"MISSING: {func}")

