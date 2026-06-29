# ================= IMPORTS =================
import math
import re
from datetime import datetime


# ============ COMMON WEAK PASSWORDS ============
COMMON_PASSWORDS = [
    "123456", "password", "12345678", "qwerty", "abc123",
    "111111", "admin", "welcome", "123123", "password123"
]


# ============ ENTROPY CALCULATION ============
def calculate_entropy(password):
    charset = 0

    if re.search(r"[a-z]", password):
        charset += 26

    if re.search(r"[A-Z]", password):
        charset += 26

    if re.search(r"[0-9]", password):
        charset += 10

    if re.search(r"[^A-Za-z0-9]", password):
        charset += 32

    if charset == 0:
        return 0

    entropy = len(password) * math.log2(charset)
    return round(entropy, 2)


# ============ PASSWORD ANALYSIS ============
def analyze_password(password):
    score = 0
    suggestions = []

    # Length check
    if len(password) >= 8:
        score += 20
    else:
        suggestions.append("Use at least 8 characters")

    # Uppercase check
    if re.search(r"[A-Z]", password):
        score += 15
    else:
        suggestions.append("Add uppercase letters")

    # Lowercase check
    if re.search(r"[a-z]", password):
        score += 15
    else:
        suggestions.append("Add lowercase letters")

    # Number check
    if re.search(r"[0-9]", password):
        score += 15
    else:
        suggestions.append("Add numbers")

    # Special character check
    if re.search(r"[^A-Za-z0-9]", password):
        score += 15
    else:
        suggestions.append("Add special characters")

    # Entropy calculation
    entropy = calculate_entropy(password)

    if entropy >= 50:
        score += 20

    # Common password check
    if password.lower() in COMMON_PASSWORDS:
        score -= 30
        suggestions.append("Very common password detected")

    # Predictable pattern detection
    if "123" in password or "abc" in password.lower():
        score -= 10
        suggestions.append("Avoid predictable patterns")

    # Keep score within 0–100
    score = max(0, min(score, 100))

    # Password classification
    if score < 40:
        strength = "WEAK"
        rating = "Poor Password"
        verdict = "Very risky password"
        crack_time = "Few seconds"

    elif score < 80:
        strength = "MEDIUM"
        rating = "Average Password"
        verdict = "Decent but can improve"
        crack_time = "Months / Years"

    else:
        strength = "STRONG"
        rating = "Excellent Password"
        verdict = "Highly secure password"
        crack_time = "Many years"

    return strength, score, entropy, suggestions, rating, verdict, crack_time


# ============ SECURITY BAR ============
def security_bar(score):
    filled = score // 10
    empty = 10 - filled
    return "[" + "█" * filled + "-" * empty + "]"


# ============ SAVE REPORT ============
def save_report(password, result):
    with open("password_report.txt", "a") as file:
        file.write(f"\nDate: {datetime.now()}\n")
        file.write(f"Password: {'*' * len(password)}\n")
        file.write(f"Strength: {result[0]}\n")
        file.write(f"Score: {result[1]}/100\n")
        file.write(f"Entropy: {result[2]} bits\n")
        file.write(f"Crack Time: {result[6]}\n")
        file.write("-" * 40 + "\n")


# ============ MAIN PROGRAM ============
print("===== AI Password Strength Analyzer =====")

while True:
    password = input("\nEnter Password (or type exit): ")

    if password.lower() == "exit":
        print("Program Closed Successfully.")
        break

    result = analyze_password(password)

    print("\n===== AI Password Analysis =====")
    print("Password Checked Successfully")
    print("Date:", datetime.now().strftime("%Y-%m-%d %I:%M %p"))
    print("Strength:", result[0])
    print("Score:", result[1], "/100")
    print("Entropy:", result[2], "bits")
    print("Crack Time Estimate:", result[6])
    print("Security Level:", security_bar(result[1]), f"{result[1]}%")
    print("Rating:", result[4])
    print("AI Verdict:", result[5])

    print("\nSuggestions:")
    if result[3]:
        for suggestion in result[3]:
            print("-", suggestion)
    else:
        print("- No suggestions. Excellent password!")

    print("\nBest Password Example:")
    print("Abc@2026Secure!")

    save_report(password, result)
