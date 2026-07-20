with open("app_clean.py", "r", encoding="utf-8") as f:
    content = f.read()

imports = """
from pages import home, analyzer, builder, about, pricing, faq, testimonials, changelog, job_search, feedback_page
"""

content = content.replace("class ResumeApp:", imports + "\nclass ResumeApp:")

# Replace the self.pages routing
routing_old = """        self.pages = {
            "Home": self.render_home,
            "Resume Analyzer": self.render_analyzer,
            "Resume Builder": self.render_builder,
            "Dashboard": self.render_dashboard,
            "Job Search": self.render_job_search,
            "Feedback": self.render_feedback_page,
            "About": self.render_about,
            "Pricing": self.render_pricing,
            "FAQ": self.render_faq,
            "Testimonials": self.render_testimonials,
            "Changelog": self.render_changelog
        }"""

routing_new = """        self.pages = {
            "Home": lambda: home.render(self),
            "Resume Analyzer": lambda: analyzer.render(self),
            "Resume Builder": lambda: builder.render(self),
            "Dashboard": self.render_dashboard,
            "Job Search": lambda: job_search.render(self),
            "Feedback": lambda: feedback_page.render(self),
            "About": lambda: about.render(self),
            "Pricing": lambda: pricing.render(self),
            "FAQ": lambda: faq.render(self),
            "Testimonials": lambda: testimonials.render(self),
            "Changelog": lambda: changelog.render(self)
        }"""

content = content.replace(routing_old, routing_new)

with open("app_clean.py", "w", encoding="utf-8") as f:
    f.write(content)
