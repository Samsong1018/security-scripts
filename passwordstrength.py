import re
import hashlib

def check_password_strength(password):
    """
    Evaluate password strength and return a score and feedback.
    """
    score = 0
    feedback = []
    
    # Length check
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Password should be at least 8 characters long")
    
    # Uppercase check
    if re.search(r'[A-Z]', password):
        score += 1
    else:
        feedback.append("Add uppercase letters")
    
    # Lowercase check
    if re.search(r'[a-z]', password):
        score += 1
    else:
        feedback.append("Add lowercase letters")
    
    # Number check
    if re.search(r'\d', password):
        score += 1
    else:
        feedback.append("Add numbers")
    
    # Special character check
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 1
    else:
        feedback.append("Add special characters")
    
    # Determine strength level
    strength_levels = ["Very Weak", "Weak", "Fair", "Good", "Strong", "Very Strong"]
    strength = strength_levels[score]
    
    return {"score": score, "strength": strength, "feedback": feedback}


password = input("Enter a password to check: ")
result = check_password_strength(password)
    
print(f"\nStrength: {result['strength']} ({result['score']}/5)")
if result['feedback']:
    print("Suggestions:")
    for suggestion in result['feedback']:
        print(f"  - {suggestion}")

print("Your hash: " + hashlib.sha256(password.encode('utf-8')).hexdigest())