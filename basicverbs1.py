import streamlit as st
import random

st.set_page_config(page_title="🔤 Lithuanian Verb Conjugation Quiz", page_icon="🇱🇹", layout="centered")

# Lithuanian present tense conjugations
conjugations = {
    "galėti":    {"aš": "galiu",    "tu": "gali",    "jis/ji": "gali",    "mes": "galime",  "jūs": "galite",  "jie/jos": "gali"},
    "sėdėti":    {"aš": "sėdžiu",  "tu": "sėdi",   "jis/ji": "sėdi",   "mes": "sėdime", "jūs": "sėdite", "jie/jos": "sėdi"},
    "atsisėsti": {"aš": "atsisėdu","tu": "atsisėdi","jis/ji": "atsisėdi","mes": "atsisėdame","jūs": "atsisėdate","jie/jos": "atsisėda"},
    "kainuoti":  {"aš": "kainuoju","tu": "kainuoji","jis/ji": "kainuoja","mes": "kainuojame","jūs": "kainuojate","jie/jos": "kainuoja"},
    "nešti":     {"aš": "nešu",    "tu": "neši",   "jis/ji": "neša",   "mes": "nešame",  "jūs": "nešate",  "jie/jos": "neša"},
    "atsiskaityti": {"aš": "atsiskaitau","tu": "atsiskaiti","jis/ji": "atsiskaito","mes": "atsiskaitome","jūs": "atsiskaitote","jie/jos": "atsiskaito"},
    "norėti":    {"aš": "noriu",   "tu": "nori",   "jis/ji": "nori",   "mes": "norime",  "jūs": "norite",  "jie/jos": "nori"},
    "skaityti":  {"aš": "skaitau", "tu": "skaitai","jis/ji": "skaito","mes": "skaitome","jūs": "skaitote","jie/jos": "skaito"},
    "dirbti":    {"aš": "dirbu",   "tu": "dirbi",  "jis/ji": "dirba",  "mes": "dirbame", "jūs": "dirbate", "jie/jos": "dirba"},
    "rašyti":    {"aš": "rašau",   "tu": "rašai",  "jis/ji": "rašo",   "mes": "rašome", "jūs": "rašote", "jie/jos": "rašo"},
    "klausyti":  {"aš": "klausau", "tu": "klausi", "jis/ji": "klauso","mes": "klausome","jūs": "klausote","jie/jos": "klauso"},
    "klausti":   {"aš": "klausiau","tu": "klausiai","jis/ji": "klausia","mes": "klausiame","jūs": "klausiate","jie/jos": "klausia"},
    "būti":      {"aš": "esu",    "tu": "esi",    "jis/ji": "yra",    "mes": "esame",   "jūs": "esate",   "jie/jos": "yra"},
    "turėti":    {"aš": "turiu",  "tu": "turi",   "jis/ji": "turi",   "mes": "turime",  "jūs": "turite",  "jie/jos": "turi"},
}

pronouns = ["aš", "tu", "jis/ji", "mes", "jūs", "jie/jos"]

TOTAL_QUESTIONS = 10

# --- Initialize state ---
if "score" not in st.session_state:
    st.session_state.score = 0
    st.session_state.current = 0
    st.session_state.question = {}
    st.session_state.finished = False

# --- Functions ---
def new_question():
    verb = random.choice(list(conjugations.keys()))
    pronoun = random.choice(pronouns)
    correct = conjugations[verb][pronoun]

    options = set([correct])
    all_forms = set(conjugations[verb].values())
    while len(options) < 3:
        choice = random.choice(list(all_forms))
        options.add(choice)
    options = list(options)
    random.shuffle(options)

    st.session_state.question = {
        "verb": verb,
        "pronoun": pronoun,
        "correct": correct,
        "options": options
    }

def reset_game():
    st.session_state.score = 0
    st.session_state.current = 0
    st.session_state.finished = False
    new_question()

# --- Main ---
st.markdown("<h1 style='color: red; text-align: center;'>🔤 Lithuanian Verb Conjugation Quiz</h1>", unsafe_allow_html=True)

if st.session_state.current == 0:
    new_question()

if not st.session_state.finished:
    q = st.session_state.question
    st.markdown(f"### Veiksmažodis **„{q['verb']}“** su įvardžiu **„{q['pronoun']}“**", unsafe_allow_html=True)

    for opt in q["options"]:
        # 3 columns: empty, button, empty → centers the button
        col1, col2, col3 = st.columns([2, 3, 2])
        with col2:
            if st.button(opt):
                if opt == q["correct"]:
                    st.success("✅ Teisingai! Puiku! 😊")
                    st.session_state.score += 10
                else:
                    st.error(f"❌ Neteisingai. Teisingas atsakymas: **{q['correct']}**")
                st.session_state.current += 1
                if st.session_state.current >= TOTAL_QUESTIONS:
                    st.session_state.finished = True
                else:
                    new_question()
                st.stop()

else:
    st.markdown(f"🎉 **Žaidimas baigtas!** Tavo rezultatas: **{st.session_state.score} / {TOTAL_QUESTIONS * 10}** taškų.", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 3, 2])
    with col2:
        if st.button("🔄 Žaisti iš naujo"):
            reset_game()
