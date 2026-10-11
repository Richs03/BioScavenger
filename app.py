import json
import subprocess
import requests
import streamlit as st

st.set_page_config(
    page_title="BioScavenger | Touch Grass Quest",
    page_icon="🌿",
    layout="centered",
)

# --- Session State Management ---
if "credits" not in st.session_state:
    st.session_state.credits = 0

if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "completed_tasks" not in st.session_state:
    st.session_state.completed_tasks = set()

if "quest_generated" not in st.session_state:
    st.session_state.quest_generated = False

# --- Top Header & Scoreboard ---
st.title("🌿 BioScavenger")
st.markdown(
    "**Screen-Free Sensory Quests.** Step away from displays, immerse your senses in nature, and earn Nature Credits."
)

st.metric(
    label="🏆 Nature Exploration Score",
    value=f"{st.session_state.credits} Credits",
)
st.divider()

# --- Quest Configuration Section ---
st.subheader("1. Configure Your Expedition")
col1, col2 = st.columns(2)
with col1:
    location = st.selectbox(
        "Select Environment",
        [
            "Urban Park",
            "Backyard / Garden",
            "College Campus",
            "Balcony / Rooftop",
            "Forest Trail",
        ],
    )
with col2:
    duration_min = st.selectbox(
        "Available Duration",
        [10, 15, 20, 30],
        format_func=lambda x: f"{x} Minutes",
    )

if st.button("🚀 Embark on Quest", type="primary"):
    with st.spinner("Generating sensory quest and synthesizing voice guide..."):
        prompt = f"""
        You are BioScavenger, an immersive mindfulness and outdoor nature guide.
        Generate 3 tactile, sensory, and observable nature challenges for a user situated at: {location} for {duration_min} minutes.
        At least one challenge must require finding a distinct tangible object (e.g., specific leaf shape, bark pattern, stone texture, or wild blossom).

        Create a rich, calming, descriptive narration script (around 70 to 90 words).
        Structure of narration:
        1. An opening mindfulness cue (e.g., take a slow deep breath, feel the outdoor air).
        2. Walk through the 3 challenges one after another in a serene tone.
        3. Instruct the explorer to put their device away in their pocket and return once complete.

        Return ONLY valid JSON matching this schema:
        {{
          "tasks": ["Challenge 1 description", "Challenge 2 description", "Challenge 3 description"],
          "narration": "Full spoken walkthrough script here."
        }}
        """

        try:
            # 1. Ollama LLM Call
            res = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "qwen2.5:3b",
                    "prompt": prompt,
                    "format": "json",
                    "stream": False,
                },
            )
            data = json.loads(res.json()["response"])
            narration = data.get(
                "narration",
                "Welcome outside. Take a gentle breath. Observe the flora around you, listen closely to the winds and birds, and collect your observations before returning.",
            )
            st.session_state.tasks = data.get("tasks", [])
            st.session_state.completed_tasks = set()
            st.session_state.quest_generated = True

            # 2. Piper Audio Synthesis Call
            proc = subprocess.Popen(
                [
                    "piper.exe",
                    "--model",
                    "en_US-lessac-medium.onnx",
                    "--output_file",
                    "quest.wav",
                ],
                stdin=subprocess.PIPE,
                text=True,
                encoding="utf-8",
            )
            proc.communicate(input=narration)

            st.rerun()

        except Exception as e:
            st.error(f"Failed to generate quest: {e}")

# --- Active Mission Section ---
if st.session_state.quest_generated and st.session_state.tasks:
    st.divider()
    st.subheader("2. Audio Briefing & Sensory Fieldwork")

    st.markdown(
        "> 🎧 **Audio Walkthrough:** Put on your earphones, press play below, and let the voice guide your outdoor exploration."
    )
    st.audio("quest.wav", format="audio/wav")

    st.info(
        f"📱 **Screen Lock Guidance:** After playing the audio briefing, pocket your phone for the next **{duration_min} minutes** to focus entirely on your surroundings."
    )

    st.subheader("3. Field Verification & Proof of Discovery")
    st.caption("Upload photographic evidence for each completed objective.")

    for idx, task in enumerate(st.session_state.tasks):
        is_done = idx in st.session_state.completed_tasks
        status_label = "✅ Completed (+50 Credits)" if is_done else "⏳ Pending"

        with st.expander(
            f"Objective {idx + 1}: {task} — {status_label}", expanded=not is_done
        ):
            if is_done:
                st.success(
                    "Objective verified and logged in your expedition journal."
                )
            else:
                uploaded_photo = st.file_uploader(
                    f"Upload photo documentation for Objective {idx + 1}",
                    type=["jpg", "png", "jpeg"],
                    key=f"file_{idx}",
                )

                if uploaded_photo is not None:
                    st.image(
                        uploaded_photo,
                        caption=f"Field Documentation: Objective {idx + 1}",
                        use_container_width=True,
                    )

                    if st.button(
                        f"Claim 50 Credits for Objective {idx + 1}",
                        key=f"claim_{idx}",
                    ):
                        st.session_state.credits += 50
                        st.session_state.completed_tasks.add(idx)
                        st.balloons()
                        st.rerun()

    # Expedition Completion Check
    if (
        len(st.session_state.completed_tasks) == len(st.session_state.tasks)
        and len(st.session_state.tasks) > 0
    ):
        st.success(
            "🎉 **Expedition Complete!** All objectives have been documented. You have successfully reconnected with the outdoors."
        )