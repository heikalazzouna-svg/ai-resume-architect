# Smart Resume AI 🚀

A next-generation, AI-powered platform designed to optimize resumes and showcase your true potential. Built with a custom glassmorphic UI, dynamic SaaS navigation, and advanced Gemini AI analysis.

> **Built by a student, for students.** — *The Tunisia Tech Career Lab 🇹🇳*

---

## 📸 Platform Previews

<!-- To add your images, upload them to your GitHub repo, then replace the placeholder links below with the actual paths (e.g., docs/dashboard.png) -->

<img width="1363" height="722" alt="image" src="https://github.com/user-attachments/assets/f24ef400-4dc5-44c6-9106-078351d6fb73" />


<img width="1298" height="711" alt="image" src="https://github.com/user-attachments/assets/c810fde8-3761-4251-828b-2cdc8223f35a" />


---

## ✨ Key Features
- **Elite Modern UI:** A fully custom, dark-themed glassmorphic design system overriding default layouts for a premium SaaS experience.
- **Sleek Dynamic Sidebar:** Grouped navigation, glowing active states, and custom Lucide-style icons natively injected via CSS.
- **AI-Powered Analysis:** Gemini-backed insights tailored specifically to tech job roles (ATS scoring, skill gap analysis, and tailored recommendations).
- **Auto Resume Builder:** Generate professionally formatted DOCX resumes dynamically from your analysis data.
- **Privacy First:** Strict opt-in consent flow ensuring your resume data is handled exclusively in-memory unless saved locally by choice.

## 🛠️ Architecture & Tech Stack
- **Frontend Framework:** Streamlit (Python)
- **Styling Engine:** Custom CSS Token Architecture (`style.css` + `ui_components.py`)
- **AI Engine:** Google Gemini Pro
- **Storage:** Local SQLite Database (`resume_data.db`)
- **Security:** `bcrypt` mathematically secured admin passwords

## 🚀 Getting Started (Local Development)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git
   cd YOUR-REPO-NAME
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables:**
   Create a `.env` file in the `utils/` directory based on the example provided, and add your Google Gemini API key:
   ```bash
   cp .env.example utils/.env
   ```

4. **Run the Application:**
   ```bash
   streamlit run app.py
   ```

---
_Created with ♥ by Heikal Azzouna._
