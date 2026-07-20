"""Company data and market insights for job search"""

FEATURED_COMPANIES = {
    "tech": [
        {
            "name": "Google",
            "icon": "fab fa-google",
            "color": "#4285F4",
            "careers_url": "https://careers.google.com",
            "description": "Leading technology company known for search, cloud, and innovation",
            "categories": ["Software", "AI/ML", "Cloud", "Data Science"]
        },
        {
            "name": "Microsoft",
            "icon": "fab fa-microsoft",
            "color": "#00A4EF",
            "careers_url": "https://careers.microsoft.com",
            "description": "Global leader in software, cloud, and enterprise solutions",
            "categories": ["Software", "Cloud", "Gaming", "Enterprise"]
        },
        {
            "name": "Amazon",
            "icon": "fab fa-amazon",
            "color": "#FF9900",
            "careers_url": "https://www.amazon.jobs",
            "description": "E-commerce and cloud computing giant",
            "categories": ["Software", "Operations", "Cloud", "Retail"]
        },
        {
            "name": "Apple",
            "icon": "fab fa-apple",
            "color": "#555555",
            "careers_url": "https://www.apple.com/careers",
            "description": "Innovation leader in consumer technology",
            "categories": ["Software", "Hardware", "Design", "AI/ML"]
        },
        {
            "name": "Facebook",
            "icon": "fab fa-facebook",
            "color": "#1877F2",
            "careers_url": "https://www.metacareers.com/",
            "description": "Social media and technology company",
            "categories": ["Software", "Marketing", "Networking", "AI/ML"]
        },
        {
            "name": "Netflix",
            "icon": "fas fa-play-circle",
            "color": "#E50914",
            "careers_url": "https://explore.jobs.netflix.net/careers",
            "description": "Streaming media company",
            "categories": ["Software", "Marketing", "Design", "Service"],
            "logo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Netflix_2015_logo.svg/1920px-Netflix_2015_logo.svg.png",
            "website": "https://jobs.netflix.com/",
            "industry": "Entertainment & Technology"
        }
    ],
    "regional_tech": [
        {
            "name": "Vermeg",
            "icon": "fas fa-building",
            "color": "#0070C0",
            "careers_url": "https://www.vermeg.com/careers/",
            "description": "Software solutions for banking, wealth and insurance",
            "categories": ["FinTech", "Software", "Consulting"]
        },
        {
            "name": "SOFRECOM",
            "icon": "fas fa-building",
            "color": "#FF7900",
            "careers_url": "https://www.sofrecom.com/en/careers",
            "description": "IT and telecom consulting and engineering",
            "categories": ["Telecom", "Consulting", "Engineering"]
        },
        {
            "name": "Capgemini",
            "icon": "fas fa-building",
            "color": "#0070AD",
            "careers_url": "https://www.capgemini.com/careers/",
            "description": "Global leader in consulting, technology services and digital transformation",
            "categories": ["IT Services", "Consulting", "Digital"]
        },
        {
            "name": "Orange",
            "icon": "fas fa-building",
            "color": "#FF7900",
            "careers_url": "https://orange.jobs/",
            "description": "Major telecommunications operator",
            "categories": ["Telecom", "Digital", "IT Services"]
        }
    ],
    "global_corps": [
        {
            "name": "IBM",
            "icon": "fas fa-server",
            "color": "#1F70C1",
            "careers_url": "https://www.ibm.com/careers",
            "description": "Global leader in technology and consulting",
            "categories": ["Software", "Consulting", "AI/ML", "Cloud"],
            "logo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/IBM_logo.svg/1920px-IBM_logo.svg.png",
            "website": "https://www.ibm.com/careers/",
            "industry": "Technology & Consulting"
        },
        {
            "name": "Accenture",
            "icon": "fas fa-building",
            "color": "#A100FF",
            "careers_url": "https://www.accenture.com/careers",
            "description": "Global professional services company",
            "categories": ["Consulting", "Technology", "Digital"]
        },
        {
            "name": "Cognizant",
            "icon": "fas fa-building",
            "color": "#1299D8",
            "careers_url": "https://careers.cognizant.com",
            "description": "Leading professional services company",
            "categories": ["IT Services", "Consulting", "Digital"]
        }
    ]
}

JOB_MARKET_INSIGHTS = {
    "trending_skills": [
        {"name": "Artificial Intelligence", "growth": "+45%", "icon": "fas fa-brain"},
        {"name": "Cloud Computing", "growth": "+38%", "icon": "fas fa-cloud"},
        {"name": "Data Science", "growth": "+35%", "icon": "fas fa-chart-line"},
        {"name": "Cybersecurity", "growth": "+32%", "icon": "fas fa-shield-alt"},
        {"name": "DevOps", "growth": "+30%", "icon": "fas fa-code-branch"},
        {"name": "Machine Learning", "growth": "+28%", "icon": "fas fa-robot"},
        {"name": "Blockchain", "growth": "+25%", "icon": "fas fa-lock"},
        {"name": "Big Data", "growth": "+23%", "icon": "fas fa-database"},
        {"name": "Internet of Things", "growth": "+21%", "icon": "fas fa-wifi"}
    ],
    "top_locations": [
        {"name": "Tunis", "jobs": "15,000+", "icon": "fas fa-city"},
        {"name": "Paris", "jobs": "45,000+", "icon": "fas fa-city"},
        {"name": "Lyon", "jobs": "25,000+", "icon": "fas fa-city"},
        {"name": "Sfax", "jobs": "8,000+", "icon": "fas fa-city"},
        {"name": "Marseille", "jobs": "15,000+", "icon": "fas fa-city"},
        {"name": "Sousse", "jobs": "5,000+", "icon": "fas fa-city"},
        {"name": "Toulouse", "jobs": "12,000+", "icon": "fas fa-city"},
        {"name": "Ariana", "jobs": "4,000+", "icon": "fas fa-city"},
        {"name": "Nice", "jobs": "8,000+", "icon": "fas fa-city"},
        {"name": "Remote", "jobs": "30,000+", "icon": "fas fa-globe-americas"},
    ],
    "salary_insights": [
        {"role": "Machine Learning Engineer", "range": "50k-120k", "experience": "0-5 years"},
        {"role": "Big Data Engineer", "range": "40k-100k", "experience": "0-5 years"},
        {"role": "Software Engineer", "range": "30k-90k", "experience": "0-5 years"},
        {"role": "Data Scientist", "range": "40k-100k", "experience": "0-5 years"},
        {"role": "DevOps Engineer", "range": "35k-95k", "experience": "0-5 years"},
        {"role": "UI/UX Designer", "range": "30k-80k", "experience": "0-5 years"},
        {"role": "Full Stack Developer", "range": "40k-100k", "experience": "0-5 years"},
        {"role": "C++/C#/Python/Java Developer", "range": "30k-85k", "experience": "0-5 years"},
        {"role": "Django Developer", "range": "35k-90k", "experience": "0-5 years"},
        {"role": "Cloud Engineer", "range": "35k-95k", "experience": "0-5 years"},
        {"role": "Google Cloud/AWS/Azure Engineer", "range": "35k-95k", "experience": "0-5 years"},
        {"role": "Salesforce Engineer", "range": "35k-95k", "experience": "0-5 years"},
    ]
}

def get_featured_companies(category=None):
    """Get featured companies, optionally filtered by category"""
    if category and category in FEATURED_COMPANIES:
        return FEATURED_COMPANIES[category]
    return [company for companies in FEATURED_COMPANIES.values() for company in companies]

def get_market_insights():
    """Get job market insights"""
    return JOB_MARKET_INSIGHTS

def get_company_info(company_name):
    """Get company information by name"""
    for companies in FEATURED_COMPANIES.values():
        for company in companies:
            if company["name"] == company_name:
                return company
    return None

def get_companies_by_industry(industry):
    """Get list of companies by industry"""
    companies = []
    for companies_list in FEATURED_COMPANIES.values():
        for company in companies_list:
            if "industry" in company and company["industry"] == industry:
                companies.append(company)
    return companies