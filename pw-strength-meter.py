import streamlit as st
import re
import random
import string

# Common weak passwords
Weak_Passwords = {"password", "123456", "password123", "admin"}

# Function to check password strength
def check_password_strength(password):
    score = 0
    feedback = []

    if password.lower() in Weak_Passwords:
        return 0, ["❗ The password is too common. Make it unique."]

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("The Password should be at least 8 characters long.")

    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Include both uppercase and lowercase letters.")

    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("Add at least one number (0-9).")

    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("Include at least one special character (!@#$%^&*).")

    return score, feedback

# Function to create a strong password
def generate_strong_password(length=12):
    all_characters = string.ascii_letters + string.digits + "!@#$%^&*"
    password = [
        random.choice(string.ascii_uppercase),
        random.choice(string.ascii_lowercase),
        random.choice(string.digits),
        random.choice("!@#$%^&*")
    ]
    password += random.choices(all_characters, k=length - 4)
    random.shuffle(password)
    return ''.join(password)

# Streamlit App UI

st.title("🔐 Password Strength Meter")

if "checked" not in st.session_state:
    st.session_state["checked"] = False
if "last_score" not in st.session_state:
    st.session_state["last_score"] = 0
if "feedback" not in st.session_state:
    st.session_state["feedback"] = []

password = st.text_input("Enter your password:", type="password")


if st.button("✅ Check Password Strength"):
    if password:
        score, feedback = check_password_strength(password)
        st.session_state["last_score"] = score  # store score in session
        st.session_state["feedback"] = feedback
        st.session_state["checked"] = True

        st.write(f"### 🔎 Password Score: {score}/4")
        if score == 4:
            st.success("✅ Strong Password!")
        elif score == 3:
            st.warning("⚠️ Moderate Password - Consider adding more security features.")
        else:
            st.error("❌ Weak Password - Try improving it.")

        if feedback:
            st.subheader("Suggestions:")
            for tip in feedback:
                st.write("•", tip)
    else:
        st.warning("⚠️ Please enter a password before checking.")

# Suggestion if score is low
if st.session_state.get("checked") and st.session_state.get("last_score", 0) < 4:
    
    if st.button("🔄 Suggest a Strong Password"):
        strong_pw = generate_strong_password()
        st.code(strong_pw, language="text")