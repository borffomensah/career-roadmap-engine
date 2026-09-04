import streamlit as st
import requests

st.set_page_config(page_title="AI Career Roadmap Generator", layout="centered")

st.title("🎯 AI Career Roadmap Generator")
st.write("Tell us about your background and career ambition to get your single best-matched career path.")

# Supported tech keywords for validation
TECH_KEYWORDS = [
    "data", "machine learning", "ml", "ai", "artificial intelligence", "python", 
    "sql", "software", "web", "frontend", "backend", "full-stack", "fullstack", 
    "cloud", "devops", "design", "ui", "ux", "cybersecurity", "security", 
    "engineer", "engineering", "analytics", "rag", "econometrics", "quantitative"
]

# Sentence Form Questionnaire
user_sentence = st.text_area(
    "Describe your career goal, current skills, and preferences in full sentences:",
    height=120,
    placeholder="e.g., I want to become a Machine Learning Engineer. I currently know Python, SQL, and Statistics, and I prefer remote roles focused on MLOps and Model Deployment."
)

if st.button("Generate My Roadmap", type="primary"):
    query_text = user_sentence.strip().lower()
    
    if not query_text:
        st.warning("Please enter your career details above.")
    # Guardrail Check: Verify if prompt contains tech-related topics
    elif not any(keyword in query_text for keyword in TECH_KEYWORDS):
        st.warning(
            "⚠️ **Domain Restriction:** This roadmap generator currently specializes exclusively in "
            "**Tech, Data Science, Artificial Intelligence, Software Engineering, DevOps, Cybersecurity, and UX Design**.\n\n"
            "Non-tech career goals (such as Nursing, Medicine, Law, or Trades) are not in the current catalog. "
            "Please refine your prompt to focus on a tech or data role!"
        )
    else:
        with st.spinner("Analyzing vectors and building your roadmap..."):
            BACKEND_URL = "https://career-roadmap-backend-7e6h.onrender.com/recommend/"
            
            payload = {
                "goal": user_sentence,
                "skills": "",
                "preferences": "",
                "top_k": 1
            }
            
            try:
                res = requests.post(BACKEND_URL, json=payload)
                if res.status_code == 200:
                    data = res.json()[0]
                    
                    st.success(f"### Recommended Track: {data['title']}")
                    st.info(f"**Career Field:** {data['career_track']} | **Duration:** {data['roadmap']['estimated_duration']}")
                    st.write(f"**Summary:** {data['summary']}")
                    
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


# --- Main Page Discreet Footer / Author Imprint ---
st.markdown("---")
footer_col1, footer_col2 = st.columns([3, 1])

#with footer_col1:
    #st.markdown(
        #"<p style='font-size: 11px; color: #555555; margin: 0;'>"
        #"<b>Tweentech Technologies</b> &bull; Career Roadmap Generator."
        #"</p>", 
        #unsafe_allow_html=True
    #)

with footer_col2:
    st.markdown(
        "<p style='font-size: 11px; color: #777777; margin: 0; text-align: right;'>"
        "Engineered by <b>Daniel Borffo Mensah</b>"
        "</p>", 
        unsafe_allow_html=True
    )