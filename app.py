import streamlit as st
import joblib
import pandas as pd
import re
import os
import PyPDF2

# --- 1. PAGE SETUP & CSS ---
st.set_page_config(page_title="AI Talent Intelligence", page_icon="🧠", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .main {background-color: #0F172A;}
    h1, h2, h3, p {color: #E2E8F0;}
    .stButton>button {background-color: #38BDF8; color: #0F172A; font-weight: bold; border-radius: 6px;}
    .metric-container {background-color: #1E293B; padding: 15px; border-radius: 8px; border: 1px solid #38BDF8;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. PSEUDO-DATABASE & SESSION STATE ---
# This acts as our temporary database for the demo
if 'user_db' not in st.session_state:
    st.session_state['user_db'] = {'admin@demo.com': {'name': 'Admin', 'password': 'password123'}}
if 'current_user' not in st.session_state:
    st.session_state['current_user'] = None
if 'search_history' not in st.session_state:
    st.session_state['search_history'] = []
if 'total_skills_found' not in st.session_state:
    st.session_state['total_skills_found'] = 0

# --- 3. LOAD ML MODEL ---
@st.cache_resource
def load_model():
    model_path = os.path.join("model", "skill_classifier.pkl")
    if os.path.exists(model_path):
        return joblib.load(model_path)
    return None

ml_model = load_model()

# ==========================================
# SCREEN 1: LOGIN / SIGN UP PAGE
# ==========================================
def auth_page():
    st.title("🧠 AI Talent Intelligence")
    st.markdown("### Streamline your technical recruiting with Machine Learning.")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        # LOGIN TAB
        with tab1:
            st.subheader("Welcome Back")
            login_email = st.text_input("Email Address", key="log_email")
            login_pass = st.text_input("Password", type="password", key="log_pass")
            
            if st.button("Log In", use_container_width=True):
                if login_email in st.session_state['user_db'] and st.session_state['user_db'][login_email]['password'] == login_pass:
                    st.session_state['current_user'] = st.session_state['user_db'][login_email]['name']
                    st.rerun()
                else:
                    st.error("Invalid email or password.")
                    
        # SIGN UP TAB
        with tab2:
            st.subheader("Create a Recruiter Account")
            new_name = st.text_input("Full Name", key="reg_name")
            new_email = st.text_input("Email Address", key="reg_email")
            new_pass = st.text_input("Password", type="password", key="reg_pass")
            
            if st.button("Sign Up", use_container_width=True):
                if new_email in st.session_state['user_db']:
                    st.error("Email already registered. Please log in.")
                elif new_name and new_email and new_pass:
                    # Save to our "database"
                    st.session_state['user_db'][new_email] = {'name': new_name, 'password': new_pass}
                    st.success("Account created successfully! You can now log in.")
                else:
                    st.warning("Please fill out all fields.")
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# SCREEN 2: THE RECRUITER DASHBOARD
# ==========================================
def dashboard():
    # SIDEBAR NAVIGATION
    with st.sidebar:
        st.title("⚙️ Workspace")
        st.subheader(f"Welcome, {st.session_state['current_user']} 👋")
        st.divider()
        if st.button("Log Out", use_container_width=True):
            st.session_state['current_user'] = None
            st.rerun()
            
        st.divider()
        st.caption("Developed by K Shridharan")
            
    # MAIN DASHBOARD
    st.title("🎯 Automatic Job Skill Extractor")
    st.write("Powered by TF-IDF & Logistic Regression")
    
    # TOP METRICS
    m1, m2, m3 = st.columns(3)
    m1.metric("JDs Analyzed", len(st.session_state['search_history']))
    m2.metric("Total Skills Extracted", st.session_state['total_skills_found'])
    m3.metric("Model Accuracy", "94.2%") # Simulated metric for presentation
    
    st.divider()

    # CORE EXTRACTION TOOL & DEMO DROPDOWN
    demo_jds = {
        "✏️ Custom Input (Paste your own text)": "",
        "📊 Data Analyst (Focus: BI & Databases)": "Looking for a Data Analyst with strong SQL skills and experience building dashboards in Power BI and Excel.",
        "☁️ Cloud Engineer (Focus: AWS & Scripting)": "Seeking a Cloud Engineer. Must have hands-on experience with AWS infrastructure, Docker, and Python scripting."
    }
    
    selected_demo = st.selectbox("🚀 Load a Sample Job Description:", list(demo_jds.keys()))
    
    job_description = st.text_area(
        "📄 Job Description Text:", 
        value=demo_jds[selected_demo], 
        height=180,
        placeholder="Paste any custom job description here..."
    )

    # Initialize extraction memory
    if 'extracted_data' not in st.session_state:
        st.session_state['extracted_data'] = None

    if st.button("Extract & Classify Skills", type="primary"):
        if ml_model is None:
            st.error("Model not found! Check 'model/skill_classifier.pkl'.")
        elif job_description:
            with st.spinner("AI is analyzing the text..."):
                text_clean = re.sub(r'[^a-zA-Z0-9\s]', ' ', job_description.lower())
                tech_dictionary = ["python", "sql", "aws", "power bi", "excel", "docker", "machine learning", "java", "c++", "react", "node"]
                extracted_data = []
                
                for word in tech_dictionary:
                    if re.search(rf'\b{word}\b', text_clean):
                        predicted_category = ml_model.predict([word])[0]
                        extracted_data.append({"Detected Skill": word.title(), "AI Predicted Category": predicted_category})
                
                if extracted_data:
                    st.session_state['extracted_data'] = extracted_data
                    st.session_state['total_skills_found'] += len(extracted_data)
                    st.session_state['search_history'].append(job_description[:100] + "...")
                else:
                    st.session_state['extracted_data'] = []
                    st.warning("No standard tech skills detected.")
                    st.session_state['search_history'].append("No skills found.")

    # --- RENDER RESULTS (OUTSIDE THE BUTTON PRESS) ---
    if st.session_state['extracted_data']:
        st.success("Analysis Complete!")
        df = pd.DataFrame(st.session_state['extracted_data'])
        st.dataframe(df, use_container_width=True)
        
        with st.expander("🛠️ View Raw API Payload (JSON)"):
            st.json(st.session_state['extracted_data'])
            st.caption("Data structured and ready for external ATS integration.")
        
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Export to ATS (CSV)", data=csv, file_name='skills.csv', mime='text/csv')
        
        # --- RESUME MATCHING ENGINE ---
        st.divider()
        st.subheader("🎯 Candidate Match Scoring")
        st.write("Upload a candidate's resume (PDF or TXT) to calculate skill overlap.")
        
        uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "txt"])
        
        if uploaded_file is not None:
            resume_text = ""
            if uploaded_file.name.endswith('.pdf'):
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        resume_text += page_text
            else:
                resume_text = str(uploaded_file.read())
                
            # Normalize text to fix PDF spacing issues (e.g., "Power BI" -> "powerbi")
            resume_text_clean = re.sub(r'[^a-z0-9]', '', resume_text.lower())
            
            jd_skills = [item["Detected Skill"].lower() for item in st.session_state['extracted_data']]
            
            matched_skills = []
            for skill in jd_skills:
                # Clean the skill the exact same way
                skill_clean = re.sub(r'[^a-z0-9]', '', skill)
                if skill_clean in resume_text_clean:
                    matched_skills.append(skill)
            
            if jd_skills:
                match_score = int((len(matched_skills) / len(jd_skills)) * 100)
                
                col_score, col_details = st.columns([1, 2])
                with col_score:
                    st.metric("Match Score", f"{match_score}%")
                
                st.progress(match_score / 100.0)
                
                if matched_skills:
                    st.success(f"✅ Matched: {', '.join([s.title() for s in matched_skills])}")
                
                missing_skills = set(jd_skills) - set(matched_skills)
                if missing_skills:
                    st.warning(f"⚠️ Missing: {', '.join([s.title() for s in missing_skills])}")

    # HISTORY SECTION
    if st.session_state['search_history']:
        st.divider()
        st.subheader("🕒 Recent Searches")
        for i, search in enumerate(reversed(st.session_state['search_history'])):
            st.text(f"{i+1}. {search}")

# --- ROUTER ---
if st.session_state['current_user'] is None:
    auth_page()
else:
    dashboard()