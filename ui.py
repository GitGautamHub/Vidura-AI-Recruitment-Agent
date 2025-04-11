
import streamlit as st
import pandas as pd
import base64
import io
import matplotlib.pyplot as plt
import time
import requests
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

api_key = os.getenv("MAGIC_API_KEY")


def setup_page():
    """Apply custom CSS and setup page (without setting page config)"""
    # Apply custom CSS only
    apply_custom_css()
    
    # Add local logo handling via JavaScript
    st.markdown("""
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Try to load the logo, if it fails, show fallback text
            var logoImg = document.querySelector('.logo-image');
            if (logoImg) {
                logoImg.onerror = function() {
                    var logoContainer = document.querySelector('.logo-container');
                    if (logoContainer) {
                        logoContainer.innerHTML = '<div style="font-size: 40px;">🚀</div>';
                    }
                };
            }
        });
    </script>
    """, unsafe_allow_html=True)

def display_header():

    try:
        with open("vidura_logo.png", "rb") as img_file:
            logo_base64 = base64.b64encode(img_file.read()).decode()
            logo_html = f'<img src="data:image/jpeg;base64,{logo_base64}" alt="Vidura Logo" class="logo-image" style="max-height: 180px;">'
    except:
      
        logo_html = '<div style="font-size: 50px; text-align: center;">🚀</div>'

    st.markdown(f"""
    <div class="main-header">
        <div class="header-container">
            <div class="logo-container" style="text-align: center; margin-bottom: 20px;">
                {logo_html}
            </div>
            <div class="title-container" style="text-align: center;">
                <h1>Vidura: AI Recruitment Agent</h1>
                <p>Smart Resume Analysis & Interview Preparation System</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)



def apply_custom_css(accent_color="#d32f2f"):
    st.markdown(f"""
    <style>
        /* Main container */
        .main {{
            background-color: #000000 !important;
            color: white !important;
        }}

        /* Active tabs and highlights based on accent color */
        .stTabs [aria-selected=\"true\"] {{
            background-color: #000000 !important;
            border-bottom: 3px solid {accent_color} !important;
            color: {accent_color} !important;
        }}

        /* Buttons styled with accent color */
        .stButton button {{
            background-color: {accent_color} !important;
            color: white !important;
        }}

        .stButton button:hover {{
            filter: brightness(85%);
        }}

        /* Warning message */
        div.stAlert {{
            background-color: #4a0000 !important;
            color: white !important;
        }}

        /* Input fields */
        .stTextInput input, .stTextArea textarea, .stSelectbox div {{
            background-color: #222222 !important;
            color: white !important;
        }}

        /* Horizontal rule black and accent color gradient */
        hr {{
            border: none;
            height: 2px;
            background-image: linear-gradient(to right, black 50%, {accent_color} 50%);
        }}

        /* General markdown text */
        .stMarkdown, .stMarkdown p {{
            color: white !important;
        }}

        /* Skill tags styling */
        .skill-tag {{
            display: inline-block;
            background-color: {accent_color};
            color: white;
            padding: 5px 12px;
            border-radius: 15px;
            margin: 5px;
            font-weight: bold;
        }}

        .skill-tag.missing {{
            background-color: #444;
            color: #ccc;
        }}

        /* Horizontal layout for Strengths and Improvements */
        .strengths-improvements {{
            display: flex;
            gap: 20px;
        }}

        .strengths-improvements > div {{
            flex: 1;
        }}
        
        /* Card styling for sections */
        .card {{
            background-color: #111111;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            border-left: 4px solid {accent_color};
        }}
        
        /* Improvement suggestion styling */
        .improvement-item {{
            background-color: #222222;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
        }}
        
        /* Before-after comparison */
        .comparison-container {{
            display: flex;
            gap: 20px;
            margin-top: 15px;
        }}
        
        .comparison-box {{
            flex: 1;
            background-color: #333333;
            padding: 15px;
            border-radius: 5px;
        }}
        
        /* Weakness detail styling */
        .weakness-detail {{
            background-color: #330000;
            padding: 10px 15px;
            margin: 5px 0;
            border-radius: 5px;
            border-left: 3px solid #ff6666;
        }}
        
        /* Solution styling */
        .solution-detail {{
            background-color: #003300;
            padding: 10px 15px;
            margin: 5px 0;
            border-radius: 5px;
            border-left: 3px solid #66ff66;
        }}
        
        /* Example detail styling */
        .example-detail {{
            background-color: #000033;
            padding: 10px 15px;
            margin: 5px 0;
            border-radius: 5px;
            border-left: 3px solid #6666ff;
        }}
        
        /* Download button styling */
        .download-btn {{
            display: inline-block;
            background-color: {accent_color};
            color: white;
            padding: 8px 16px;
            border-radius: 5px;
            text-decoration: none;
            margin: 10px 0;
            text-align: center;
        }}
        
        .download-btn:hover {{
            filter: brightness(85%);
        }}
        
        /* Pie chart styling */
        .pie-chart-container {{
            padding: 10px;
            background-color: #111111;
            border-radius: 10px;
            margin-bottom: 15px;
        }}
    </style>
    """, unsafe_allow_html=True)




def setup_sidebar():
    with st.sidebar:
        st.markdown("## ⚙️ Settings")

        # Static theme color (black)
        theme_color = "#000000"
        st.markdown(
            f"""
            <style>
                .stButton button, .main-header, .stTabs [aria-selected="true"] {{
                    background-color: {theme_color} !important;
                    border-color: {theme_color} !important;
                }}
            </style>
            """, unsafe_allow_html=True
        )

        st.markdown("---")

        st.markdown("### 🧭 Navigation")
        st.markdown(
            """
            - **Resume Analysis**
            - **Resume Q&A**
            - **Interview Questions**
            - **Resume Improvement**
            - **Generate Improved Resume**
            - **AI Resume Extractor**
            """,
            unsafe_allow_html=True
        )

        st.markdown("---")

        st.markdown("### About Vidura")
        st.markdown(
            """
            **Vidura** is your AI-powered Recruitment Assistant:
             1. Analyze Resumes
             2. Understand Skill Gaps
             3. Generate Targeted Interview Questions
             4. Improve & Rebuild CVs

            Powered by GPT-4o and industry-grade parsing APIs.
            """,
            unsafe_allow_html=True
        )

        st.markdown("---")

        st.markdown(
            """
            <div style="text-align: center; margin-top: 20px; font-size: 0.85rem;">
                <strong>Vidura v1.0.0</strong><br>
                Made with ❤️ by Team KantaBai
            </div>
            """, unsafe_allow_html=True
        )

    return {
        "openai_api_key": api_key,  # Internally managed now
        "theme_color": theme_color
    }


def ai_resume_parser_tab():
    st.subheader("🧠 AI-Powered Resume Parser (SharpAPI)")
    uploaded_file = st.file_uploader("Upload your resume (PDF, DOCX, etc.)", type=["pdf", "doc", "docx", "txt"])

    if uploaded_file:
        api_key = st.secrets["magicapi_key"]  # You can set this in .streamlit/secrets.toml
        with st.spinner("Parsing resume..."):
            response = requests.post(
                url="https://api.magicapi.dev/api/v1/sharpapi.com/resume/api/v1/hr/parse_resume",
                headers={
                    "accept": "application/json",
                    "x-magicapi-key": api_key
                },
                files={"file": (uploaded_file.name, uploaded_file, "application/pdf")},
                data={"language": "English"}
            )

        if response.status_code == 200:
            parsed_data = response.json()["data"]["attributes"]["result"]
            st.success("✅ Resume Parsed Successfully!")
            st.json(parsed_data)
        else:
            st.error(f"❌ Error: {response.text}")


def role_selection_section(role_requirements):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        role = st.selectbox("Select the role you're applying for:", list(role_requirements.keys()))
    
    with col2:
        upload_jd = st.checkbox("Upload custom job description instead")
    
    custom_jd = None
    if upload_jd:
        custom_jd_file = st.file_uploader("Upload job description (PDF or TXT)", type=["pdf", "txt"])
        if custom_jd_file:
            st.success("Custom job description uploaded!")
            custom_jd = custom_jd_file
    
    if not upload_jd:
        st.info(f"Required skills: {', '.join(role_requirements[role])}")
        st.markdown(f"<p>Cutoff Score for selection: <b>{75}/100</b></p>", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return role, custom_jd



def resume_upload_section():
    st.markdown("""
    <div class="card">
        <h3>📄 Upload Your Resume</h3>
        <p>Supported format: PDF</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_resume = st.file_uploader("", type=["pdf"], label_visibility="collapsed")
    
    return uploaded_resume



def create_score_pie_chart(score):
    """Create a professional pie chart for the score visualization"""
    fig, ax = plt.subplots(figsize=(4, 4), facecolor='#111111')
    
    # Data
    sizes = [score, 100 - score]
    labels = ['', '']  # We'll use annotation instead
    colors = ["#d32f2f", "#333333"]
    explode = (0.05, 0)  # explode the 1st slice (Score)
    
    # Plot
    wedges, texts = ax.pie(
        sizes, 
        labels=labels, 
        colors=colors,
        explode=explode, 
        startangle=90,
        wedgeprops={'width': 0.5, 'edgecolor': 'black', 'linewidth': 1}
    )
    
    # Draw a circle in the center to make it a donut chart
    centre_circle = plt.Circle((0, 0), 0.25, fc='#111111')
    ax.add_artist(centre_circle)
    
    # Equal aspect ratio ensures that pie is drawn as a circle
    ax.set_aspect('equal')
    
    # Add score text in the center
    ax.text(0, 0, f"{score}%", 
            ha='center', va='center', 
            fontsize=24, fontweight='bold', 
            color='white')
    
    # Add pass/fail indicator
    status = "PASS" if score >= 75 else "FAIL"
    status_color = "#4CAF50" if score >= 75 else "#d32f2f"
    ax.text(0, -0.15, status, 
            ha='center', va='center', 
            fontsize=14, fontweight='bold', 
            color=status_color)
    
    # Set the background color
    ax.set_facecolor('#111111')
    
    return fig




def display_analysis_results(analysis_result):
    if not analysis_result:
        return

    overall_score = analysis_result.get('overall_score', 0)
    selected = analysis_result.get("selected", False)
    skill_scores = analysis_result.get("skill_scores", {})
    detailed_weaknesses = analysis_result.get("detailed_weaknesses", [])

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown(
        '<div style="text-align: right; font-size: 0.8rem; color: #888; margin-bottom: 10px;">Powered by Vidura AI Recruitment</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([1, 2])

    with col1:
        st.metric("Overall Score", f"{overall_score}/100")
        fig = create_score_pie_chart(overall_score)
        st.pyplot(fig)

    with col2:
        if selected:
            st.markdown("<h2 style='color:#4CAF50;'>✅ Congratulations! You have been shortlisted.</h2>", unsafe_allow_html=True)
        else:
            st.markdown("<h2 style='color:#d32f2f;'>❌ Unfortunately, you were not selected.</h2>", unsafe_allow_html=True)
        st.write(analysis_result.get('reasoning', ''))

    st.markdown('<hr>', unsafe_allow_html=True)

    st.markdown('<div class="strengths-improvements">', unsafe_allow_html=True)

    # Strengths
    st.markdown('<div>', unsafe_allow_html=True)
    st.subheader("🌟 Strengths")
    strengths = analysis_result.get("strengths", [])
    if strengths:
        for skill in strengths:
            st.markdown(f'<div class="skill-tag">{skill} ({skill_scores.get(skill, "N/A")}/10)</div>', unsafe_allow_html=True)
    else:
        st.write("No notable strengths identified.")
    st.markdown('</div>', unsafe_allow_html=True)

    # Weaknesses
    
    st.markdown('<div>', unsafe_allow_html=True)
    st.subheader("🚩 Areas for Improvement")
    missing_skills = analysis_result.get("missing_skills", [])
    if missing_skills:
        for skill in missing_skills:
            st.markdown(f'<div class="skill-tag missing">{skill} ({skill_scores.get(skill, "N/A")}/10)</div>', unsafe_allow_html=True)
    else:
        st.write("No significant areas for improvement.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    
    # Detailed weaknesses section
    if detailed_weaknesses:
        st.markdown('<hr>', unsafe_allow_html=True)
        st.subheader("📊 Detailed Weakness Analysis")
        
        for weakness in detailed_weaknesses:
            skill_name = weakness.get('skill', '')
            score = weakness.get('score', 0)
            
            with st.expander(f"{skill_name} (Score: {score}/10)"):
                # Clean detail display
                detail = weakness.get('detail', 'No specific details provided.')
                # Clean JSON formatting if it appears in the text
                if detail.startswith('```json') or '{' in detail:
                    detail = "The resume lacks examples of this skill."
                
                st.markdown(f'<div class="weakness-detail"><strong>Issue:</strong> {detail}</div>', 
                           unsafe_allow_html=True)
                
                # Display improvement suggestions if available
                if 'suggestions' in weakness and weakness['suggestions']:
                    st.markdown("<strong>How to improve:</strong>", unsafe_allow_html=True)
                    for i, suggestion in enumerate(weakness['suggestions']):
                        st.markdown(f'<div class="solution-detail">{i+1}. {suggestion}</div>', 
                                   unsafe_allow_html=True)
                
                # Display example if available
                if 'example' in weakness and weakness['example']:
                    st.markdown("<strong>Example addition:</strong>", unsafe_allow_html=True)
                    st.markdown(f'<div class="example-detail">{weakness["example"]}</div>', 
                               unsafe_allow_html=True)
    
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        report_content = f"""
# Vidura : AI Recruitment Agent

## Overall Score: {overall_score}/100

Status: {"✅ Shortlisted" if selected else "❌ Not Selected"}

## Analysis Reasoning
{analysis_result.get('reasoning', 'No reasoning provided.')}

## Strengths
{", ".join(strengths if strengths else ["None identified"])}

## Areas for Improvement
{", ".join(missing_skills if missing_skills else ["None identified"])}

## Detailed Weakness Analysis
"""
        # Add detailed weaknesses to report
        for weakness in detailed_weaknesses:
            skill_name = weakness.get('skill', '')
            score = weakness.get('score', 0)
            detail = weakness.get('detail', 'No specific details provided.')
            
            # Clean JSON formatting if it appears in the text
            if detail.startswith('```json') or '{' in detail:
                detail = "The resume lacks examples of this skill."
                
            report_content += f"\n### {skill_name} (Score: {score}/10)\n"
            report_content += f"Issue: {detail}\n"
            
            # Add suggestions to report
            if 'suggestions' in weakness and weakness['suggestions']:
                report_content += "\nImprovement suggestions:\n"
                for i, sugg in enumerate(weakness['suggestions']):
                    report_content += f"- {sugg}\n"
            
            # Add example to report
            if 'example' in weakness and weakness['example']:
                report_content += f"\nExample: {weakness['example']}\n"
            
        report_content += "\n---\nAnalysis provided by Vidura Recruitment Agent"
        
        report_b64 = base64.b64encode(report_content.encode()).decode()
        href = f'<a class="download-btn" href="data:text/plain;base64,{report_b64}" download="Vidura_resume_analysis.txt">📊 Download Analysis Report</a>'
        st.markdown(href, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


import streamlit as st
import requests
import time

import streamlit as st
import requests
import time

def ai_resume_parser_tab():
    st.markdown("## 🧠 AI-Powered Resume Parser (SharpAPI)")
    st.markdown("Upload your resume and let AI extract your professional journey in seconds.")

    uploaded_file = st.file_uploader(
        "📄 Upload your resume (PDF, DOC, DOCX, TXT)", 
        type=["pdf", "doc", "docx", "txt"]
    )

    if uploaded_file:
        api_key = "cm9csy3v50002l504kwgdbi28"  # Replace this if needed

        with st.spinner("📤 Uploading and parsing resume..."):
            try:
                # Step 1: Send resume to API
                response = requests.post(
                    url="https://api.magicapi.dev/api/v1/sharpapi.com/resume/api/v1/hr/parse_resume",
                    headers={
                        "accept": "application/json",
                        "x-magicapi-key": api_key
                    },
                    files={"file": (uploaded_file.name, uploaded_file, uploaded_file.type)},
                    data={"language": "English"}
                )

                if response.status_code in [200, 202]:
                    data = response.json()
                    job_id = data.get("job_id")
                    status_url = data.get("status_url")

                    st.info(f"⏳ Parsing started... **Job ID:** `{job_id}`")

                    # Fallback URL fix
                    if not status_url or "api.market" in status_url:
                        status_url = f"https://api.magicapi.dev/api/v1/sharpapi.com/resume/api/v1/hr/parse_resume/job/status/{job_id}"
                        st.warning("⚠️ Status URL fallback applied.")

                    # Step 2: Poll result
                    for attempt in range(10):
                        time.sleep(2)
                        poll = requests.get(status_url, headers={"x-magicapi-key": api_key})

                        if poll.status_code == 200:
                            parsed = poll.json()
                            status = parsed["data"]["attributes"]["status"]

                            if status == "success":
                                result = parsed["data"]["attributes"]["result"]
                                st.success("✅ Resume Parsed Successfully!")

                                # Pretty print
                                st.markdown("### 👤 Candidate Details")
                                st.write(f"**Name:** {result.get('candidate_name', '-')}")
                                st.write(f"**Email:** {result.get('candidate_email', '-')}")
                                st.write(f"**Phone:** {result.get('candidate_phone', '-')}")
                                st.write(f"**Address:** {result.get('candidate_address', '-')}")

                                st.markdown("### 🎓 Education")
                                education = result.get("education_qualifications", [])
                                if education:
                                    for edu in education:
                                        st.write(f"- {edu['degree_type']} from **{edu['school_name']}**")
                                        st.caption(f"{edu['start_date']} to {edu['end_date']} | {edu['faculty_department']}")
                                else:
                                    st.warning("No education info found.")

                                st.markdown("### 💼 Work Experience")
                                jobs = result.get("positions", [])
                                if jobs:
                                    for job in jobs:
                                        st.write(f"**{job['position_name']}** at {job['company_name']}")
                                        st.caption(f"{job['start_date']} to {job.get('end_date', 'Present')}")
                                        st.markdown(f"*{job['job_details']}*")
                                else:
                                    st.warning("No job positions found.")

                                return
                        elif poll.status_code == 404:
                            st.warning(f"⚠️ Attempt {attempt + 1}/10: Status 404 - Not ready yet")
                        elif poll.status_code == 401:
                            st.error("❌ Invalid API Key (401)")
                            return
                        elif poll.status_code == 402:
                            st.error("❌ Payment Required / Monthly quota exceeded (402)")
                            return
                        else:
                            st.warning(f"⏳ Attempt {attempt + 1}/10: Still waiting...")

                    st.error("❌ Parsing took too long. Please try again later.")
                else:
                    st.error(f"❌ Upload failed. API Response: `{response.status_code}` {response.text}")

            except Exception as e:
                st.error(f"🚨 Unexpected Error: {str(e)}")


def resume_qa_section(has_resume, ask_question_func=None):
    if not has_resume:
        st.warning("Please upload and analyze a resume first.")
        return
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    st.subheader("Ask Questions About the Resume")
    user_question = st.text_input("Enter your question about the resume:", placeholder="What is the candidate's most recent experience?")
    
    if user_question and ask_question_func:
        with st.spinner("Searching resume and generating response..."):
            response = ask_question_func(user_question)
            
            st.markdown('<div style="background-color: #111122; padding: 15px; border-radius: 5px; border-left: 5px solid #d32f2f;">', unsafe_allow_html=True)
            st.write(response)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Add example questions
    with st.expander("Example Questions"):
        example_questions = [
            "What is the candidate's most recent role?",
            "How many years of experience does the candidate have with Python?",
            "What educational qualifications does the candidate have?",
            "What are the candidate's key achievements?",
            "Has the candidate managed teams before?",
            "What projects has the candidate worked on?",
            "Does the candidate have experience with cloud technologies?"
        ]
        
        for question in example_questions:
            if st.button(question, key=f"q_{question}"):
                st.session_state.current_question = question
                st.experimental_rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def interview_questions_section(has_resume, generate_questions_func=None):
    if not has_resume:
        st.warning("Please upload and analyze a resume first.")
        return
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        question_types = st.multiselect(
            "Select question types:",
            ["Basic", "Technical", "Experience", "Scenario", "Coding", "Behavioral"],
            default=["Basic", "Technical"]
        )
    
    with col2:
        difficulty = st.select_slider(
            "Question difficulty:",
            options=["Easy", "Medium", "Hard"],
            value="Medium"
        )
    
    num_questions = st.slider("Number of questions:", 3, 15, 5)
    
    if st.button("Generate Interview Questions"):
        if generate_questions_func:
            with st.spinner("Generating personalized interview questions..."):
                questions = generate_questions_func(question_types, difficulty, num_questions)
                
                # Create content for download
                download_content = f"# Vidura AI Recruitment - Interview Questions\n\n"
                download_content += f"Difficulty: {difficulty}\n"
                download_content += f"Types: {', '.join(question_types)}\n\n"
                
                for i, (q_type, question) in enumerate(questions):
                    with st.expander(f"{q_type}: {question[:50]}..."):
                        st.write(question)
                        
                        # For coding questions, add code editor
                        if q_type == "Coding":
                            st.code("# Write your solution here", language="python")
                    
                    # Add to download content
                    download_content += f"## {i+1}. {q_type} Question\n\n"
                    download_content += f"{question}\n\n"
                    if q_type == "Coding":
                        download_content += "```python\n# Write your solution here\n```\n\n"
                
                # Add Vidura branding to download content
                download_content += "\n---\nQuestions generated by Vidura AI Recruitment Agent"
                
                # Add download button
                if questions:
                    st.markdown("---")
                    questions_bytes = download_content.encode()
                    b64 = base64.b64encode(questions_bytes).decode()
                    href = f'<a class="download-btn" href="data:text/markdown;base64,{b64}" download="Vidura_interview_questions.md">📝 Download All Questions</a>'
                    st.markdown(href, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def resume_improvement_section(has_resume, improve_resume_func=None):
    if not has_resume:
        st.warning("Please upload and analyze a resume first.")
        return
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    improvement_areas = st.multiselect(
        "Select areas to improve:",
        ["Content", "Format", "Skills Highlighting", "Experience Description", "Education", "Projects", "Achievements", "Overall Structure"],
        default=["Content", "Skills Highlighting"]
    )
    
    target_role = st.text_input("Target role (optional):", placeholder="e.g., Senior Data Scientist at Google")
    
    if st.button("Generate Resume Improvements"):
        if improve_resume_func:
            with st.spinner("Analyzing and generating improvements..."):
                improvements = improve_resume_func(improvement_areas, target_role)
                
                # Create content for download
                download_content = f"# Vidura AI Recruitment - Resume Improvement Suggestions\n\nTarget Role: {target_role if target_role else 'Not specified'}\n\n"
                
                for area, suggestions in improvements.items():
                    with st.expander(f"Improvements for {area}", expanded=True):
                        st.markdown(f"<p>{suggestions['description']}</p>", unsafe_allow_html=True)
                        
                        st.subheader("Specific Suggestions")
                        for i, suggestion in enumerate(suggestions["specific"]):
                            st.markdown(f'<div class="solution-detail"><strong>{i+1}.</strong> {suggestion}</div>', unsafe_allow_html=True)
                        
                        if "before_after" in suggestions:
                            st.markdown('<div class="comparison-container">', unsafe_allow_html=True)
                            
                            st.markdown('<div class="comparison-box">', unsafe_allow_html=True)
                            st.markdown("<strong>Before:</strong>", unsafe_allow_html=True)
                            st.markdown(f"<pre>{suggestions['before_after']['before']}</pre>", unsafe_allow_html=True)
                            st.markdown('</div>', unsafe_allow_html=True)
                            
                            st.markdown('<div class="comparison-box">', unsafe_allow_html=True)
                            st.markdown("<strong>After:</strong>", unsafe_allow_html=True) 
                            st.markdown(f"<pre>{suggestions['before_after']['after']}</pre>", unsafe_allow_html=True)
                            st.markdown('</div>', unsafe_allow_html=True)
                            
                            st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Add to download content
                    download_content += f"## Improvements for {area}\n\n"
                    download_content += f"{suggestions['description']}\n\n"
                    download_content += "### Specific Suggestions\n\n"
                    for i, suggestion in enumerate(suggestions["specific"]):
                        download_content += f"{i+1}. {suggestion}\n"
                    download_content += "\n"
                    
                    if "before_after" in suggestions:
                        download_content += "### Before\n\n"
                        download_content += f"```\n{suggestions['before_after']['before']}\n```\n\n"
                        download_content += "### After\n\n"
                        download_content += f"```\n{suggestions['before_after']['after']}\n```\n\n"
                
                # Add Vidura branding to download content
                download_content += "\n---\nProvided by Vidura AI Recruitment Agent"
                
                # Add download button
                st.markdown("---")
                report_bytes = download_content.encode()
                b64 = base64.b64encode(report_bytes).decode()
                href = f'<a class="download-btn" href="data:text/markdown;base64,{b64}" download="Vidura_resume_improvements.md">📝 Download All Suggestions</a>'
                st.markdown(href, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def improved_resume_section(has_resume, get_improved_resume_func=None):
    if not has_resume:
        st.warning("Please upload and analyze a resume first.")
        return
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    target_role = st.text_input("Target role:", placeholder="e.g., Senior Software Engineer")
    highlight_skills = st.text_area("Paste your JD to get updated Resume", placeholder="e.g., Python, React, Cloud Architecture")
    
    if st.button("Generate Improved Resume"):
        if get_improved_resume_func:
            with st.spinner("Creating improved resume..."):
                improved_resume = get_improved_resume_func(target_role, highlight_skills)
                
                st.subheader("Improved Resume")
                st.text_area("", improved_resume, height=400)
                
                # Download buttons
                col1, col2 = st.columns(2)
                
                with col1:
                    # Text file download
                    resume_bytes = improved_resume.encode()
                    b64 = base64.b64encode(resume_bytes).decode()
                    href = f'<a class="download-btn" href="data:file/txt;base64,{b64}" download="Vidura_improved_resume.txt">📄 Download as TXT</a>'
                    st.markdown(href, unsafe_allow_html=True)
                
                with col2:
                    # Markdown file download
                    md_content = f"""# {target_role if target_role else 'Professional'} Resume

{improved_resume}

---
Resume enhanced by Vidura Recruitment Agent
"""
                    md_bytes = md_content.encode()
                    md_b64 = base64.b64encode(md_bytes).decode()
                    md_href = f'<a class="download-btn" href="data:text/markdown;base64,{md_b64}" download="Vidura_improved_resume.md">📝 Download as Markdown</a>'
                    st.markdown(md_href, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def create_tabs():
    return st.tabs([
        "Resume Analysis", 
        "Resume Q&A", 
        "Interview Questions", 
        "Resume Improvement", 
        "Improved Resume",
        "AI Resume Extractor"
    ])