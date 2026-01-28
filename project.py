import sys
import time
import json
import os
import urllib.request

# ---------------- GLOBAL DATA ----------------

user_profile = {}
visa_scores = {}
history_log = {}
financial_plan = {}

DATA_FILE = "data.json"

CONSULTANT_NOTE = """
DISCLAIMER:
This system provides decision-support guidance based on
official immigration policies and Pakistani applicant trends.
Final visa decisions are made by embassy authorities only.
"""

# ---------------- UTILITIES ----------------

def slow_print(text, delay=0.002):
    for c in text:
        print(c, end="", flush=True)
        time.sleep(delay)
    print()

def separator():
    print("=" * 90)

def pause():
    input("\nPress Enter to continue...")

def get_pkr_to_usd_rate():
    try:
        with urllib.request.urlopen("https://open.er-api.com/v6/latest/PKR") as response:
            data = json.loads(response.read())
            return data['rates']['USD']
    except:
        return 0.0036  # fallback

# ---------------- DATA STORAGE ----------------

def save_data():
    data = {
        "user_profile": user_profile,
        "visa_scores": visa_scores,
        "history_log": history_log,
        "financial_plan": financial_plan
    }
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_data():
    if not os.path.exists(DATA_FILE):
        return False
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
        user_profile.update(data.get("user_profile", {}))
        visa_scores.update(data.get("visa_scores", {}))
        history_log.update(data.get("history_log", {}))
        financial_plan.update(data.get("financial_plan", {}))
    return True

def log_action(module, action):
    history_log.setdefault(module, []).append(action)
    save_data()

# ---------------- USER PROFILE ----------------

def collect_basic_info():
    separator()
    slow_print("PERSONAL INFORMATION (PAKISTAN)")
    separator()
    user_profile["name"] = input("Full Name: ")
    user_profile["dob"] = input("Date of Birth (DD-MM-YYYY): ")
    user_profile["nationality"] = "Pakistani"
    user_profile["marital"] = input("Marital Status: ")
    log_action("profile", "Basic info collected")

def collect_education():
    separator()
    slow_print("EDUCATION DETAILS")
    separator()
    user_profile["qualification"] = input("Highest Qualification: ")
    user_profile["field"] = input("Field of Study: ")
    user_profile["marks"] = float(input("Marks Percentage: "))
    user_profile["year"] = int(input("Graduation Year: "))
    log_action("profile", "Education recorded")

def collect_work():
    separator()
    slow_print("WORK EXPERIENCE")
    separator()
    user_profile["experience"] = int(input("Years of Experience: "))
    user_profile["occupation"] = input("Occupation: ")
    log_action("profile", "Work experience recorded")

def collect_language():
    separator()
    slow_print("LANGUAGE (IELTS)")
    separator()
    user_profile["ielts"] = float(input("IELTS Overall Band (0-9): "))
    log_action("profile", "IELTS recorded")

def collect_finances():
    separator()
    slow_print("FINANCIAL INFORMATION (PAKISTAN)")
    separator()
    rate = get_pkr_to_usd_rate()
    user_profile["monthly_income"] = float(input("Monthly Income (PKR): ")) * rate
    user_profile["savings"] = float(input("Total Savings (PKR): ")) * rate
    user_profile["liabilities"] = float(input("Liabilities (PKR): ")) * rate
    log_action("profile", "Financials converted PKR→USD")

# ---------------- SCORING ----------------

def education_score():
    m = user_profile["marks"]
    return 30 if m >= 85 else 20 if m >= 70 else 10

def experience_score():
    e = user_profile["experience"]
    return 30 if e >= 8 else 20 if e >= 4 else 10

def language_score():
    b = user_profile["ielts"]
    return 20 if b >= 8 else 15 if b >= 7 else 10 if b >= 6 else 5

def base_score():
    return education_score() + experience_score() + language_score()

# ---------------- COUNTRY SYSTEM ----------------

def canada_points():
    visa_scores["Canada"] = base_score() + 10
    return visa_scores["Canada"]

def australia_points():
    visa_scores["Australia"] = base_score() + 5
    return visa_scores["Australia"]

def germany_points():
    score = education_score() + experience_score()
    if "engineering" in user_profile["field"].lower():
        score += 15
    visa_scores["Germany"] = score
    return score

def uk_points():
    visa_scores["UK"] = base_score()
    return visa_scores["UK"]

def uae_points():
    visa_scores["UAE"] = experience_score() + 10
    return visa_scores["UAE"]

# ---------------- PROFESSIONAL MODULES ----------------

def skilled_immigration():
    separator()
    slow_print("SKILLED IMMIGRATION ASSESSMENT")
    separator()

    canada_points()
    australia_points()
    germany_points()
    uk_points()
    uae_points()

    for c, p in visa_scores.items():
        slow_print(f"{c}: {p} points")

    log_action("skilled", "Skilled immigration evaluated")
    pause()

def ai_recommendation():
    separator()
    slow_print("AI CONSULTANT RECOMMENDATION")
    separator()

    ranked = sorted(visa_scores.items(), key=lambda x: x[1], reverse=True)
    for i, (c, s) in enumerate(ranked, 1):
        slow_print(f"Rank {i}: {c} (Score: {s})")

    slow_print(f"\nBest Option for Pakistani Applicant: {ranked[0][0]}")
    log_action("ai", "AI recommendation generated")
    pause()

def rejection_analysis():
    separator()
    slow_print("PAKISTAN VISA REJECTION RISK")
    separator()

    risks = []
    if user_profile["ielts"] < 6:
        risks.append("Low IELTS")
    if user_profile["monthly_income"] < 400:
        risks.append("Weak financial proof")
    if user_profile["experience"] < 2:
        risks.append("Low work experience")

    if not risks:
        slow_print("Low rejection risk detected")
    else:
        slow_print("Possible rejection reasons:")
        for r in risks:
            slow_print(f"- {r}")

    log_action("risk", "Rejection risk analyzed")
    pause()

def document_checklist():
    separator()
    slow_print("PAKISTAN DOCUMENT CHECKLIST")
    separator()
    docs = [
        "Passport (6+ months validity)",
        "NADRA CNIC",
        "HEC Attested Degrees",
        "IELTS TRF",
        "6-Month Bank Statement",
        "Police Clearance",
        "Medical (Embassy Approved)"
    ]
    for d in docs:
        slow_print(f"- {d}")
    log_action("docs", "Checklist generated")
    pause()

def official_resources():
    separator()
    slow_print("OFFICIAL GOVERNMENT WEBSITES")
    separator()
    slow_print("Canada: https://www.canada.ca/immigration")
    slow_print("UK: https://www.gov.uk/immigration")
    slow_print("Australia: https://immi.homeaffairs.gov.au")
    slow_print("Germany: https://www.make-it-in-germany.com")
    slow_print("IELTS: https://www.ielts.org")
    slow_print("HEC Pakistan: https://www.hec.gov.pk")
    slow_print("NADRA: https://www.nadra.gov.pk")
    pause()

# ---------------- MENU ----------------

def menu():
    separator()
    print("1. Skilled Immigration Assessment")
    print("2. AI Recommendation")
    print("3. Rejection Risk Analysis")
    print("4. Document Checklist")
    print("5. Official Resources")
    print("0. Exit")
    return input("Select Option: ")

# ---------------- MAIN ----------------

def main():
    separator()
    slow_print("PROFESSIONAL IMMIGRATION SUPPORT SYSTEM (PAKISTAN)")
    separator()
    slow_print(CONSULTANT_NOTE)

    if not load_data():
        collect_basic_info()
        collect_education()
        collect_work()
        collect_language()
        collect_finances()

    while True:
        c = menu()
        if c == "1": skilled_immigration()
        elif c == "2": ai_recommendation()
        elif c == "3": rejection_analysis()
        elif c == "4": document_checklist()
        elif c == "5": official_resources()
        elif c == "0":
            slow_print("Session Ended")
            sys.exit()
        else:
            slow_print("Invalid option")

if __name__ == "__main__":
    main()

