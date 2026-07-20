"""Privacy policy content for the Smart Resume AI application."""

from config.branding import APP_NAME, FOUNDER_NAME

PRIVACY_LAST_UPDATED = "July 4, 2026"

PRIVACY_SECTIONS = [
    {
        "title": "Overview",
        "body": (
            f"{APP_NAME} helps you analyze and improve your resume. We take privacy seriously. "
            "This policy explains what data we process, when we store it, and your choices."
        ),
    },
    {
        "title": "What we collect",
        "body": (
            "**When you analyze or build a resume (default):** Your file is processed in memory to produce "
            "results. We do **not** save your resume, contact details, or analysis to our database unless "
            "you explicitly opt in.\n\n"
            "**If you opt in to save data:** We may store name, email, phone, LinkedIn, portfolio, resume "
            "content, target role, and analysis scores in a local SQLite database for platform analytics.\n\n"
            "**AI analysis:** Resume text is sent to Google Gemini when you use the AI Analyzer. See "
            "Google's terms for how they handle API data.\n\n"
            "**Feedback:** Ratings and comments you submit on the Feedback page are stored locally.\n\n"
            "**Admin usage:** Admin login events (email, action, timestamp) are logged for security."
        ),
    },
    {
        "title": "What we do not do",
        "body": (
            "- We do not sell your personal data.\n"
            "- We do not share resume content with third parties except AI providers needed to run analysis you request.\n"
            "- We do not require an account to use core features."
        ),
    },
    {
        "title": "Your choices",
        "body": (
            "- Leave the **“Save my data”** checkbox unchecked to analyze resumes without storing PII.\n"
            "- Contact the operator to request deletion of stored data.\n"
            "- Do not use the AI Analyzer if you do not want resume text sent to Google Gemini."
        ),
    },
    {
        "title": "Data retention & security",
        "body": (
            "Opt-in resume data is kept in a local database on the server running this app. Admin passwords "
            "are stored using bcrypt hashing. You are responsible for securing your deployment, API keys "
            "(`.env`), and database files in production."
        ),
    },
    {
        "title": "Contact",
        "body": (
            f"Questions about this policy? Reach out to **{FOUNDER_NAME}** through the contact links on "
            "the About page, or open an issue in the project repository."
        ),
    },
]
