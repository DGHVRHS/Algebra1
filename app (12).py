import streamlit as st

st.set_page_config(page_title="Jeopardy!", layout="wide")

# Game Data (5 Categories: 2 Horror Movie Trivia + 3 Worksheet Categories)
JEOPARDY_DATA = {
    "Horror Icons & Killers": [
        {"val": 200, "q": "What hockey-mask wearing killer haunts Camp Crystal Lake?", "a": "Jason Voorhees"},
        {"val": 400, "q": "In 'A Nightmare on Elm Street', what weapon does Freddy Krueger wear on his right hand?", "a": "A glove with razor-sharp blades"},
        {"val": 600, "q": "What is the name of the killer doll possessed by serial killer Charles Lee Ray?", "a": "Chucky"},
        {"val": 800, "q": "In Stephen King's 'IT', what form does the shapeshifting entity most frequently take?", "a": "Pennywise the Dancing Clown"},
        {"val": 1000, "q": "What are the names of the two high school students revealed to be the original dual Ghostface killers in the 1996 movie 'Scream'?", "a": "Billy Loomis and Stu Macher"}
    ],
    "Horror Cinema": [
        {"val": 200, "q": "In 'The Ring', how many days do victims have to live after watching the cursed videotape?", "a": "7 Days"},
        {"val": 400, "q": "Which 2017 horror film directed by Jordan Peele features 'The Sunken Place'?", "a": "Get Out"},
        {"val": 600, "q": "In this 2018 psychological horror film directed by Ari Aster, a family unravels terrifying, demonic secrets following the death of their grandmother.", "a": "Hereditary"},
        {"val": 800, "q": "In 'A Quiet Place', what sensory ability do the monsters rely on to hunt humans?", "a": "Hearing / Sound"},
        {"val": 1000, "q": "This 1999 horror film popularized found-footage style as 3 student filmmakers got lost in Maryland woods.", "a": "The Blair Witch Project"}
    ],
    "Balancing Act & Scales": [
        {"val": 200, "q": r"A scale balances 3 mystery bags ($b$) and a 4-gram weight against a 25-gram weight. Write an equation modeling this.", "a": r"$3b + 4 = 25$"},
        {"val": 400, "q": r"If 2 identical boxes and a 5-gram weight balance against a 21-gram weight, what is the weight of one box?", "a": r"8 grams ($2x + 5 = 21 \implies x = 8$)"},
        {"val": 600, "q": r"A scale has 4 blocks ($x$) and two 10g weights on the left, balanced against 2 blocks and six 10g weights on the right. Write the equation.", "a": r"$4x + 20 = 2x + 60$"},
        {"val": 800, "q": r"On a balance scale, 1 star ($s$) and three 10g weights balance 3 stars and one 10g weight. What is the weight of 1 star?", "a": r"10 grams ($s + 30 = 3s + 10 \implies 2s = 20 \implies s = 10$)"},
        {"val": 1000, "q": r"From the previous scale ($s + 30 = 3s + 10$), what is the value of $2s$ (2 star weights)?", "a": r"20 grams ($2s = 20$)"}
    ],
    "Algebraic Equivalence": [
        {"val": 200, "q": r"If $4x + 9 = 25$, what is the value of $4x + 15$?", "a": r"31 (Since $4x = 16$, then $16 + 15 = 31$, or add 6 to both sides)"},
        {"val": 400, "q": r"If $6y - 12 = 30$, what is the value of $6y$?", "a": r"42 ($6y = 30 + 12$)"},
        {"val": 600, "q": r"If $2a + 3b = 15$, what is the value of $6a + 9b$?", "a": r"45 (Multiply the entire equation by 3)"},
        {"val": 800, "q": r"Given the equation $9p + 3 = 4p + 28$, find the value of $5p$.", "a": r"25 ($9p - 4p = 28 - 3 \implies 5p = 25$)"},
        {"val": 1000, "q": r"If $4r + 5s = 18$, what is the value of $12r + 15s - 10$?", "a": r"44 ($3(18) - 10 = 54 - 10 = 44$)"}
    ],
    "Equations in Real Life": [
        {"val": 200, "q": r"Britney scored 32 points in a video game. Hugh scored 22 points plus some foxes ($f$). Write an equation showing they tied.", "a": r"$22 + f = 32$"},
        {"val": 400, "q": r"If Britney (32 points) and Hugh ($22 + f$) tied, how many points is a fox ($f$) worth?", "a": r"10 points ($f = 10$)"},
        {"val": 600, "q": r"Climber A starts at 48 ft descending at 3 ft/sec. Climber B starts on ground ascending at 2.5 ft/sec. Write an equation for time $s$ when they are at the same height.", "a": r"$48 - 3s = 2.5s$"},
        {"val": 800, "q": r"Maya has \$120 and deposits \$15/week ($120 + 15w$). Carlos has \$210 and withdraws \$10/week ($210 - 10w$). After how many weeks $w$ will they have equal money?", "a": r"3.6 weeks ($25w = 90 \implies w = 3.6$)"},
        {"val": 1000, "q": r"Without solving $5x + 14 = 2x - 7$, explain why $x$ must be negative.", "a": r"Subtracting $2x$ leaves $3x + 14 = -7$. Adding 14 to $3x$ yields a negative number, so $3x$ (and $x$) must be negative."}
    ]
}

# Session State Setup for 4 Teams
if "scores" not in st.session_state:
    st.session_state.scores = {"Team 1": 0, "Team 2": 0, "Team 3": 0, "Team 4": 0}
if "used_questions" not in st.session_state:
    st.session_state.used_questions = set()
if "active_q" not in st.session_state:
    st.session_state.active_q = None

st.title("🏆 Classroom Jeopardy!")

# Scoreboard Sidebar
st.sidebar.header("Scoreboard")
for team in st.session_state.scores:
    st.session_state.scores[team] = st.sidebar.number_input(
        f"{team}", value=st.session_state.scores[team], step=100
    )

if st.sidebar.button("Reset Game"):
    st.session_state.scores = {"Team 1": 0, "Team 2": 0, "Team 3": 0, "Team 4": 0}
    st.session_state.used_questions = set()
    st.session_state.active_q = None
    st.rerun()

# Active Question Screen
if st.session_state.active_q:
    q_data = st.session_state.active_q
    st.info(f"**Category:** {q_data['cat']} | **Value:** ${q_data['val']}")
    
    st.markdown(f"### {q_data['q']}")
    st.write("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Show Answer"):
            st.success(f"**Answer:** {q_data['a']}")
    
    st.write("### Award Points:")
    score_cols = st.columns(4)
    for idx, team in enumerate(st.session_state.scores):
        if score_cols[idx].button(f"+${q_data['val']} to {team}"):
            st.session_state.scores[team] += q_data['val']
            st.session_state.active_q = None
            st.rerun()
            
    if st.button("Close Question without Points"):
        st.session_state.active_q = None
        st.rerun()

else:
    # 5-Column Jeopardy Grid
    categories = list(JEOPARDY_DATA.keys())
    cols = st.columns(len(categories))

    for cat_idx, cat in enumerate(categories):
        with cols[cat_idx]:
            st.markdown(f"### {cat}")
            for q_idx, item in enumerate(JEOPARDY_DATA[cat]):
                q_id = f"{cat}_{q_idx}"
                if q_id in st.session_state.used_questions:
                    st.button(f"---", key=q_id, disabled=True, use_container_width=True)
                else:
                    if st.button(f"${item['val']}", key=q_id, use_container_width=True):
                        st.session_state.used_questions.add(q_id)
                        st.session_state.active_q = {**item, "cat": cat}
                        st.rerun()
