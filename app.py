import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# --- 1. FIREBASE INITIALIZATION ---
if not firebase_admin._apps:
    try:
        firebase_config = dict(st.secrets["firebase"])
        cred = credentials.Certificate(firebase_config)
        firebase_admin.initialize_app(cred)
    except Exception:
        pass

db = firestore.client() if firebase_admin._apps else None

# --- 2. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="RozgarWFH - India's Trusted Verified Work From Home Jobs",
    page_icon="💻",
    layout="wide"
)

st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stButton>button { width: 100%; border-radius: 10px; background-color: #4f46e5; color: white; font-weight: bold; }
    .stButton>button:hover { background-color: #4338ca; color: white; }
    </style>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE MANAGEMENT ---
if "user" not in st.session_state:
    st.session_state.user = None
if "page" not in st.session_state:
    st.session_state.page = "jobs"

# Expanded Initial Sample Jobs (Including Science, Education, & Healthcare)
INITIAL_JOBS = [
    {
        "title": "Senior AI Research Scientist (Remote)",
        "company": "Bharat DeepTech Labs",
        "location": "Remote - PAN India",
        "type": "Full-Time",
        "salary": "₹25 LPA - ₹40 LPA",
        "category": "Scientists",
        "posted": "1 hour ago",
        "description": "Lead cutting-edge research in large language models and computer vision. PhD or Master's in Computer Science/AI required.",
        "requirements": ["PhD or M.Tech in AI/ML", "Strong publication record", "Expertise in PyTorch / Python"]
    },
    {
        "title": "Online Professor / Subject Matter Expert (Physics/Maths)",
        "company": "Global Virtual University",
        "location": "Remote - Flexible",
        "type": "Part-Time",
        "salary": "₹1.2 LPA / month",
        "category": "Professors",
        "posted": "3 hours ago",
        "description": "Deliver online masterclasses, curate advanced curriculum, and mentor postgraduate students globally.",
        "requirements": ["Postgraduate degree / Doctorate in relevant field", "5+ years teaching experience",
                         "Excellent online presentation skills"]
    },
    {
        "title": "Digital Healthcare Executive & Tele-Consultation Lead",
        "company": "MediConnect Remote India",
        "location": "Remote - Delhi NCR / Mumbai",
        "type": "Full-Time",
        "salary": "₹10 LPA - ₹15 LPA",
        "category": "Health Executives",
        "posted": "Yesterday",
        "description": "Manage digital health operations, coordinate with remote medical practitioners, and oversee patient care protocols.",
        "requirements": ["Degree in Healthcare Management / Life Sciences", "3+ years healthcare admin experience",
                         "Strong communication skills"]
    },
    {
        "title": "Senior Online Educator & Curriculum Designer",
        "company": "EdVenture India Academy",
        "location": "Remote - PAN India",
        "type": "Full-Time",
        "salary": "₹8 LPA - ₹12 LPA",
        "category": "Teachers",
        "posted": "2 days ago",
        "description": "Design interactive remote learning modules and teach live online classes for senior secondary students.",
        "requirements": ["B.Ed / M.Ed or Master's degree", "Passion for digital teaching",
                         "Engaging storytelling and teaching style"]
    },
    {
        "title": "Remote Frontend Developer (React.js)",
        "company": "TechNova Solutions India",
        "location": "Remote - India",
        "type": "Full-Time",
        "salary": "₹12 LPA - ₹18 LPA",
        "category": "IT & Software",
        "posted": "2 days ago",
        "description": "Looking for an experienced React developer to build scalable SaaS dashboards. Must have reliable broadband setup.",
        "requirements": ["2+ years experience in React & Tailwind CSS", "Strong proficiency in REST APIs"]
    },
    {
        "title": "Remote Customer Success Executive",
        "company": "Zomato Support Hub",
        "location": "Remote - Haryana / Delhi",
        "type": "Full-Time",
        "salary": "₹4.5 LPA - ₹6 LPA",
        "category": "Customer Support",
        "posted": "3 days ago",
        "description": "Handle inbound customer queries via chat and email. Complete remote training provided.",
        "requirements": ["Graduate in any discipline", "Fluent in English & Hindi", "Quiet workspace & headset"]
    }
]


def get_jobs_from_firestore():
    if not db:
        return INITIAL_JOBS
    try:
        jobs_ref = db.collection("jobs")
        docs = list(jobs_ref.stream())
        if not docs:
            for job in INITIAL_JOBS:
                jobs_ref.add(job)
            return INITIAL_JOBS
        return [{**doc.to_dict(), "id": doc.id} for doc in docs]
    except Exception as e:
        st.error(f"Database error: {e}")
        return INITIAL_JOBS


# --- 4. HEADER / NAVBAR ---
col1, col2, col3 = st.columns([3, 4, 3])
with col1:
    st.markdown("### 💻 Rozgar<span style='color:#4f46e5;'>WFH</span>", unsafe_allow_html=True)
    st.caption("100% Verified Remote Jobs in India")

with col3:
    if st.session_state.user:
        if st.button("👤 My Profile & Vault"):
            st.session_state.page = "profile"
        if st.button("🚪 Logout"):
            st.session_state.user = None
            st.session_state.page = "jobs"
            st.rerun()
    else:
        if st.button("🔑 Candidate Login / Register"):
            st.session_state.page = "auth"

st.divider()

# --- 5. PAGE: AUTHENTICATION ---
if st.session_state.page == "auth":
    st.markdown("## 🔐 Candidate Registration / Login")
    st.write("Create your account securely using Email & Password to apply for jobs and manage documents.")

    with st.form("auth_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        mobile = st.text_input("Mobile Number (10 digits)")

        submitted = st.form_submit_button("Register & Proceed")
        if submitted:
            if name and email and mobile:
                st.session_state.user = {
                    "name": name,
                    "email": email,
                    "mobile": mobile,
                    "resume": None,
                    "certificates": []
                }
                st.success(f"Welcome, {name}! Account created successfully.")
                st.session_state.page = "jobs"
                st.rerun()
            else:
                st.warning("Please fill in all fields.")

# --- 6. PAGE: CANDIDATE PROFILE & DOCUMENT VAULT ---
elif st.session_state.page == "profile":
    user = st.session_state.user
    st.markdown(f"## 👤 Candidate Dashboard: {user['name']}")

    col_a, col_b = st.columns(2)
    with col_a:
        st.info(f"**Email:** {user['email']}\n\n**Mobile:** +91 {user['mobile']}\n\n**Account Status:** Verified")

    with col_b:
        st.markdown("### 📂 Document & Resume Vault")
        resume_file = st.file_uploader("Upload Resume / CV (PDF / DOCX)", type=["pdf", "docx"])
        if resume_file:
            user["resume"] = resume_file.name
            st.success(f"Resume '{resume_file.name}' uploaded successfully!")

        cert_file = st.file_uploader("Upload Qualification Degree / Certificate", type=["pdf", "jpg", "png"])
        if cert_file:
            user["certificates"].append(cert_file.name)
            st.success(f"Certificate '{cert_file.name}' added to vault!")

    st.markdown("---")
    st.markdown("### 📋 Tracked Job Applications")

    if db:
        try:
            apps_ref = db.collection("applications").where("applicantEmail", "==", user["email"]).stream()
            apps = [doc.to_dict() for doc in apps_ref]
            if apps:
                for app in apps:
                    st.markdown(f"""
                        <div style="background:white; padding:15px; border-radius:10px; border:1px solid #e2e8f0; margin-bottom:10px;">
                            <strong>{app['jobTitle']}</strong> at {app['company']}<br>
                            <span style="color:#d97706; font-size:12px;">Status: {app['status']}</span> | 
                            <span style="color:#64748b; font-size:12px;">Applied on: {app['appliedAt']}</span>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("You haven't applied to any jobs yet.")
        except Exception:
            st.info("No applications found.")
    else:
        st.info("Database connection required to view tracked applications.")

    if st.button("⬅️ Back to Job Search"):
        st.session_state.page = "jobs"
        st.rerun()

# --- 7. PAGE: JOB SEARCH & LISTINGS ---
elif st.session_state.page == "jobs":
    st.markdown("## 🔎 Active Remote Openings in India")

    # Search and Filter bar (with expanded categories)
    search_query = st.text_input("Search job title, skills, or company...", "")
    category = st.selectbox(
        "Filter by Category",
        [
            "All",
            "Scientists",
            "Professors",
            "Health Executives",
            "Teachers",
            "IT & Software",
            "Customer Support",
            "Content & Writing",
            "Data & Analytics",
            "Digital Marketing"
        ]
    )

    jobs = get_jobs_from_firestore()

    # Filter jobs logic
    filtered_jobs = []
    for job in jobs:
        matches_query = search_query.lower() in job["title"].lower() or search_query.lower() in job["company"].lower()
        matches_cat = category == "All" or job.get("category") == category
        if matches_query and matches_cat:
            filtered_jobs.append(job)

    st.write(f"Showing **{len(filtered_jobs)}** verified remote openings:")

    for job in filtered_jobs:
        with st.container():
            st.markdown(f"""
                <div style="background:white; padding:20px; border-radius:15px; border:1px solid #e2e8f0; margin-bottom:15px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                    <span style="background:#e0e7ff; color:#3730a3; padding:4px 10px; border-radius:6px; font-size:12px; font-weight:bold;">{job.get('category', 'Remote')}</span>
                    <span style="background:#d1fae5; color:#065f46; padding:4px 10px; border-radius:6px; font-size:12px; font-weight:bold; margin-left:8px;">✓ Verified</span>
                    <h3 style="margin-top:10px; margin-bottom:5px; color:#1e293b;">{job['title']}</h3>
                    <p style="color:#64748b; font-size:14px; margin-bottom:10px;">🏢 {job['company']}  |  📍 {job['location']}</p>
                    <p style="font-weight:600; color:#0f172a;">💰 {job['salary']}  •  🕒 {job['type']}</p>
                    <p style="color:#334155; font-size:14px;">{job['description']}</p>
                </div>
            """, unsafe_allow_html=True)

            if st.button(f"Apply Now for {job['title']}", key=job.get('id', job['title'])):
                if not st.session_state.user:
                    st.warning("Please register or login first to submit your application.")
                    st.session_state.page = "auth"
                    st.rerun()
                else:
                    user = st.session_state.user
                    if db:
                        try:
                            db.collection("applications").add({
                                "jobTitle": job["title"],
                                "company": job["company"],
                                "location": job["location"],
                                "salary": job["salary"],
                                "applicantName": user["name"],
                                "applicantEmail": user["email"],
                                "applicantMobile": user["mobile"],
                                "resumeFileName": user["resume"] or "No resume attached",
                                "status": "Under Review",
                                "appliedAt": "Today"
                            })
                            st.success(f"Application submitted successfully to {job['company']}!")
                        except Exception as e:
                            st.error(f"Error submitting application: {e}")
                    else:
                        st.success(f"Application simulated successfully for {user['name']}!")
            st.divider()