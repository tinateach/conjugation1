import streamlit as st
import random

st.set_page_config(
    page_title="🔤 Lithuanian Verb Conjugation Quiz",
    page_icon="🇱🇹",
    layout="centered"
)

# Lithuanian present tense conjugations
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

# Meanings for the infinitives
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

TOTAL_QUESTIONS = 10

# --- Initialize session state ---
if "score" not in st.session_state:
    st.session_state.score = 0
    st.session_state.correct_count = 0
    st.session_state.current = 0
    st.session_state.finished = False
    st.session_state.feedback = ""
    st.session_state.show_feedback = False
    st.session_state.question = {}
    st.session_state.answer = None

def new_question():
    verb = random.choice(list(conjugations.keys()))
    pronoun = random.choice(pronouns)
    correct = conjugations[verb][pronoun]

    # Pick other forms of the SAME verb
    possible_pronouns = [p for p in pronouns if p != pronoun]
    distractors = set()
    while len(distractors) < 2 and possible_pronouns:
        dp = random.choice(possible_pronouns)
        possible_pronouns.remove(dp)
        distractor = conjugations[verb][dp]
        if distractor != correct:
            distractors.add(distractor)

    options = list(distractors)
    options.append(correct)
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
    st.session_state.feedback = ""

def reset_game():
    st.session_state.score = 0
    st.session_state.correct_count = 0
    st.session_state.current = 0
    st.session_state.finished = False
    new_question()

if st.session_state.current == 0 and not st.session_state.finished:
    new_question()

st.markdown("<h1 style='color: red; text-align: center;'>🔤 Lithuanian Verb Conjugation Quiz</h1>", unsafe_allow_html=True)

if not st.session_state.finished:
    q = st.session_state.question
    st.markdown(
        f"### Veiksmažodis **„{q['verb']}“** (*{q['meaning']}*) su įvardžiu **„{q['pronoun']}“**",
        unsafe_allow_html=True
    )

    st.session_state.answer = st.radio(
        "Pasirinkite teisingą formą:",
        q["options"],
        key=f"answer_{st.session_state.current}"
    )

    if st.button("Patikrinti atsakymą"):
        if st.session_state.answer is None:
            st.warning("Pasirinkite atsakymą prieš tikrinant.")
        else:
            if st.session_state.answer.strip().lower() == q["correct"].strip().lower():
                st.session_state.score += 10
                st.session_state.correct_count += 1
                st.session_state.feedback = "✅ Teisingai! Puiku! 😊"
            else:
                st.session_state.feedback = f"❌ Neteisingai. Teisingas atsakymas: **{q['correct']}**"
            st.session_state.show_feedback = True

    if st.session_state.show_feedback:
        if "✅" in st.session_state.feedback:
            st.success(st.session_state.feedback)
        else:
            st.error(st.session_state.feedback)

        if st.button("Kitas klausimas"):
            st.session_state.current += 1
            if st.session_state.current >= TOTAL_QUESTIONS:
                st.session_state.finished = True
            else:
                new_question()
            st.session_state.show_feedback = False
            st.experimental_rerun()

else:
    st.markdown(f"""
    🎉 **Žaidimas baigtas!**  
    ✅ Teisingų atsakymų: **{st.session_state.correct_count} / {TOTAL_QUESTIONS}**  
    🏆 Surinkta taškų: **{st.session_state.score} / {TOTAL_QUESTIONS * 10}**
    """, unsafe_allow_html=True)

    if st.button("🔄 Žaisti iš naujo"):
        reset_game()
        st.experimental_rerun()
