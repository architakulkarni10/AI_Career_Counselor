
# import streamlit as st
# import requests
# import pandas as pd
# from io import BytesIO
# import base64

# # ---------------- CUSTOM CSS ----------------
# st.markdown("""
#     <style>
#         .chat-bubble {
#             padding: 12px 16px;
#             border-radius: 15px;
#             margin-bottom: 10px;
#             max-width: 80%;
#             font-size: 16px;
#             line-height: 1.5;
#             word-wrap: break-word;
#         }
#         .user-msg {
#             background-color: #007BFF;
#             color: white;
#             align-self: flex-end;
#             margin-left: auto;
#             text-align: right;
#         }
#         .bot-msg {
#             background-color: #f1f1f1;
#             color: #212529;
#             align-self: flex-start;
#             margin-right: auto;
#         }
#         .chat-container {
#             display: flex;
#             flex-direction: column;
#         }
#         .start-over-btn > button {
#             background-color: #dc3545;
#             color: white;
#             border-radius: 10px;
#             margin-top: 10px;
#         }
#     </style>
# """, unsafe_allow_html=True)

# # ---------------- PAGE CONFIG ----------------
# st.set_page_config(page_title="AI Career Counselor", page_icon="🎓", layout="wide")

# st.title("🧠 AI Career Counselor")
# st.caption("Empowering your future through personalized career guidance.")

# # ---------------- SIDEBAR NAVIGATION ----------------
# st.sidebar.title("🎯 Navigation")
# choice = st.sidebar.radio("Choose Mode", ["💬 Chat", "📝 Quiz", "📊 Recommendations"])

# # ---------------- SESSION STATE ----------------
# if 'quiz_answers' not in st.session_state:
#     st.session_state.quiz_answers = {}

# if 'chat_history' not in st.session_state:
#     st.session_state.chat_history = []

# def get_career_matches(answers):
#     careers = {
#         "Software Engineer": 0,
#         "Psychologist": 0,
#         "UX Designer": 0,
#         "Environmental Scientist": 0,
#         "Entrepreneur": 0,
#         "Graphic Designer": 0
#     }

#     interest = answers.get("interest")
#     skills = answers.get("skills")
#     work = answers.get("work")
#     personality = answers.get("personality")
#     values = answers.get("values")

#     if interest == "Technology":
#         careers["Software Engineer"] += 2
#         careers["UX Designer"] += 1
#     if interest == "Helping People":
#         careers["Psychologist"] += 2
#     if interest == "Creativity":
#         careers["Graphic Designer"] += 2
#         careers["UX Designer"] += 1
#     if interest == "Science":
#         careers["Environmental Scientist"] += 2
#     if skills == "Empathy":
#         careers["Psychologist"] += 2
#     if skills == "Logical Thinking":
#         careers["Software Engineer"] += 2
#     if skills == "Creativity":
#         careers["Graphic Designer"] += 1
#         careers["UX Designer"] += 2
#     if personality == "Big Picture Thinker":
#         careers["Entrepreneur"] += 2
#     if work == "Hands-on":
#         careers["Environmental Scientist"] += 2

#     total = sum(careers.values()) or 1
#     for k in careers:
#         careers[k] = round((careers[k] / total) * 100)
#     return careers

# def get_career_details(career):
#     details = {
#         "Software Engineer": "Develops software and systems. High salary, remote options, high innovation.",
#         "Psychologist": "Helps people with mental health. Requires advanced degrees, emotionally rewarding.",
#         "UX Designer": "Designs user interfaces and experiences. Combines creativity with tech.",
#         "Environmental Scientist": "Studies and solves environmental problems. Often fieldwork based.",
#         "Entrepreneur": "Starts and manages businesses. High risk, high reward.",
#         "Graphic Designer": "Creates visual concepts by hand or with software. Creative and client-driven."
#     }
#     return details.get(career, "No details available.")

# def generate_download_link(data, filename):
#     towrite = BytesIO()
#     data.to_csv(towrite, index=False)
#     towrite.seek(0)
#     b64 = base64.b64encode(towrite.read()).decode()
#     return f'<a href="data:file/csv;base64,{b64}" download="{filename}">📥 Download Report as CSV</a>'

# # ---------------- CHAT MODE ----------------
# if choice == "💬 Chat":
#     st.subheader("💬 Chat with CareerBot")

#     if st.button("🔄 Start New Chat", key="start_over", type="primary"):
#         st.session_state.chat_history = []

#     for entry in st.session_state.chat_history:
#         msg_class = "user-msg" if entry["sender"] == "user" else "bot-msg"
#         st.markdown(f'<div class="chat-container"><div class="chat-bubble {msg_class}">{entry["message"]}</div></div>', unsafe_allow_html=True)

#     with st.form(key="chat_form", clear_on_submit=True):
#         user_input = st.text_input("You:", key="chat_input")
#         send_clicked = st.form_submit_button("Send")

#         if send_clicked and user_input.strip():
#             st.session_state.chat_history.append({"sender": "user", "message": user_input})
#             try:
#                 response = requests.post(
#                     "http://localhost:5005/webhooks/rest/webhook",
#                     json={"sender": "user", "message": user_input}
#                 )
#                 messages = response.json()
#                 if messages:
#                     for msg in messages:
#                         bot_msg = msg.get("text", "")
#                         st.session_state.chat_history.append({"sender": "bot", "message": bot_msg})
#                 else:
#                     st.session_state.chat_history.append({"sender": "bot", "message": "..."})
#             except Exception as e:
#                 st.session_state.chat_history.append({"sender": "bot", "message": "⚠️ Unable to connect to the bot. Please ensure Rasa is running."})
#                 st.error("Bot is not running. Please start Rasa with `rasa run`.")

# elif choice == "📝 Quiz":
#     st.subheader("📝 Career Interest Quiz")

#     st.session_state.quiz_answers["interest"] = st.selectbox(
#         "1. What are you most interested in?",
#         ["Math", "Science", "Creativity", "Helping People", "Technology"]
#     )

#     st.session_state.quiz_answers["skills"] = st.selectbox(
#         "2. Which skill best describes you?",
#         ["Logical Thinking", "Communication", "Creativity", "Empathy", "Leadership"]
#     )

#     st.session_state.quiz_answers["work"] = st.selectbox(
#         "3. What kind of work do you enjoy?",
#         ["Hands-on", "Analytical", "Team-based", "Independent", "Creative"]
#     )

#     st.session_state.quiz_answers["values"] = st.selectbox(
#         "4. Which value matters most in your career?",
#         ["Making Money", "Helping Others", "Innovation", "Stability", "Recognition"]
#     )

#     st.session_state.quiz_answers["personality"] = st.selectbox(
#         "5. What type of personality do you have?",
#         ["Introverted", "Extroverted", "Detail-Oriented", "Big Picture Thinker", "Curious"]
#     )

#     if st.button("✅ Submit Quiz"):
#         st.success("✅ Answers saved! Head to '📊 Recommendations'.")

# # ---------------- RECOMMENDATION MODE ----------------
# elif choice == "📊 Recommendations":
#     st.subheader("📊 Career Recommendations")

#     if st.session_state.quiz_answers:
#         scores = get_career_matches(st.session_state.quiz_answers)
#         top_careers = sorted(scores.items(), key=lambda x: x[1], reverse=True)

#         filter_threshold = st.slider("Minimum Match %", 0, 100, 0, 5)
#         filtered_careers = [(career, score) for career, score in top_careers if score >= filter_threshold]

#         st.markdown("### 🎯 Career Fit Percentages")
#         for career, score in filtered_careers:
#             with st.expander(f"{career} ({score}%)"):
#                 st.progress(score / 100)
#                 st.write(get_career_details(career))

#         st.markdown("---")
#         st.markdown("### 📌 Summary")
#         if filtered_careers:
#             best_match = filtered_careers[0][0]
#             st.markdown(f"Your top match is **{best_match}** based on your preferences.")
#         else:
#             st.warning("No careers matched your filter.")

#         df = pd.DataFrame(filtered_careers, columns=["Career", "Match %"])
#         st.markdown(generate_download_link(df, "career_recommendations.csv"), unsafe_allow_html=True)
#     else:
#         st.warning("Please complete the quiz first.")

import streamlit as st
import requests
import pandas as pd
from io import BytesIO
import base64
from streamlit_option_menu import option_menu  # <-- NEW

st.markdown("""
 <style>
    /* Main content background white */
    .main .block-container {
        background-color: white;
        padding: 2rem 1.5rem;
        border-radius: 10px;
    }

    /* Chat bubbles (as before) */
    .chat-bubble {
        padding: 12px 16px;
        border-radius: 15px;
        margin-bottom: 10px;
        max-width: 80%;
        font-size: 16px;
        line-height: 1.5;
        word-wrap: break-word;
    }
    .user-msg {
        background-color: #007BFF;
        color: white;
        align-self: flex-end;
        margin-left: auto;
        text-align: right;
    }
    .bot-msg {
        background-color: #f1f1f1;
        color: #212529;
        align-self: flex-start;
        margin-right: auto;
    }
    .chat-container {
        display: flex;
        flex-direction: column;
    }
    .start-over-btn > button {
        background-color: #dc3545;
        color: white;
        border-radius: 10px;
        margin-top: 10px;
    }
</style>

""", unsafe_allow_html=True)


# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Career Counselor", page_icon="🎓", layout="wide")

st.title("🧠 AI Career Counselor")
st.caption("Empowering your future through personalized career guidance.")

# ---------------- MODERN SIDEBAR ----------------
with st.sidebar:
    choice = option_menu(
        menu_title="🎯 Navigation",
        options=["💬 Chat", "📝 Quiz", "📊 Recommendations"],
        icons=["chat-dots", "list-check", "bar-chart-line"],
        menu_icon="robot",
        default_index=0,
        styles={
            "container": {"padding": "5px", "background-color": "#0f172a"},
            "icon": {"color": "#ffffff", "font-size": "20px"},
            "nav-link": {
                "font-size": "18px",
                "text-align": "left",
                "margin":"0px",
                "--hover-color": "#1e293b"
            },
            "nav-link-selected": {
                "background-color": "#2563eb",
                "color": "white"
            },
        }
    )

# ---------------- SESSION STATE ----------------
if 'quiz_answers' not in st.session_state:
    st.session_state.quiz_answers = {}

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# ---------------- FUNCTION DEFINITIONS ----------------
def get_career_matches(answers):
    careers = {
        "Software Engineer": 0,
        "Psychologist": 0,
        "UX Designer": 0,
        "Environmental Scientist": 0,
        "Entrepreneur": 0,
        "Graphic Designer": 0
    }

    interest = answers.get("interest")
    skills = answers.get("skills")
    work = answers.get("work")
    personality = answers.get("personality")
    values = answers.get("values")

    if interest == "Technology":
        careers["Software Engineer"] += 2
        careers["UX Designer"] += 1
    if interest == "Helping People":
        careers["Psychologist"] += 2
    if interest == "Creativity":
        careers["Graphic Designer"] += 2
        careers["UX Designer"] += 1
    if interest == "Science":
        careers["Environmental Scientist"] += 2
    if skills == "Empathy":
        careers["Psychologist"] += 2
    if skills == "Logical Thinking":
        careers["Software Engineer"] += 2
    if skills == "Creativity":
        careers["Graphic Designer"] += 1
        careers["UX Designer"] += 2
    if personality == "Big Picture Thinker":
        careers["Entrepreneur"] += 2
    if work == "Hands-on":
        careers["Environmental Scientist"] += 2

    total = sum(careers.values()) or 1
    for k in careers:
        careers[k] = round((careers[k] / total) * 100)
    return careers

def get_career_details(career):
    details = {
        "Software Engineer": "Develops software and systems. High salary, remote options, high innovation.",
        "Psychologist": "Helps people with mental health. Requires advanced degrees, emotionally rewarding.",
        "UX Designer": "Designs user interfaces and experiences. Combines creativity with tech.",
        "Environmental Scientist": "Studies and solves environmental problems. Often fieldwork based.",
        "Entrepreneur": "Starts and manages businesses. High risk, high reward.",
        "Graphic Designer": "Creates visual concepts by hand or with software. Creative and client-driven."
    }
    return details.get(career, "No details available.")

def generate_download_link(data, filename):
    towrite = BytesIO()
    data.to_csv(towrite, index=False)
    towrite.seek(0)
    b64 = base64.b64encode(towrite.read()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="{filename}">📥 Download Report as CSV</a>'

# ---------------- CHAT MODE ----------------
if choice == "💬 Chat":
    st.subheader("💬 Chat with CareerBot")

    if st.button("🔄 Start New Chat", key="start_over", type="primary"):
        st.session_state.chat_history = []

    for entry in st.session_state.chat_history:
        msg_class = "user-msg" if entry["sender"] == "user" else "bot-msg"
        st.markdown(f'<div class="chat-container"><div class="chat-bubble {msg_class}">{entry["message"]}</div></div>', unsafe_allow_html=True)

    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input("You:", key="chat_input")
        send_clicked = st.form_submit_button("Send")

        if send_clicked and user_input.strip():
            st.session_state.chat_history.append({"sender": "user", "message": user_input})
            try:
                response = requests.post(
                    "http://localhost:5005/webhooks/rest/webhook",
                    json={"sender": "user", "message": user_input}
                )
                messages = response.json()
                if messages:
                    for msg in messages:
                        bot_msg = msg.get("text", "")
                        st.session_state.chat_history.append({"sender": "bot", "message": bot_msg})
                else:
                    st.session_state.chat_history.append({"sender": "bot", "message": "..."})
            except Exception as e:
                st.session_state.chat_history.append({"sender": "bot", "message": "⚠️ Unable to connect to the bot. Please ensure Rasa is running."})
                st.error("Bot is not running. Please start Rasa with `rasa run`.")

# ---------------- QUIZ MODE ----------------
elif choice == "📝 Quiz":
    st.subheader("📝 Career Interest Quiz")

    st.session_state.quiz_answers["interest"] = st.selectbox(
        "1. What are you most interested in?",
        ["Math", "Science", "Creativity", "Helping People", "Technology"]
    )

    st.session_state.quiz_answers["skills"] = st.selectbox(
        "2. Which skill best describes you?",
        ["Logical Thinking", "Communication", "Creativity", "Empathy", "Leadership"]
    )

    st.session_state.quiz_answers["work"] = st.selectbox(
        "3. What kind of work do you enjoy?",
        ["Hands-on", "Analytical", "Team-based", "Independent", "Creative"]
    )

    st.session_state.quiz_answers["values"] = st.selectbox(
        "4. Which value matters most in your career?",
        ["Making Money", "Helping Others", "Innovation", "Stability", "Recognition"]
    )

    st.session_state.quiz_answers["personality"] = st.selectbox(
        "5. What type of personality do you have?",
        ["Introverted", "Extroverted", "Detail-Oriented", "Big Picture Thinker", "Curious"]
    )

    if st.button("✅ Submit Quiz"):
        st.success("✅ Answers saved! Head to '📊 Recommendations'.")

# ---------------- RECOMMENDATION MODE ----------------
elif choice == "📊 Recommendations":
    st.subheader("📊 Career Recommendations")

    if st.session_state.quiz_answers:
        scores = get_career_matches(st.session_state.quiz_answers)
        top_careers = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        filter_threshold = st.slider("Minimum Match %", 0, 100, 0, 5)
        filtered_careers = [(career, score) for career, score in top_careers if score >= filter_threshold]

        st.markdown("### 🎯 Career Fit Percentages")
        for career, score in filtered_careers:
            with st.expander(f"{career} ({score}%)"):
                st.progress(score / 100)
                st.write(get_career_details(career))

        st.markdown("---")
        st.markdown("### 📌 Summary")
        if filtered_careers:
            best_match = filtered_careers[0][0]
            st.markdown(f"Your top match is **{best_match}** based on your preferences.")
        else:
            st.warning("No careers matched your filter.")

        df = pd.DataFrame(filtered_careers, columns=["Career", "Match %"])
        st.markdown(generate_download_link(df, "career_recommendations.csv"), unsafe_allow_html=True)
    else:
        st.warning("Please complete the quiz first.")
