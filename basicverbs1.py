import streamlit as st
import random

# Lithuanian present tense conjugations
conjugations = {
    "galėti": {"aš": "galiu", "tu": "gali", "jis/ji": "gali", "mes": "galime", "jūs": "galite", "jie/jos": "gali"},
    "sėdėti": {"aš": "sėdžiu", "tu": "sėdi", "jis/ji": "sėdi", "mes": "sėdime", "jūs": "sėdite", "jie/jos": "sėdi"},
    "atsisėsti": {"aš": "atsisėdu", "tu": "atsisėdi", "jis/ji": "atsisėdi", "mes": "atsisėdame", "jūs": "atsisėdate", "jie/jos": "atsisėda"},
    "kainuoti": {"aš": "kainuoju", "tu": "kainuoji", "jis/ji": "kainuoja", "mes": "kainuojame", "jūs": "kainuojate", "jie/jos": "kainuoja"},
    "nešti": {"aš": "nešu", "tu": "neši", "jis/ji": "neša", "mes": "nešame", "jūs": "nešate", "jie/jos": "neša"},
    "atsiskaityti": {"aš": "atsiskaitau", "tu": "atsiskaiti", "jis/ji": "atsiskaito", "mes": "atsiskaitome", "jūs": "atsiskaitote", "jie/jos": "atsiskaito"},
    "norėti": {"aš": "noriu", "tu": "nori", "jis/ji": "nori", "mes": "norime", "jūs": "norite", "jie/jos": "nori"},
    "skaityti": {"aš": "skaitau", "tu": "skaitai", "jis/ji": "skaito", "mes": "skaitome", "jūs": "skaitote", "jie/jos": "skaito"},
    "dirbti": {"aš": "dirbu", "tu": "dirbi", "jis/ji": "dirba", "mes": "dirbame", "jūs": "dirbate", "jie/jos": "dirba"},
    "rašyti": {"aš": "rašau", "tu": "rašai", "jis/ji": "rašo", "mes": "rašome", "jūs": "rašote", "jie/jos": "rašo"},
    "klausyti": {"aš": "klausau", "tu": "klausi", "jis/ji": "klauso", "mes": "klausome", "jūs": "klausote", "jie/jos": "klauso"},
    "klausti": {"aš": "klausiau", "tu": "klausiai", "jis/ji": "klausia", "mes": "klausiame", "jūs": "klausiate", "jie/jos": "klausia"},
    "būti": {"aš": "esu", "tu": "esi", "jis/ji": "yra", "mes": "esame", "jūs": "esate", "jie/jos": "yra"},
    "turėti": {"aš": "turiu", "tu": "turi", "jis/ji": "turi", "mes": "turime", "jūs": "turite", "jie/jos": "turi"},
}

pronouns = ["aš", "tu", "jis/ji", "mes", "jūs", "jie/jos"]

# English translations of verbs
verb_translations = {
    "galėti": "to be able",
    "sėdėti": "to sit",
    "atsisėsti": "to sit down",
    "kainuoti": "to cost",
    "nešti": "to carry",
    "atsiskaityti": "to pay / to settle",
    "norėti": "to want",
    "skaityti": "to read",
    "dirbti": "to work",
    "rašyti": "to write",
    "klausyti": "to listen",
    "klausti": "to ask",
    "būti": "to be",
    "turėti": "to have"
}

# Initialize session state
if "score" not in st.session_state:
    st.session_state.score = 0
    st.session_state.current = 0
    st.session_state.total = 10
    st.session_state.question = {}
    st.session_state.options = []
    st.session_state.correct = ""

def new_question():
    verb = random.choice(list(conjugations.keys()))
    pronoun = random.choice(pronouns)
    correct = conjugations[verb][pronoun]
    options = set([correct])
    all_forms = set(conjugations[verb].values())
    while len(options) < 3:
        options.add(random.choice(list(all_forms)))
    options = list(options)
    random.shuffle(options)

    st.session_state.question = {"verb": verb, "pronoun": pronoun}
    st.session_state.options = options
    st.session_state.correct = correct

def restart_game():
    st.session_state.score = 0
    st.session_state.current = 0
    new_question()

# UI
st.title("🔤 Lithuanian Verb Conjugation Quiz")
st.markdown("Choose the correct present tense form for the verb and pronoun:")

# Game logic
if st.session_state.current >= st.session_state.total:
    st.success(f"🎉 Game Over! Your score: {st.session_state.score} / {st.session_state.total * 10} points.")
    if st.button("🔄 Play Again"):
        restart_game()
        st.rerun()
else:
    if not st.session_state.question:
        new_question()

    q = st.session_state.question
    verb_lt = q["verb"]
    pronoun_lt = q["pronoun"]
    verb_en = verb_translations.get(verb_lt, "unknown")

    st.subheader(f"Veiksmažodis: **{verb_lt}**, Įvardis: **{pronoun_lt}**")
    st.caption(f"🔍 *{verb_lt}* means **{verb_en}** in English.")

    for opt in st.session_state.options:
        if st.button(opt):
            if opt == st.session_state.correct:
                st.session_state.score += 10
                st.success("✅ Teisingai! Puiku! 😊")
            else:
                st.error(f"❌ Neteisingai. Teisingas atsakymas: **{st.session_state.correct}**")
            st.session_state.current += 1
            if st.session_state.current < st.session_state.total:
                new_question()
            st.rerun()
