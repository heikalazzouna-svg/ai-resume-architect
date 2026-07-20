"""Module containing job-related data and configurations"""

# Job titles and skills suggestions
JOB_SUGGESTIONS = [
    {"text": "Software Engineer", "icon": "💻"},
    {"text": "Full Stack Developer", "icon": "🔧"},
    {"text": "Data Scientist", "icon": "📊"},
    {"text": "Product Manager", "icon": "📱"},
    {"text": "DevOps Engineer", "icon": "⚙️"},
    {"text": "UI/UX Designer", "icon": "🎨"},
    {"text": "Python Developer", "icon": "🐍"},
    {"text": "Java Developer", "icon": "☕"},
    {"text": "React Developer", "icon": "⚛️"},
    {"text": "Machine Learning Engineer", "icon": "🤖"},
    {"text": "Backend Developer", "icon": "🖧"},
    {"text": "Frontend Developer", "icon": "🎨"},
    {"text": "Node.js Developer", "icon": "🌿"},
    {"text": "Angular Developer", "icon": "📐"},
    {"text": "PHP Developer", "icon": "🐘"},
    {"text": "Ruby Developer", "icon": "💎"},
    {"text": "Go Developer", "icon": "🚀"},
    {"text": "C++ Developer", "icon": "🖥️"},
    {"text": "C# Developer", "icon": "🎮"},
    {"text": "Django Developer", "icon": "🛠️"},
    {"text": "Data Analyst", "icon": "📈"},
    {"text": "Big Data Engineer", "icon": "📡"},
    {"text": "Database Administrator", "icon": "🗄️"},
    {"text": "Business Intelligence Analyst", "icon": "📊"},
    {"text": "Cloud Engineer", "icon": "☁️"},
    {"text": "AWS Engineer", "icon": "☁️🔧"},
    {"text": "Azure Engineer", "icon": "☁️🖥️"},
    {"text": "Google Cloud Engineer", "icon": "☁️📡"},
    {"text": "Network Engineer", "icon": "🔌"},
    {"text": "AI Researcher", "icon": "🧠"},
    {"text": "NLP Engineer", "icon": "🗣️"},
    {"text": "Computer Vision Engineer", "icon": "👁️"},
    {"text": "Deep Learning Engineer", "icon": "🧠📚"},
    {"text": "Cybersecurity Analyst", "icon": "🔒"},
    {"text": "Ethical Hacker", "icon": "🕵️‍♂️"},
    {"text": "Security Engineer", "icon": "🛡️"},
    {"text": "Penetration Tester", "icon": "🔍"},
    {"text": "Cryptography Engineer", "icon": "🔑"},
    {"text": "Game Developer", "icon": "🎮"},
    {"text": "Embedded Systems Engineer", "icon": "🖧⚙️"},
    {"text": "Mobile App Developer", "icon": "📱"},
    {"text": "iOS Developer", "icon": "🍏"},
    {"text": "Android Developer", "icon": "🤖"},
    {"text": "Blockchain Developer", "icon": "🔗"},
    {"text": "IoT Developer", "icon": "🌐"},
    {"text": "AR/VR Developer", "icon": "🕶️"},
    {"text": "Project Manager", "icon": "📋"},
    {"text": "Technical Writer", "icon": "✍️"},
    {"text": "QA Engineer", "icon": "✅"},
    {"text": "Scrum Master", "icon": "🔄"},
    {"text": "Support Engineer", "icon": "📞"},
    {"text": "IT Consultant", "icon": "🧑‍💼"},
    {"text": "Technical Support Specialist", "icon": "🎧"}
]


# Location suggestions - organized by states/regions and major cities
LOCATION_SUGGESTIONS = [
    # Work modes
    {"text": "Remote", "icon": "🏠", "type": "work_mode"},
    {"text": "Work from Home", "icon": "🏠", "type": "work_mode"},
    {"text": "Hybrid", "icon": "🏢", "type": "work_mode"},
    
    # Major tech hubs
    {"text": "Tunis", "icon": "📍", "type": "city", "state": "Tunis Governorate"},
    {"text": "Paris", "icon": "📍", "type": "city", "state": "Île-de-France"},
    {"text": "Lyon", "icon": "📍", "type": "city", "state": "Auvergne-Rhône-Alpes"},
    {"text": "Sfax", "icon": "📍", "type": "city", "state": "Sfax Governorate"},
    {"text": "Marseille", "icon": "📍", "type": "city", "state": "Provence-Alpes-Côte d'Azur"},
    {"text": "Sousse", "icon": "📍", "type": "city", "state": "Sousse Governorate"},
    
    # Regions/Governorates
    {"text": "Tunis Governorate", "icon": "🗺️", "type": "state"},
    {"text": "Sfax Governorate", "icon": "🗺️", "type": "state"},
    {"text": "Sousse Governorate", "icon": "🗺️", "type": "state"},
    {"text": "Ariana Governorate", "icon": "🗺️", "type": "state"},
    {"text": "Île-de-France", "icon": "🗺️", "type": "state"},
    {"text": "Auvergne-Rhône-Alpes", "icon": "🗺️", "type": "state"},
    {"text": "Provence-Alpes-Côte d'Azur", "icon": "🗺️", "type": "state"},
    {"text": "Occitanie", "icon": "🗺️", "type": "state"},
    
    # Tunis Governorate cities
    {"text": "Tunis", "icon": "📍", "type": "city", "state": "Tunis Governorate"},
    {"text": "La Marsa", "icon": "📍", "type": "city", "state": "Tunis Governorate"},
    {"text": "Carthage", "icon": "📍", "type": "city", "state": "Tunis Governorate"},
    
    # Sfax Governorate cities
    {"text": "Sfax", "icon": "📍", "type": "city", "state": "Sfax Governorate"},
    {"text": "Sakiet Ezzit", "icon": "📍", "type": "city", "state": "Sfax Governorate"},
    
    # Sousse Governorate cities
    {"text": "Sousse", "icon": "📍", "type": "city", "state": "Sousse Governorate"},
    {"text": "Hammam Sousse", "icon": "📍", "type": "city", "state": "Sousse Governorate"},
    
    # Ariana Governorate cities
    {"text": "Ariana", "icon": "📍", "type": "city", "state": "Ariana Governorate"},
    {"text": "Soukra", "icon": "📍", "type": "city", "state": "Ariana Governorate"},
    
    # Île-de-France cities
    {"text": "Paris", "icon": "📍", "type": "city", "state": "Île-de-France"},
    {"text": "Boulogne-Billancourt", "icon": "📍", "type": "city", "state": "Île-de-France"},
    {"text": "Saint-Denis", "icon": "📍", "type": "city", "state": "Île-de-France"},
    
    # Auvergne-Rhône-Alpes cities
    {"text": "Lyon", "icon": "📍", "type": "city", "state": "Auvergne-Rhône-Alpes"},
    {"text": "Grenoble", "icon": "📍", "type": "city", "state": "Auvergne-Rhône-Alpes"},
    
    # Provence-Alpes-Côte d'Azur cities
    {"text": "Marseille", "icon": "📍", "type": "city", "state": "Provence-Alpes-Côte d'Azur"},
    {"text": "Nice", "icon": "📍", "type": "city", "state": "Provence-Alpes-Côte d'Azur"},
    
    # Occitanie cities
    {"text": "Toulouse", "icon": "📍", "type": "city", "state": "Occitanie"},
    {"text": "Montpellier", "icon": "📍", "type": "city", "state": "Occitanie"}
]

# Function to get cities by state
def get_cities_by_state(state_name):
    """Get list of cities for a specific state"""
    return [loc for loc in LOCATION_SUGGESTIONS if loc.get("type") == "city" and loc.get("state") == state_name]

# Function to get all states
def get_all_states():
    """Get list of all states"""
    return [loc for loc in LOCATION_SUGGESTIONS if loc.get("type") == "state"]

# Job types
JOB_TYPES = [
    {"id": "all", "text": "All Types"},
    {"id": "full-time", "text": "Full Time"},
    {"id": "part-time", "text": "Part Time"},
    {"id": "contract", "text": "Contract"},
    {"id": "internship", "text": "Internship"},
    {"id": "remote", "text": "Remote"}
]

# Experience levels
EXPERIENCE_RANGES = [
    {"id": "all", "text": "All Levels"},
    {"id": "fresher", "text": "Fresher"},
    {"id": "1-3", "text": "1-3 years"},
    {"id": "3-5", "text": "3-5 years"},
    {"id": "5-7", "text": "5-7 years"},
    {"id": "7+", "text": "7+ years"}
]

# Salary ranges
SALARY_RANGES = [
    {"id": "all", "text": "All Ranges"},
    {"id": "0-30", "text": "0-30k TND"},
    {"id": "30-60", "text": "30k-60k TND"},
    {"id": "60-100", "text": "60k-100k TND"},
    {"id": "100-150", "text": "100k-150k TND"},
    {"id": "150+", "text": "150k+ TND"}
]