from flask import Flask, render_template, request
import string
import secrets

app = Flask(__name__)

COMMON_PASSWORDS = [
    "abcd@123",
    "password@123",
    "password123!",
    "welcome123@",
    "admin123#",
    "qwerty123!",
    "login123@",
    "india123@",
    "user123#",
    "test123@",
    "hello123!",
    "manager123#"
]

@app.route("/", methods=["GET", "POST"])
def home():

    score = None
    strength = ""
    percentage = 0
    suggestions = []
    generated_password = ""
    crack_time = ""
    breach_risk = "Low"

    checks = {
        "length": False,
        "uppercase": False,
        "lowercase": False,
        "number": False,
        "special": False,
        "common": False,
        "unique": False
    }

    if request.method == "POST":

        action = request.form.get("action")
        password = request.form.get("password", "")

        score = 0

        if len(password) >= 8:
            checks["length"] = True
            score += 1
        else:
            suggestions.append("Use at least 8 characters")

        if any(c.isupper() for c in password):
            checks["uppercase"] = True
            score += 1
        else:
            suggestions.append("Add uppercase letters")

        if any(c.islower() for c in password):
            checks["lowercase"] = True
            score += 1
        else:
            suggestions.append("Add lowercase letters")

        if any(c.isdigit() for c in password):
            checks["number"] = True
            score += 1
        else:
            suggestions.append("Add numbers")

        if any(c in string.punctuation for c in password):
            checks["special"] = True
            score += 1
        else:
            suggestions.append("Add special characters")

        if password.lower() not in [p.lower() for p in COMMON_PASSWORDS]:
            checks["common"] = True
            score += 1
        else:
            suggestions.append("Avoid common passwords")

        if len(set(password)) >= 5:
            checks["unique"] = True
            score += 1
        else:
            suggestions.append("Avoid repeated characters")

        percentage = int((score / 7) * 100)


        risky_words = ["123", "password", "admin", "qwerty"]

        if any(word in password.lower() for word in risky_words):
            breach_risk = "High"

        if score <= 3:
            strength = "WEAK"
            crack_time = "Few Minutes"

        elif score <= 5:
            strength = "MEDIUM"
            crack_time = "Several Days"

        else:
            strength = "STRONG"
            crack_time = "Several Years"

        if action == "generate":

            chars = (
                string.ascii_letters +
                string.digits +
                string.punctuation
            )

            generated_password = ''.join(
                secrets.choice(chars)
                for _ in range(12)
            )

    return render_template(
        "index.html",
        score=score,
        strength=strength,
        percentage=percentage,
        suggestions=suggestions,
        generated_password=generated_password,
        crack_time=crack_time,
        breach_risk=breach_risk,
        checks=checks
    )

if __name__ == "__main__":
    app.run(debug=True)