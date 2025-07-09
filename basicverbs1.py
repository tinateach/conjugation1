import streamlit as st
import random

conjugations = {
    "pradėti": {"aš": "pradedu", "tu": "pradedi", "jis/ji": "pradeda", "mes": "pradedame", "jūs": "pradedate", "jie/jos": "pradeda"},
    # add your other verbs here
}

pronouns = ["aš", "tu", "jis/ji", "mes", "jūs", "jie/jos"]

if "score" not in st.session_state:
    st.session_state.score = 0
if "current" not in st.session_state:
    st.session_state.current = 0
if "question" not in st.session_state:
    st.session_state.question = None

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

    st.session_state.question = {
        "verb": verb,
        "pronoun": pronoun,
        "correct": correct,
        "options": options
    }
    st.session_state.answered = False
    st.session_state.selected_option = None

if st.session_state.question is None:
    new_question()

q = st.session_state.question

# Display question nicely
st.markdown(f"**Veiksmažodis „{q['verb']}“ su įvardžiu „{q['pronoun']}“**")

for option in q['options']:
    if st.button(option):
        st.session_state.selected_option = option
        st.session_state.answered = True
        if option == q['correct']:
            st.success("✅ Puiku! Teisingai.")
            st.session_state.score += 10
        else:
            st.error(f"❌ Neteisingai. Teisingas atsakymas: {q['correct']}")

        new_question()
        st.experimental_rerun()

st.write(f"Taškai: {st.session_state.score}")
