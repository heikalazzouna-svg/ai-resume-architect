import os

with open('app.py', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

# 1. Replace self.pages
start_idx = None
end_idx = None
for i, line in enumerate(lines):
    if 'self.pages = {' in line:
        start_idx = i
    if start_idx is not None and '}' in line and i > start_idx:
        end_idx = i
        break

new_pages_code = """        self.pages = {
            "Home": self.render_home,
            "Analyzer": self.render_analyzer,
            "Builder": self.render_builder,
            "Job Search": self.render_job_search,
            "Pricing": self.render_pricing,
            "FAQ": self.render_faq,
            "Testimonials": self.render_testimonials,
            "Changelog": self.render_changelog,
            "Dashboard": self.render_dashboard,
            "Feedback": self.render_feedback_page,
            "About": self.render_about
        }
"""
if start_idx and end_idx:
    lines = lines[:start_idx] + [new_pages_code] + lines[end_idx+1:]

# 2. Add methods before def main(self):
main_idx = next(i for i, line in enumerate(lines) if 'def main(self):' in line)
new_methods = """
    def render_pricing(self):
        page_header("Simple, Transparent Pricing", "Choose the plan that fits your career goals", icon="??")
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('<div class="bento-card"><h3>Basic</h3><h2>Free</h2><p>For getting started</p><ul><li>Basic Resume Analysis</li><li>1 Template</li><li>Community Support</li></ul><br><button class="stButton" style="width:100%">Current Plan</button></div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="bento-card" style="border-color: var(--accent-color);"><h3>Pro</h3><h2>$9<span style="font-size:0.5em">/mo</span></h2><p>For active job seekers</p><ul><li>AI Resume Analysis</li><li>All Templates</li><li>Cover Letter Gen</li><li>Priority Support</li></ul><br><button class="stButton" style="width:100%">Upgrade to Pro</button></div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="bento-card"><h3>Elite</h3><h2>$29<span style="font-size:0.5em">/mo</span></h2><p>For career acceleration</p><ul><li>Everything in Pro</li><li>Mock Interviews</li><li>1-on-1 Coaching</li></ul><br><button class="stButton" style="width:100%">Contact Us</button></div>', unsafe_allow_html=True)

    def render_faq(self):
        page_header("Frequently Asked Questions", "Find answers to common questions", icon="?")
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("How does the AI Resume Analyzer work?"):
            st.write("Our AI analyzes your resume against industry standards and specific job descriptions to provide a match score and actionable feedback.")
        with st.expander("Is my data secure?"):
            st.write("Yes. We use industry-standard encryption and only store your data if you explicitly opt-in.")
        with st.expander("Can I export my resume to PDF?"):
            st.write("PDF export is currently in development and will be available to all Pro users soon.")

    def render_testimonials(self):
        page_header("Success Stories", "See how we've helped others land their dream jobs", icon="??")
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="bento-card">"The AI feedback was exactly what I needed. I landed interviews at top tech companies within weeks!"<br><br><b>- Sarah J., Software Engineer</b></div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="bento-card">"The resume builder templates are clean and ATS-friendly. Highly recommended."<br><br><b>- Michael T., Product Manager</b></div>', unsafe_allow_html=True)

    def render_changelog(self):
        page_header("Changelog", "Latest updates and improvements", icon="??")
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### v1.1.0 - Identity & Polish")
        st.markdown("- Unified design tokens to premium cyan/indigo")
        st.markdown("- Added Pricing, FAQ, and Testimonial pages")
        st.markdown("- Improved Resume Builder UX")
        st.markdown("### v1.0.0 - Initial Release")
        st.markdown("- Basic Resume Analysis")
        st.markdown("- Resume Builder")

"""
lines.insert(main_idx, new_methods)

# 3. Modify render_builder
builder_idx = next(i for i, line in enumerate(lines) if 'def render_builder(self):' in line)
for i in range(builder_idx, min(builder_idx + 20, len(lines))):
    if 'st.title' in lines[i] and 'Resume Builder' in lines[i]:
        lines[i] = '        page_header("Resume Builder", "Create an ATS-friendly resume in minutes", icon="??")\n'
    if 'Create a professional, ATS-friendly resume in minutes.' in lines[i]:
        lines[i] = ''

with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
