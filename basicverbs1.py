import streamlit as st
import random

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
total_questions = 10

if "score" not in st.session_state:
    st.session_state.score = 0
if "current" not in st.session_state:
    st.session_state.current = 0
if "question" not in st.session_state:
    st.session_state.question = None
if "options" not in st.session_state:
    st.session_state.options = []
if "correct_answer" not in st.session_state:
    st.session_state.correct_answer = ""
if "answered" not in st.session_state:
    st.session_state.answered = False
if "selected_option" not in st.session_state:
    st.session_state.selected_option = None

def new_question():
    verb = random.choice(list(conjugations.keys()))
    pronoun = random.choice(pronouns)
    question_text = f'Veiksmažodis „{verb}“ su įvardžiu „{pronoun}“'
    correct = conjugations[verb][pronoun]

    options = set([correct])
    all_forms = set(conjugations[verb].values())
    while len(options) < 3:
        options.add(random.choice(list(all_forms)))
    options = list(options)
    random.shuffle(options)

    st.session_state.question = question_text
    st.session_state.correct_answer = correct
    st.session_state.options = options
    st.session_state.answered = False
    st.session_state.selected_option = None

def check_answer(selected):
    st.session_state.selected_option = selected
    st.session_state.answered = True
    if selected == st.session_state.correct_answer:
        st.session_state.score += 10

def reset_quiz():
    st.session_state.score = 0
    st.session_state.current = 0
    new_question()

st.title("🔤 Lithuanian Verb Conjugation Quiz")

if st.session_state.current >= total_questions:
    st.success(f"🎉 Žaidimas baigtas! Tavo rezultatas: {st.session_state.score} / {total_questions*10} taškų.")
    if st.button("🔄 Žaisti iš naujo"):
        reset_quiz()
else:
    if st.session_state.question is None or st.session_state.answered:
        if st.session_state.current > 0:
            st.session_state.current += 1
        if st.session_state.current < total_questions:
            new_question()

    st.markdown(f"### Klausimas {st.session_state.current + 1} iš {total_questions}")
    st.write(st.session_state.question)

    for option in st.session_state.options:
        if st.session_state.answered:
            # Show buttons disabled after answering
            if option == st.session_state.correct_answer:
                st.button(f"✅ {option}", key=option, disabled=True)
            elif option == st.session_state.selected_option:
                st.button(f"❌ {option}", key=option, disabled=True)
            else:
                st.button(option, key=option, disabled=True)
        else:
            if st.button(option, key=option):
                check_answer(option)
                st.experimental_rerun()

    if st.session_state.answered:
        if st.session_state.selected_option == st.session_state.correct_answer:
            st.success("Puiku! 😊")
        else:
            st.error(f"Neteisingai! Teisingas atsakymas: {st.session_state.correct_answer}")

        if st.session_state.current + 1 == total_questions:
            if st.button("Baigti žaidimą"):
                st.session_state.current = total_questions  # mark complete
                st.experimental_rerun()
        else:
            if st.button("Kitas klausimas"):
                st.session_state.current += 1
                st.session_state.answered = False
                st.experimental_rerun()
