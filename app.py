import streamlit as st
import datetime
import time

# Page configuration
st.set_page_config(page_title="FocusLock - Mindful Friction Tool", page_icon="🎯", layout="centered")

# App Header
st.title("🎯 FocusLock")
st.subheader("The 'Mindful Friction' Productivity Tool")
st.write("Traditional blockers fail. FocusLock makes you justify your distractions, building real self-awareness.")

# Initialize Session States to store data during the run
if "sprint_active" not in st.session_state:
    st.session_state.sprint_active = False
if "current_task" not in st.session_state:
    st.session_state.current_task = ""
if "excuse_log" not in st.session_state:
    st.session_state.excuse_log = []

# --- SCREEN 1: TASK SETTER ---
if not st.session_state.sprint_active:
    st.write("---")
    st.markdown("### 🚀 Start a Deep Work Sprint")
    task = st.text_input("What specific productive task are you working on right now?", placeholder="e.g., Writing Chapter 1, Coding login page...")
    duration = st.slider("Sprint Duration (Minutes)", min_value=5, max_value=60, value=25, step=5)
    
    if st.button("Start Focus Sprint", type="primary"):
        if task.strip() == "":
            st.error("Please enter a valid task before starting!")
        else:
            st.session_state.sprint_active = True
            st.session_state.current_task = task
            st.session_state.start_time = datetime.datetime.now()
            st.rerun()

# --- SCREEN 2: ACTIVE SPRINT & INTERCEPTOR ---
else:
    st.write("---")
    st.success(f"⚡ **Active Sprint:** Working on *'{st.session_state.current_task}'*")
    st.info("Status: Focus Mode Active. Do not switch tabs!")
    
    st.markdown("### ⚠️ Simulate a Distraction Intercept")
    st.write("In the full product, this overlay triggers automatically when you visit Facebook/YouTube. Try it below:")
    
    distracting_site = st.selectbox("Where are you trying to sneak away to?", ["Select a distraction...", "YouTube", "Instagram", "Twitter/X", "Netflix", "Online Shopping"])
    
    if distracting_site != "Select a distraction...":
        st.markdown(f"<div style='background-color:#ffe6e6; padding:15px; border-radius:10px; border-left:5px solid #ff4d4d;'>"
                    f"<h4>🛑 HOLD ON!</h4>"
                    f"<p>You committed to working on: <strong>{st.session_state.current_task}</strong>.</p>"
                    f"<p>Why do you need to visit <strong>{distracting_site}</strong> right now?</p>"
                    f"</div>", unsafe_allow_html=True)
        
        user_excuse = st.text_input("Type your honest excuse (Minimum 10 characters to unlock):", key="excuse_input")
        
        if st.button("Submit Excuse & Force Unlock"):
            if len(user_excuse) < 10:
                st.error("Too short! Be honest with yourself. Type a real reason.")
            else:
                log_entry = {
                    "time": datetime.datetime.now().strftime("%H:%M:%S"),
                    "task": st.session_state.current_task,
                    "site": distracting_site,
                    "excuse": user_excuse
                }
                st.session_state.excuse_log.append(log_entry)
                st.balloons()
                st.success(f"Unlocked {distracting_site} for 10 minutes. Distraction logged in your Mirror Dashboard.")
                time.sleep(2)
                st.rerun()
                
    if st.button("End Focus Sprint Successfully", type="secondary"):
        st.session_state.sprint_active = False
        st.success("Great job on finishing your sprint!")
        time.sleep(1.5)
        st.rerun()

# --- SCREEN 3: THE MIRROR DASHBOARD ---
if st.session_state.excuse_log:
    st.write("---")
    st.markdown("### 📊 The Mirror Dashboard (Your Self-Awareness Data)")
    st.write("Here are the excuses you gave to yourself today. Look at them and reflect:")
    
    for log in st.session_state.excuse_log:
        st.markdown(f"⏱️ **{log['time']}** — Tried to open **{log['site']}** while working on *'{log['task']}'*.\n"
                    f"🗣️ *Your Excuse:* \"{log['excuse']}\"")
