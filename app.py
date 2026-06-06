import streamlit as st
import pandas as pd
import joblib

st.set_page_config(
    page_title="Student Mental Health Risk Screening",
    page_icon="🌿",
    layout="wide"
)

st.markdown("""
<style>
    /* Main background - stronger contrast */
    .stApp {
        background:
            radial-gradient(circle at top left, rgba(197, 229, 220, 0.75), transparent 34%),
            radial-gradient(circle at top right, rgba(207, 221, 245, 0.55), transparent 30%),
            linear-gradient(135deg, #DDEFEA 0%, #EAF4F1 45%, #DCE8F4 100%);
        color: #263648;
    }

    /* Main container */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1180px;
    }

    /* Hero section */
    .hero-card {
        background: linear-gradient(135deg, #FFFFFF 0%, #F7FFFC 100%);
        padding: 42px 46px;
        border-radius: 30px;
        box-shadow: 0px 18px 45px rgba(63, 111, 103, 0.20);
        border: 1px solid rgba(118, 183, 168, 0.25);
        margin-bottom: 30px;
    }

    .hero-title {
        font-size: 44px;
        font-weight: 850;
        color: #24364B;
        line-height: 1.15;
        margin-bottom: 14px;
        letter-spacing: -0.5px;
    }

    .hero-subtitle {
        font-size: 17px;
        color: #607286;
        line-height: 1.7;
        max-width: 900px;
        margin-bottom: 20px;
    }

    .badge {
        display: inline-block;
        background-color: #DDEFEA;
        color: #315F57;
        padding: 9px 15px;
        border-radius: 999px;
        font-size: 13px;
        font-weight: 800;
        margin-right: 8px;
        margin-top: 8px;
        border: 1px solid rgba(118, 183, 168, 0.28);
    }

    /* Section */
    .section-title {
        font-size: 30px;
        font-weight: 850;
        color: #24364B;
        margin-top: 14px;
        margin-bottom: 6px;
        letter-spacing: -0.2px;
    }

    .section-subtitle {
        font-size: 15px;
        color: #5F7185;
        margin-bottom: 24px;
    }

    .note-card {
        background: rgba(255, 255, 255, 0.72);
        color: #294B49;
        padding: 19px 23px;
        border-radius: 20px;
        border-left: 7px solid #6FAFA3;
        font-size: 15px;
        line-height: 1.65;
        margin-bottom: 30px;
        box-shadow: 0px 10px 28px rgba(63, 111, 103, 0.10);
    }

    /* Result cards */
    .result-card-low {
        background: linear-gradient(135deg, #DFF3E4 0%, #F7FFF8 100%);
        color: #24553A;
        padding: 26px;
        border-radius: 24px;
        border-left: 8px solid #7FB77E;
        box-shadow: 0px 12px 28px rgba(127, 183, 126, 0.18);
        margin-bottom: 18px;
    }

    .result-card-moderate {
        background: linear-gradient(135deg, #FFF4D6 0%, #FFFDF6 100%);
        color: #6A5228;
        padding: 26px;
        border-radius: 24px;
        border-left: 8px solid #D6B35A;
        box-shadow: 0px 12px 28px rgba(214, 179, 90, 0.18);
        margin-bottom: 18px;
    }

    .result-card-high {
        background: linear-gradient(135deg, #FDE2E2 0%, #FFFAFA 100%);
        color: #7A3030;
        padding: 26px;
        border-radius: 24px;
        border-left: 8px solid #D98C8C;
        box-shadow: 0px 12px 28px rgba(217, 140, 140, 0.18);
        margin-bottom: 18px;
    }

    .risk-label {
        font-size: 15px;
        font-weight: 800;
        opacity: 0.85;
        margin-bottom: 6px;
    }

    .risk-main {
        font-size: 31px;
        font-weight: 900;
        margin-bottom: 8px;
    }

    .risk-desc {
        font-size: 15px;
        line-height: 1.7;
    }

    /* Support card */
    .support-card {
        background: linear-gradient(135deg, #E8F4FF 0%, #F4F0FF 100%);
        color: #263B5E;
        padding: 28px;
        border-radius: 26px;
        border-left: 8px solid #8CAFE6;
        box-shadow: 0px 12px 30px rgba(90, 120, 170, 0.16);
        margin-top: 30px;
        margin-bottom: 22px;
    }

    .support-title {
        font-size: 24px;
        font-weight: 900;
        color: #24364B;
        margin-bottom: 10px;
    }

    .support-text {
        font-size: 16px;
        line-height: 1.75;
        color: #40546F;
    }

    .support-highlight {
        margin-top: 15px;
        background-color: rgba(255,255,255,0.82);
        padding: 15px 17px;
        border-radius: 17px;
        font-weight: 800;
        color: #314766;
        border: 1px solid rgba(140, 175, 230, 0.22);
    }

    /* Button */
    div.stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #6FAFA3 0%, #5E9F94 100%);
        color: white;
        font-size: 17px;
        font-weight: 850;
        border-radius: 16px;
        padding: 13px;
        border: none;
        box-shadow: 0px 8px 18px rgba(95, 160, 148, 0.32);
        transition: 0.25s ease;
    }

    div.stButton > button:hover {
        background: linear-gradient(135deg, #5E9F94 0%, #4D8B80 100%);
        color: white;
        border: none;
        transform: translateY(-1px);
    }

    /* Input fields */
    div[data-baseweb="select"] > div {
        border-radius: 15px;
        background-color: rgba(255, 255, 255, 0.86);
        border-color: #CFE0DD;
    }

    input {
        border-radius: 15px !important;
        background-color: rgba(255, 255, 255, 0.86) !important;
    }

    /* Metric */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.72);
        padding: 18px 20px;
        border-radius: 20px;
        border: 1px solid rgba(118, 183, 168, 0.18);
        box-shadow: 0px 10px 24px rgba(63, 111, 103, 0.10);
    }

    /* Hide Streamlit footer/menu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    h1, h2, h3 {
        color: #24364B;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    return joblib.load("depression_model.pkl")


model_package = load_model()

model = model_package["model"]
scaler = model_package["scaler"]
feature_columns = model_package["feature_columns"]

st.markdown("""
<div class="hero-card">
    <div class="hero-title">🌿 Student Mental Health Risk Screening</div>
    <div class="hero-subtitle">
        Aplikasi pendukung berbasis machine learning untuk membantu mengestimasi risiko kesehatan mental mahasiswa
        berdasarkan faktor akademik, gaya hidup, tekanan finansial, dan riwayat keluarga.
    </div>
    <span class="badge">Academic Factors</span>
    <span class="badge">Lifestyle Factors</span>
    <span class="badge">Financial Stress</span>
    <span class="badge">Machine Learning Screening</span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="note-card">
    <b>Catatan:</b> Aplikasi ini memberikan estimasi risiko berdasarkan model machine learning dan bukan pengganti diagnosis medis.
    Jika mengalami kondisi serius, disarankan untuk berkonsultasi dengan tenaga profesional.
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-title">Input Data Mahasiswa</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">Lengkapi data berikut untuk mendapatkan estimasi risiko berdasarkan model.</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2, gap="large")

with col1:
    gender_input = st.selectbox("Gender", ["Male", "Female"])

    age = st.number_input(
        "Age",
        min_value=15,
        max_value=60,
        value=20
    )

    academic_pressure = st.slider(
        "Academic Pressure",
        min_value=0,
        max_value=5,
        value=3
    )

    ipk_indonesia = st.number_input(
        "IPK Indonesia",
        min_value=0.0,
        max_value=4.0,
        value=3.0,
        step=0.01
    )

    study_satisfaction = st.slider(
        "Study Satisfaction",
        min_value=0,
        max_value=5,
        value=3
    )

with col2:
    sleep_duration_input = st.selectbox(
        "Sleep Duration",
        [
            "Less than 5 hours",
            "5-6 hours",
            "7-8 hours",
            "More than 8 hours",
            "Others"
        ]
    )

    dietary_habits_input = st.selectbox(
        "Dietary Habits",
        ["Healthy", "Moderate", "Unhealthy", "Others"]
    )

    suicidal_thoughts_input = st.selectbox(
        "Have you ever had suicidal thoughts?",
        ["No", "Yes"]
    )

    work_study_hours = st.slider(
        "Work/Study Hours per Day",
        min_value=0,
        max_value=15,
        value=6
    )

    financial_stress = st.slider(
        "Financial Stress",
        min_value=1,
        max_value=5,
        value=3
    )

    family_history_input = st.selectbox(
        "Family History of Mental Illness",
        ["No", "Yes"]
    )

button_col, empty_col = st.columns([1, 5])
with button_col:
    predict_button = st.button("Analyze Risk")


def preprocess_input():
    gender_map = {
        "Female": 0,
        "Male": 1
    }

    sleep_map = {
        "Less than 5 hours": 1,
        "5-6 hours": 2,
        "7-8 hours": 3,
        "More than 8 hours": 4,
        "Others": 0
    }

    dietary_map = {
        "Healthy": 0,
        "Moderate": 1,
        "Others": 2,
        "Unhealthy": 3
    }

    suicidal_map = {
        "No": 0,
        "Yes": 1
    }

    family_history_map = {
        "No": 0,
        "Yes": 1
    }

    cgpa = ipk_indonesia * 2.5

    input_data = pd.DataFrame([{
        "Gender": gender_map[gender_input],
        "Age": age,
        "Academic Pressure": academic_pressure,
        "CGPA": cgpa,
        "Study Satisfaction": study_satisfaction,
        "Sleep Duration": sleep_map[sleep_duration_input],
        "Dietary Habits": dietary_map[dietary_habits_input],
        "Have you ever had suicidal thoughts ?": suicidal_map[suicidal_thoughts_input],
        "Work/Study Hours": work_study_hours,
        "Financial Stress": financial_stress,
        "Family History of Mental Illness": family_history_map[family_history_input]
    }])

    input_data = input_data[feature_columns]
    input_scaled = scaler.transform(input_data)

    return input_data, input_scaled

if predict_button:
    raw_input, final_input = preprocess_input()

    prediction = model.predict(final_input)[0]
    probability = model.predict_proba(final_input)[0][1]
    probability_percent = probability * 100

    st.markdown('<div class="section-title">Prediction Result</div>', unsafe_allow_html=True)

    if probability_percent <= 30:
        risk_level = "Low Risk"
        risk_desc = (
            "Berdasarkan data yang dimasukkan, model mengklasifikasikan risiko depresi "
            "pada tingkat rendah."
        )
        card_class = "result-card-low"
    elif probability_percent <= 70:
        risk_level = "Moderate Risk"
        risk_desc = (
            "Berdasarkan data yang dimasukkan, model mengklasifikasikan risiko depresi "
            "pada tingkat sedang. Perhatikan faktor tekanan akademik, jam belajar, dan tekanan finansial."
        )
        card_class = "result-card-moderate"
    else:
        risk_level = "High Risk"
        risk_desc = (
            "Berdasarkan data yang dimasukkan, model mengklasifikasikan risiko depresi "
            "pada tingkat tinggi. Dukungan dari lingkungan sekitar dan konsultasi profesional sangat disarankan."
        )
        card_class = "result-card-high"

    st.markdown(f"""
    <div class="{card_class}">
        <div class="risk-label">Estimated Risk Level</div>
        <div class="risk-main">{risk_level}</div>
        <div class="risk-desc">{risk_desc}</div>
    </div>
    """, unsafe_allow_html=True)

    metric_col1, metric_col2 = st.columns([1, 2])

    with metric_col1:
        st.metric(
            label="Depression Risk Probability",
            value=f"{probability_percent:.2f}%"
        )

    with metric_col2:
        st.write("Risk Progress")
        st.progress(min(int(probability_percent), 100))

    with st.expander("View processed input data"):
        st.dataframe(raw_input, use_container_width=True)

st.markdown("""
<div class="support-card">
    <div class="support-title">💬 Butuh teman cerita?</div>
    <div class="support-text">
        Kamu tidak harus menghadapi semuanya sendirian. Jika membutuhkan dukungan,
        hubungi layanan bantuan resmi yang sudah diverifikasi.
    </div>
    <div class="support-highlight">
        SEJIWA di 119 ext. 8 (Gratis & Rahasia)
    </div>
</div>
""", unsafe_allow_html=True)
