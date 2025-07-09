
import streamlit as st
import random

st.set_page_config(
    page_title="🔤 Lithuanian Verb Conjugation Quiz",
    page_icon="🇱🇹",
    layout="centered"
)

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

    possible_pronouns = [p for p in pronouns if p != pronoun]
    distractors = set()
    while len(distractors) < 2 and possible_pronouns:
        dp = rand
