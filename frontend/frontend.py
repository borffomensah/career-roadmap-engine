import streamlit as st
import requests

st.set_page_config(page_title="AI Career Roadmap Generator", layout="centered")

st.title("🎯 AI Career Roadmap Generator")
st.write("Tell us about your background and career ambition to get your single best-matched career path.")

# Sentence Form Questionnaire
user_sentence = st.text_area(
    "Describe your career goal, current skills, and preferences in full sentences:",
    height=120,
    placeholder="e.g., I want to become a Machine Learning Engineer. I currently know Python, SQL, and Statistics, and I prefer remote roles focused on MLOps and Model Deployment."
)

if st.button("Generate My Roadmap", type="primary"):
    if not user_sentence.strip():
        st.warning("Please enter your career details above.")
    else:
        with st.spinner("Analyzing vectors and building your roadmap..."):
            # Local backend URL for testing (will update after Render deployment)
            BACKEND_URL = "http://127.0.0.1:8000/recommend/"
            
            payload = {
                "goal": user_sentence,
                "skills": "",
                "preferences": "",
                "top_k": 1  # Returns a single top match
            }
            
            try:
                res = requests.post(BACKEND_URL, json=payload)
                if res.status_code == 200:
                    data = res.json()[0]  # Get top recommendation
                    
                    # ⚠️ GUARDRAIL: Check if vector similarity match score meets the threshold
                    if data['match_score'] < 50.0:
                        st.warning(
                            f"⚠️ **Low Match Score ({data['match_score']}%):** "
                            "No closely matching tech career track was found for your request. "
                            "Please refine your query to focus on tech, data science, software, or design roles."
                        )
                    else:
                        st.success(f"### Recommended Track: {data['title']} ({data['match_score']}% Match)")
                        st.info(f"**Career Field:** {data['career_track']} | **Duration:** {data['roadmap']['estimated_duration']}")
                        
                        st.markdown("---")
                        st.subheader("📍 Your Phase-by-Phase Roadmap")
                        
                        for phase in data['roadmap']['phases']:
                            with st.expander(f"🔹 {phase['phase']}: {phase['focus']}", expanded=True):
                                st.write(f"**Key Toolstack:** {', '.join(phase['key_skills'])}")
                                st.write(f"🎯 **Milestone:** {phase['milestone']}")
                else:
                    st.error("Failed to generate roadmap. Please try again.")
            except Exception as e:
                st.error(f"Could not connect to server: {e}")