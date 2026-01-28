import sys
import time
import json
import os

user_profile = {}
visa_scores = {}
history_log = {}
financial_plan = {}


DATA_FILE = "data.json"


def slow_print(text, delay=0.003):
    for c in text:
        print(c, end="", flush=True)
        time.sleep(delay)
    print()


def separator():
    print("=" * 90)


def pause():
    input("\nPress Enter to continue...")


def save_data():
    """Save all global data structures to a JSON file."""
    data = {
        'user_profile': user_profile,
        'visa_scores': visa_scores,
        'history_log': history_log,
        'financial_plan': financial_plan
    }
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        slow_print(f"Error saving data: {e}")


def load_data():
    """Load data from JSON file if it exists."""
    global user_profile, visa_scores, history_log, financial_plan
    if not os.path.exists(DATA_FILE):
        return False

    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            user_profile.update(data.get('user_profile', {}))
            visa_scores.update(data.get('visa_scores', {}))
            history_log.update(data.get('history_log', {}))
            financial_plan.update(data.get('financial_plan', {}))
        slow_print(f"Data loaded from {DATA_FILE}")
        return True
    except Exception as e:
        slow_print(f"Error loading data: {e}")
        return False


def log_action(module, action):
    history_log.setdefault(module, []).append(action)
    save_data() 


# ---------------- USER DATA COLLECTION ----------------

def collect_basic_info():
    separator()
    slow_print("PERSONAL INFORMATION")
    separator()
    user_profile['name'] = input("Full name: ")
    user_profile['dob'] = input("Date of birth (DD-MM-YYYY): ")
    user_profile['birth_country'] = input("Country of birth: ")
    user_profile['nationality'] = input("Current nationality: ")
    user_profile['marital'] = input("Marital status: ")
    log_action('profile', 'Basic information recorded')


def collect_education():
    separator()
    slow_print("EDUCATION DETAILS")
    separator()
    user_profile['qualification'] = input("Highest qualification: ")
    user_profile['field'] = input("Field of study: ")
    user_profile['marks'] = float(input("Marks percentage: "))
    user_profile['year'] = int(input("Graduation year: "))
    log_action('profile', 'Education details recorded')


def collect_work():
    separator()
    slow_print("WORK EXPERIENCE")
    separator()
    user_profile['experience'] = int(input("Years of experience: "))
    user_profile['occupation'] = input("Occupation: ")
    user_profile['skills'] = input("Skills (comma separated): ").split(',')
    log_action('profile', 'Work experience recorded')


def collect_language():
    separator()
    slow_print("LANGUAGE ABILITY")
    separator()
    user_profile['english'] = input("English level (Basic/Intermediate/Advanced): ")
    log_action('profile', 'Language ability recorded')


def collect_finances():
    separator()
    slow_print("FINANCIAL STATUS")
    separator()
    user_profile['savings'] = float(input("Total savings (USD): "))
    user_profile['monthly_income'] = float(input("Monthly income (USD): "))
    user_profile['liabilities'] = float(input("Total liabilities (USD): "))
    log_action('profile', 'Financial information recorded')


# ---------------- BASE SCORING ----------------

def education_score():
    m = user_profile['marks']
    if m >= 85: return 30
    if m >= 70: return 20
    return 10


def experience_score():
    y = user_profile['experience']
    if y >= 8: return 30
    if y >= 4: return 20
    return 10


def language_score():
    lvl = user_profile['english'].lower()
    if lvl == 'advanced': return 20
    if lvl == 'intermediate': return 10
    return 5


def base_score():
    return education_score() + experience_score() + language_score()


# ---------------- COUNTRY POINT SYSTEMS ----------------

def canada_points():
    score = base_score()
    if user_profile['experience'] >= 3:
        score += 10
    if user_profile['english'].lower() == 'advanced':
        score += 10
    visa_scores['Canada'] = score
    return score


def australia_points():
    score = base_score()
    if 'age' in user_profile: 
        score += 5
    if user_profile['experience'] >= 5:
        score += 10
    visa_scores['Australia'] = score
    return score


def germany_points():
    score = education_score() + experience_score()
    if 'engineering' in user_profile['field'].lower():
        score += 15
    visa_scores['Germany'] = score
    return score


def uk_points():
    score = base_score()
    if user_profile['experience'] >= 2:
        score += 10
    visa_scores['UK'] = score
    return score


def uae_points():
    score = experience_score()
    if user_profile['monthly_income'] >= 3000:
        score += 20
    visa_scores['UAE'] = score
    return score


# ---------------- VISA MODULES ----------------

def student_visa():
    separator()
    slow_print("STUDENT VISA MODULE")
    separator()

    academic_score = education_score() + language_score()
    slow_print(f"Academic Score: {academic_score}")

    marks = user_profile['marks']
    scholarships = []

    if marks >= 85:
        scholarships = [
            "Canada – Vanier Scholarship",
            "UK – Chevening Scholarship",
            "Australia – Destination Australia",
            "Germany – DAAD Scholarship"
        ]
    elif marks >= 70:
        scholarships = [
            "UK – Commonwealth Scholarship",
            "Canada – University Entrance Scholarship",
            "Australia – Merit Based Scholarship"
        ]
    elif marks >= 60:
        scholarships = ["Partial tuition waiver possible"]
    else:
        scholarships = ["Self-funded study recommended"]

    slow_print("Eligible Scholarships:")
    for s in scholarships:
        slow_print(f"- {s}")

    log_action("student", "Student visa assessed")
    pause()


def labour_visa():
    separator()
    slow_print("LABOUR VISA MODULE")
    separator()

    score = experience_score()
    slow_print(f"Experience Score: {score}")

    slow_print("Select your main labour skill:")
    slow_print("1. Construction")
    slow_print("2. Factory / Manufacturing")
    slow_print("3. Agriculture")
    slow_print("4. Driver")
    slow_print("5. Hotel / Restaurant")

    choice = input("Enter choice: ")

    country_map = {
        "1": "Canada, Australia",
        "2": "Germany, Poland",
        "3": "Australia, New Zealand",
        "4": "UAE, Saudi Arabia",
        "5": "UK, UAE"
    }

    if choice in country_map:
        slow_print("Recommended countries:")
        slow_print(country_map[choice])
    else:
        slow_print("Invalid selection")

    log_action("labour", "Labour visa assessed")
    pause()


def skilled_immigration():
    separator()
    slow_print("SKILLED IMMIGRATION MODULE")
    separator()

    slow_print(f"Canada Points: {canada_points()}")
    slow_print(f"Australia Points: {australia_points()}")
    slow_print(f"Germany Points: {germany_points()}")
    slow_print(f"UK Points: {uk_points()}")
    slow_print(f"UAE Points: {uae_points()}")

    slow_print("Visa Success Chances:")
    for country, points in visa_scores.items():
        chance = min(95, max(30, int(points * 0.9)))
        slow_print(f"{country}: {chance}% chance")

    log_action("skilled", "Skilled immigration evaluated")
    pause()


def investment_visa():
    separator()
    slow_print("INVESTMENT VISA MODULE")
    separator()
    amount = float(input("Investment amount (USD): "))
    if amount >= 500000:
        slow_print("Golden Visa level")
    elif amount >= 150000:
        slow_print("Business establishment visa")
    else:
        slow_print("Below investment threshold")
    log_action('investment', 'Investment visa evaluated')
    pause()


def retirement_visa():
    separator()
    slow_print("RETIREMENT VISA MODULE")
    separator()
    age = int(input("Age: "))
    pension = float(input("Monthly pension (USD): "))
    if age >= 55 and pension >= 1500:
        slow_print("Eligible for retirement visas")
    else:
        slow_print("Not eligible yet")
    log_action('retirement', 'Retirement visa evaluated')
    pause()


# ---------------- FINANCIAL PLANNING MODULE ----------------

def financial_planning():
    separator()
    slow_print("FINANCIAL PLANNING FOR IMMIGRATION")
    separator()
    monthly_surplus = user_profile['monthly_income'] - (user_profile['liabilities'] / 12)
    yearly_savings = monthly_surplus * 12
    financial_plan['monthly_surplus'] = monthly_surplus
    financial_plan['yearly_savings'] = yearly_savings

    slow_print(f"Estimated monthly surplus: ${monthly_surplus:.2f}")
    slow_print(f"Estimated yearly savings: ${yearly_savings:.2f}")

    if yearly_savings >= 20000:
        slow_print("You can fund skilled or student immigration independently")
    elif yearly_savings >= 8000:
        slow_print("You should combine savings with scholarships or sponsors")
    else:
        slow_print("Financial improvement required before immigration")

    slow_print("Suggested plan:")
    slow_print("- Reduce liabilities")
    slow_print("- Improve income streams")
    slow_print("- Save minimum 24 months")
    log_action('finance', 'Financial plan generated')
    pause()


# ---------------- AI STYLE RECOMMENDATION ENGINE ----------------

def ai_recommendation():
    separator()
    slow_print("AI-STYLE IMMIGRATION RECOMMENDATION SYSTEM")
    separator()

    recommendations = []

    for country, score in visa_scores.items():
        if score >= 80:
            level = "Excellent"
        elif score >= 60:
            level = "Good"
        elif score >= 40:
            level = "Fair"
        else:
            level = "Low"

        recommendations.append((country, score, level))

    recommendations.sort(key=lambda x: x[1], reverse=True)

    rank = 1
    for country, score, level in recommendations:
        slow_print(f"Rank {rank}: {country}")
        slow_print(f"  Score: {score}")
        slow_print(f"  Success Probability: {level}")

        if level == "Excellent":
            slow_print("  Suggested Path: Skilled PR → Citizenship")
        elif level == "Good":
            slow_print("  Suggested Path: Study/Work → PR")
        elif level == "Fair":
            slow_print("  Suggested Path: Improve skills & reapply")
        else:
            slow_print("  Suggested Path: Financial & profile improvement needed")

        rank += 1
        slow_print("-")

    slow_print("AI Insight:")
    if recommendations:
        best = recommendations[0]
        slow_print(f"Best option based on your profile: {best[0]}")
        slow_print("Focus your efforts on this country first.")

    log_action('ai', 'AI recommendation generated')
    pause()


# ---------------- REPORTING ----------------

def final_report():
    separator()
    slow_print("FINAL IMMIGRATION REPORT")
    separator()
    slow_print(f"Applicant: {user_profile.get('name', 'N/A')}")
    slow_print("Country-wise points:")
    for c, s in visa_scores.items():
        slow_print(f"{c}: {s}")
    slow_print("Recommended long-term goal: Permanent Residency → Citizenship")
    pause()


def activity_log():
    separator()
    slow_print("SYSTEM ACTIVITY LOG")
    separator()
    for module, actions in history_log.items():
        slow_print(f"{module.upper()} MODULE")
        for a in actions:
            slow_print(f"- {a}")
    pause()


# ---------------- MENU ----------------

def menu():
    separator()
    print("1. Student Visa")
    print("2. Labour Visa")
    print("3. Skilled Immigration")
    print("4. Investment Visa")
    print("5. Retirement Visa")
    print("6. Financial Planning")
    print("7. Final Report")
    print("8. Activity Log")
    print("0. Exit")
    return input("Select option: ")


# ---------------- MAIN ----------------

def main():
    separator()
    slow_print("ADVANCED IMMIGRATION ADVISORY SYSTEM")
    separator()

    data_loaded = load_data()
    
    if data_loaded:
        slow_print("Welcome back! Your previous session data has been restored.")
        choice = input("Do you want to update your profile? (yes/no): ").lower()
        if choice == 'yes':
            collect_basic_info()
            collect_education()
            collect_work()
            collect_language()
            collect_finances()
    else:
        collect_basic_info()
        collect_education()
        collect_work()
        collect_language()
        collect_finances()

    while True:
        choice = menu()
        if choice == '1': student_visa()
        elif choice == '2': labour_visa()
        elif choice == '3': skilled_immigration()
        elif choice == '4': investment_visa()
        elif choice == '5': retirement_visa()
        elif choice == '6': financial_planning()
        elif choice == '7': final_report()
        elif choice == '8': activity_log()
        elif choice == '0':
            slow_print("Session closed")
            sys.exit()
        else:
            slow_print("Invalid selection")


if __name__ == '__main__':
    main()

# ---------------- DOCUMENT CHECKLIST MODULE ----------------

def document_checklist():
    separator()
    slow_print("DOCUMENT CHECKLIST GENERATOR")
    separator()

    common_docs = [
        "Passport",
        "National ID",
        "Birth Certificate",
        "Educational Transcripts",
        "Police Clearance",
        "Medical Examination",
        "Passport Photos"
    ]

    for doc in common_docs:
        slow_print(f"- {doc}")

    slow_print("Additional documents depend on visa category.")
    log_action('documents', 'Checklist generated')
    pause()


# ---------------- APPLICATION TIMELINE SIMULATOR ----------------

def application_timeline():
    separator()
    slow_print("APPLICATION & CITIZENSHIP TIMELINE SIMULATOR")
    separator()

    years = 0
    stages = [
        "Profile Preparation",
        "Visa Application",
        "Temporary Residence",
        "Permanent Residence",
        "Citizenship Eligibility"
    ]

    for stage in stages:
        years += 1
        slow_print(f"Year {years}: {stage}")

    slow_print(f"Estimated total years to citizenship: {years}")
    log_action('timeline', 'Timeline simulated')
    pause()


# ---------------- YEARLY FINANCIAL GROWTH SIMULATOR ----------------

def financial_growth_simulator():
    separator()
    slow_print("YEAR-BY-YEAR FINANCIAL GROWTH SIMULATOR")
    separator()

    yearly_income = income * 12
    savings_rate = 0.25
    yearly_savings = yearly_income * savings_rate

    exchange_rates = {
        "Canada": 1.85,
        "Australia": 1.75,
        "Germany": 3.1,
        "UK": 3.5,
        "UAE": 0.75
    }

    total_savings = 0

    for year in range(1, 11):
        total_savings += yearly_savings
        slow_print(f"Year {year}:")
        slow_print(f"  Income Saved (PKR): {int(yearly_savings)}")
        slow_print(f"  Total Savings (PKR): {int(total_savings)}")

        for country, rate in exchange_rates.items():
            foreign_value = total_savings / rate
            slow_print(f"    {country} Equivalent: {int(foreign_value)}")

        slow_print("-")

    slow_print("Financial Insight:")
    if total_savings > 3000000:
        slow_print("You are financially strong for skilled migration.")
    elif total_savings > 1500000:
        slow_print("You may proceed with study or work visas.")
    else:
        slow_print("Financial growth needed before migration.")

    log_action('finance', 'Financial growth simulated')
    pause()


# ---------------- VISA REJECTION ANALYSIS ----------------

def rejection_analysis():
    separator()
    slow_print("VISA REJECTION RISK ANALYSIS")
    separator()

    risks = []

    if income < 300:
        risks.append("Low financial proof")
    if experience < 2:
        risks.append("Insufficient work experience")
    if education_level == "highschool":
        risks.append("Low education level")

    if not risks:
        slow_print("Low rejection risk detected")
    else:
        slow_print("Potential rejection reasons:")
        for r in risks:
            slow_print(f"- {r}")

    log_action('risk', 'Rejection analysis done')
    pause()


# ---------------- MAIN EXTENDED MENU ----------------

def extended_menu():
    while True:
        separator()
        slow_print("EXTENDED IMMIGRATION SYSTEM MENU")
        separator()
        slow_print("1. Document Checklist")
        slow_print("2. Timeline Simulator")
        slow_print("3. Rejection Risk Analysis")
        slow_print("4. AI Recommendation")
        slow_print("5. Exit")

        choice = input("Select option: ")

        if choice == '1':
            document_checklist()
        elif choice == '2':
            application_timeline()
        elif choice == '3':
            rejection_analysis()
        elif choice == '4':
            ai_recommendation()
        elif choice == '5':
            break
        else:
            slow_print("Invalid option")


# ---------------- PROGRAM END ----------------

slow_print("Immigration Decision Support System Completed")




