import streamlit as st
import random

st.set_page_config(page_title="🔤 Lithuanian Verb Conjugation Quiz", page_icon="🇱🇹", layout="centered")

# Initialize session state variables
for key, default in {
    "score": 0,
    "correct_count": 0,
    "current": 0,
    "finished": False,
    "question": {},
    "answer": None,
    "show_feedback": False,
    "feedback_text": "",
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

conjugations = {
    "pradėti": {"aš": "pradedu", "tu": "pradedi", "jis/ji": "pradeda", "mes": "pradedame", "jūs": "pradedate", "jie/jos": "pradeda"},
    "daryti": {"aš": "darau", "tu": "darai", "jis/ji": "daro", "mes": "darome", "jūs": "darote", "jie/jos": "daro"},
    "veikti": {"aš": "veikiu", "tu": "veiki", "jis/ji": "veikia", "mes": "veikiame", "jūs": "veikiate", "jie/jos": "veikia"},
    "klausti": {"aš": "klausiu", "tu": "klausi", "jis/ji": "klausia", "mes": "klausiame", "jūs": "klausiate", "jie/jos": "klausia"},
    "elgtis": {"aš": "elgiuosi", "tu": "elgiesi", "jis/ji": "elgiasi", "mes": "elgiamės", "jūs": "elgiatės", "jie/jos": "elgiasi"},
    "aiškinti": {"aš": "aiškinu", "tu": "aiškini", "jis/ji": "aiškina", "mes": "aiškiname", "jūs": "aiškinate", "jie/jos": "aiškina"},
    "rašyti": {"aš": "rašau", "tu": "rašai", "jis/ji": "rašo", "mes": "rašome", "jūs": "rašote", "jie/jos": "rašo"},
    "suprasti": {"aš": "suprantu", "tu": "supranti", "jis/ji": "supranta", "mes": "suprantame", "jūs": "suprantate", "jie/jos": "supranta"},
    "būti": {"aš": "esu", "tu": "esi", "jis/ji": "yra", "mes": "esame", "jūs": "esate", "jie/jos": "yra"},
    "turėti": {"aš": "turiu", "tu": "turi", "jis/ji": "turi", "mes": "turime", "jūs": "turite", "jie/jos": "turi"},
    "žinoti": {"aš": "žinau", "tu": "žinai", "jis/ji": "žino", "mes": "žinome", "jūs": "žinote", "jie/jos": "žino"},
}

meanings = {
    "pradėti": "to start / to begin",
    "daryti": "to do / to make",
    "veikti": "to act / to operate",
    "klausti": "to ask",
    "elgtis": "to behave",
    "aiškinti": "to explain",
    "rašyti": "to write",
    "suprasti": "to understand",
    "būti": "to be",
    "turėti": "to have",
    "žinoti": "to know",
}

pronouns = ["aš", "tu", "jis/ji", "mes", "jūs", "jie/jos"]

TOTAL_QUESTIONS = 20

def new_question():
    verb = random.choice(list(conjugations.keys()))
    pronoun = random.choice(pronouns)
    correct = conjugations[verb][pronoun]

    # Get distractors from other pronouns for same verb
    distractors = []
    for p in pronouns:
        if p != pronoun:
            form = conjugations[verb][p]
            if form != correct and form not in distractors:
                distractors.append(form)
    # Pick 2 random distractors
    distractors = random.sample(distractors, min(2, len(distractors)))

    options = distractors + [correct]
    random.shuffle(options)

    st.session_state.question = {
        "verb": verb,
        "meaning": meanings[verb],
        "pronoun": pronoun,
        "correct": correct,
        "options": options
    }
    st.session_state.answer = None
    st.session_state.show_feedback = False
    st.session_state.feedback_text = ""

def reset_game():
    st.session_state.score = 0
    st.session_state.correct_count = 0
    st.session_state.current = 0
    st.session_state.finished = False
    new_question()

if st.session_state.current == 0 and not st.session_state.finished:
    new_question()

st.title("🔤 Lithuanian Verb Conjugation Quiz")

if not st.session_state.finished:
    st.markdown(f"**Question {st.session_state.current + 1} of {TOTAL_QUESTIONS}**")

    q = st.session_state.question
    st.markdown(f"### Verb **„{q['verb']}“** (*{q['meaning']}*) with pronoun **„{q['pronoun']}“**")

    # Show options radio if feedback not shown yet, else disable selection
    if not st.session_state.show_feedback:
        st.session_state.answer = st.radio(
            "Choose the correct form:",
            q["options"],
            index=0,
            key=f"answer_{st.session_state.current}"
        )

        if st.button("Submit Answer"):
            if st.session_state.answer is None:
                st.warning("Please select an answer before submitting.")
            else:
                if st.session_state.answer.strip().lower() == q["correct"].strip().lower():
                    st.session_state.score += 10
                    st.session_state.correct_count += 1
                    st.session_state.feedback_text = "✅ Correct!"
                else:
                    st.session_state.feedback_text = f"❌ Incorrect. Correct answer: **{q['correct']}**"
                st.session_state.show_feedback = True

    else:
        # Feedback shown, disable radio but still display selection
        st.radio(
            "Choose the correct form:",
            q["options"],
            index=q["options"].index(st.session_state.answer),
            key=f"answer_{st.session_state.current}",
            disabled=True
        )
        # Show feedback
        if "✅" in st.session_state.feedback_text:
            st.success(st.session_state.feedback_text)
        else:
            st.error(st.session_state.feedback_text)

        if st.button("Next Question"):
            st.session_state.show_feedback = False
            st.session_state.feedback_text = ""
            st.session_state.answer = None
            st.session_state.current += 1
            if st.session_state.current >= TOTAL_QUESTIONS:
                st.session_state.finished = True
            else:
                new_question()
            st.experimental_rerun()

else:
    st.markdown(f"""
    🎉 **Quiz Finished!**  
    ✅ Correct answers: **{st.session_state.correct_count} / {TOTAL_QUESTIONS}**  
    🏆 Score: **{st.session_state.score} / {TOTAL_QUESTIONS * 10}**
    """)

    if st.button("🔄 Play Again"):
        reset_game()
        st.experimental_rerun()
