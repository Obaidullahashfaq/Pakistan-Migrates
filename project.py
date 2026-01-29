import sys
import time
from datetime import datetime

# ================= GLOBAL DATA =================
user_profile = {}

CONSULTANT_NOTE = """
DISCLAIMER:
This system provides decision-support guidance based on
official immigration policies and Pakistani applicant trends.
Final visa decisions are made by embassy authorities only.
"""

IN_DEMAND_PROFESSIONS = [
    "engineer", "doctor", "it", "software", "developer",
    "nurse", "accountant", "electrician", "technician"
]

PROVINCE_BONUS = {
    "ontario": 10, "british columbia": 10, "alberta": 15, "saskatchewan": 20, "manitoba": 20,
    "nova scotia": 15, "new south wales": 10, "victoria": 10, "queensland": 15,
    "south australia": 20, "tasmania": 25
}

EU_COUNTRIES = ["germany","france","netherlands","sweden","norway","denmark","spain","italy","belgium"]

VISA_SUBCLASSES = {
    "canada": ["Express Entry - Federal Skilled Worker", "Provincial Nominee Program", "Canadian Experience Class"],
    "australia": ["Skilled Independent", "Skilled Nominated", "Employer Sponsored"],
    "uk": ["Skilled Worker", "Global Talent"],
    "usa": ["H1B", "EB2", "EB3"],
    "germany": ["EU Blue Card", "Job Seeker Visa"],
    "uae": ["Professional Visa", "Investor Visa"]
}

OFFICIAL_WEBSITES = {
    "canada": "https://www.canada.ca/en/immigration-refugees-citizenship.html",
    "australia": "https://immi.homeaffairs.gov.au/",
    "uk": "https://www.gov.uk/browse/visas-immigration",
    "usa": "https://www.uscis.gov/",
    "uae": "https://u.ae/en/information-and-services/visa-and-emirates-id",
    "germany": "https://www.make-it-in-germany.com/en/",
    "france": "https://france-visas.gouv.fr/",
    "netherlands": "https://ind.nl/en",
    "sweden": "https://www.migrationsverket.se/English.html",
    "norway": "https://www.udi.no/en/",
    "denmark": "https://www.nyidanmark.dk/en-GB",
    "spain": "https://www.exteriores.gob.es/en/ServiciosAlCiudadano/Paginas/inicio.aspx",
    "italy": "https://vistoperitalia.esteri.it/home/en",
    "belgium": "https://dofi.ibz.be/en/themes/immigration"
}

DOCUMENT_CHECKLIST = {
    "general": [
        "Passport (valid at least 6 months)",
        "Educational transcripts and degree certificates",
        "Work experience letters",
        "IELTS / Language Test Score",
        "Marriage certificate (if married)",
        "Birth certificates of children (if any)",
        "Proof of funds"
    ]
}

# ================= UTILITIES =================
def slow_print(text, delay=0.001):
    for c in text:
        print(c, end="", flush=True)
        time.sleep(delay)
    print()

def separator():
    print("="*120)

def pause():
    input("\nPress Enter to continue...")

def safe_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except:
            print("❌ Enter a valid number")

def safe_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except:
            print("❌ Enter a valid number")

def get_valid_dob():
    while True:
        dob = input("Date of Birth (DD-MM-YYYY): ")
        try:
            datetime.strptime(dob, "%d-%m-%Y")
            return dob
        except:
            print("❌ Invalid date format. Use DD-MM-YYYY")

def calculate_age(dob):
    birth = datetime.strptime(dob, "%d-%m-%Y")
    today = datetime.today()
    return today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))

# ================= USER INPUT =================
def collect_user_data():
    separator()
    slow_print("GLOBAL IMMIGRATION INPUT FORM (PAKISTAN)")
    separator()
    user_profile["name"] = input("Full Name: ")
    user_profile["dob"] = get_valid_dob()
    user_profile["age"] = calculate_age(user_profile["dob"])
    user_profile["marital"] = input("Marital Status (Single/Married): ").lower()
    if user_profile["marital"] == "married":
        user_profile["spouse_age"] = safe_int("Spouse Age: ")
        user_profile["spouse_profession"] = input("Spouse Profession: ").lower()
        user_profile["children"] = safe_int("Number of Children: ")
    else:
        user_profile["spouse_age"] = 0
        user_profile["spouse_profession"] = ""
        user_profile["children"] = 0
    user_profile["marks"] = safe_float("Marks Percentage: ")
    user_profile["qualification"] = input("Highest Qualification (Bachelors/Masters/PhD): ").lower()
    user_profile["experience"] = safe_int("Years of Experience: ")
    user_profile["occupation"] = input("Occupation: ").lower()
    user_profile["ielts"] = safe_float("IELTS Overall Band (0-9): ")
    user_profile["province"] = input("Preferred Province/State (e.g. Ontario, Alberta, Victoria): ").strip().lower()

# ================= SCORING FUNCTIONS =================
def age_score():
    a=user_profile["age"]
    return 30 if 18<=a<=29 else 25 if a<=34 else 20 if a<=39 else 10 if a<=44 else 0

def education_score():
    m=user_profile["marks"]
    return 30 if m>=85 else 20 if m>=70 else 10

def experience_score():
    e=user_profile["experience"]
    return 30 if e>=8 else 20 if e>=4 else 10

def language_score():
    b=user_profile["ielts"]
    return 20 if b>=8 else 15 if b>=7 else 10 if b>=6 else 5

def spouse_score():
    s=0
    if user_profile["spouse_age"] !=0 and user_profile["spouse_age"]<=35:
        s+=10
    if any(p in user_profile["spouse_profession"] for p in IN_DEMAND_PROFESSIONS):
        s+=10
    return s

def children_penalty():
    c=user_profile["children"]
    return 0 if c<=1 else -5 if c<=3 else -10

def province_score():
    return PROVINCE_BONUS.get(user_profile["province"],0)

# ================= COUNTRY SCORING =================
def canada_score(): return age_score()+education_score()+language_score()*2+experience_score()+spouse_score()+children_penalty()+province_score()
def australia_score(): return age_score()+education_score()+experience_score()*2+language_score()+spouse_score()+children_penalty()+province_score()
def uk_score(): return age_score()+education_score()+language_score()+experience_score()+spouse_score()+children_penalty()
def germany_score():
    score = age_score()+education_score()+experience_score()+language_score()
    if "engineer" in user_profile["occupation"] or "it" in user_profile["occupation"]:
        score +=15
    return score
def usa_score():
    score = age_score()+education_score()+experience_score()+language_score()
    if "it" in user_profile["occupation"] or "developer" in user_profile["occupation"]:
        score +=10
    return score
def uae_score(): return age_score()+experience_score()+language_score()
def europe_scores():
    scores={}
    for c in EU_COUNTRIES:
        score=age_score()+education_score()+experience_score()+language_score()
        if "engineer" in user_profile["occupation"] or "developer" in user_profile["occupation"]:
            score+=10
        scores[c]=score
    return scores

# ================= ELIGIBILITY =================
def eligibility_reasons(score,country):
    reasons=[]
    if score<40: reasons.append("Low overall score")
    if user_profile["ielts"]<6 and country in ["canada","australia","uk"]: reasons.append("Low language score")
    if user_profile["experience"]<2 and country in ["canada","australia","usa"]: reasons.append("Insufficient experience")
    return reasons if reasons else ["Eligible based on provided data"]

# ================= DISPLAY =================
def show_country_table():
    separator()
    print(f"{'Country':<20}{'Score':<8}{'Visa Subclass':<40}{'Official Website':<40}{'Eligibility Notes'}")
    print("-"*160)
    
    countries=["Canada","Australia","UK","Germany","USA","UAE"]
    scores=[canada_score(), australia_score(), uk_score(), germany_score(), usa_score(), uae_score()]
    for c,s in zip(countries,scores):
        subclass = ", ".join(VISA_SUBCLASSES.get(c.lower(), []))
        website = OFFICIAL_WEBSITES.get(c.lower(), "N/A")
        notes = "; ".join(eligibility_reasons(s, c.lower()))
        print(f"{c:<20}{s:<8}{subclass:<40}{website:<40}{notes}")
    
    eu = europe_scores()
    for c,s in eu.items():
        subclass="EU Blue Card / Job Seeker"
        website=OFFICIAL_WEBSITES.get(c.lower(), "N/A")
        notes="; ".join(eligibility_reasons(s, c.lower()))
        print(f"{c.title():<20}{s:<8}{subclass:<40}{website:<40}{notes}")
    
    separator()
    print("\n📋 General Document Checklist:")
    for doc in DOCUMENT_CHECKLIST["general"]:
        print(f" - {doc}")
    pause()

# ================= VISUAL & AI =================
def ascii_chart_all():
    separator()
    countries=["Canada","Australia","UK","Germany","USA","UAE"] + EU_COUNTRIES
    scores=[canada_score(), australia_score(), uk_score(), germany_score(), usa_score(), uae_score()] + list(europe_scores().values())
    for c,s in zip(countries,scores):
        bar='█'*(s//5)
        print(f"{c:<12}: {bar} {s}")
    pause()

def ai_recommendation():
    separator()
    all_scores={"Canada":canada_score(),"Australia":australia_score(),"UK":uk_score(),"Germany":germany_score(),"USA":usa_score(),"UAE":uae_score()}
    all_scores.update(europe_scores())
    ranked=sorted(all_scores.items(), key=lambda x:x[1], reverse=True)
    print("=== Recommended Countries (Highest Score First) ===")
    for i,(c,s) in enumerate(ranked,1):
        print(f"{i}. {c.title()} - {s} points")
    pause()

# ================= MENU =================
def menu():
    separator()
    print("1. View Country-wise Scores, Eligibility & Documents")
    print("2. Visual Score Chart")
    print("3. AI-style Recommendation")
    print("0. Exit")
    return input("Select Option: ")

# ================= MAIN =================
def main():
    separator()
    slow_print("GLOBAL IMMIGRATION SUPPORT SYSTEM (PAKISTANI APPLICANT)")
    separator()
    slow_print(CONSULTANT_NOTE)
    collect_user_data()
    while True:
        choice = menu()
        if choice=="1": show_country_table()
        elif choice=="2": ascii_chart_all()
        elif choice=="3": ai_recommendation()
        elif choice=="0": print("Session Ended"); sys.exit()
        else: print("Invalid option")

if __name__=="__main__":
    main()

