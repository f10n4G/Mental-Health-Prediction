import streamlit as st
import pandas as pd
import joblib


st.set_page_config(
    page_title="Student Depression Prediction",
    page_icon="🧠",
    layout="centered"
)

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #F7FBFC 0%, #EEF7F6 50%, #F9F7FF 100%);
        color: #243B53;
    }

    .main-container {
        background-color: rgba(255, 255, 255, 0.85);
        padding: 28px;
        border-radius: 24px;
        box-shadow: 0px 8px 30px rgba(80, 120, 140, 0.12);
        margin-bottom: 25px;
    }

    .hero-title {
        font-size: 44px;
        font-weight: 800;
        color: #203647;
        line-height: 1.15;
        margin-bottom: 10px;
    }

    .hero-subtitle {
        font-size: 18px;
        color: #5C6F82;
        line-height: 1.7;
        margin-bottom: 20px;
    }

    .soft-card {
        background: #FFFFFF;
        padding: 22px 24px;
        border-radius: 20px;
        border: 1px solid #E3EEF2;
        box-shadow: 0px 6px 20px rgba(80, 120, 140, 0.08);
        margin-bottom: 22px;
    }

    .info-card {
        background: #EAF7F4;
        color: #244D4A;
        padding: 18px 22px;
        border-radius: 18px;
        border-left: 6px solid #6AB7A8;
        font-size: 16px;
        line-height: 1.6;
        margin-bottom: 24px;
    }

    .support-card {
        background: linear-gradient(135deg, #EEF8FF 0%, #F4F0FF 100%);
        color: #263B5E;
        padding: 22px 24px;
        border-radius: 20px;
        border-left: 6px solid #7BA7D7;
        font-size: 17px;
        line-height: 1.6;
        margin-top: 25px;
        margin-bottom: 20px;
    }

    .support-title {
        font-size: 22px;
        font-weight: 800;
        margin-bottom: 8px;
        color: #203647;
    }

    div.stButton > button {
        width: 100%;
        background-color: #6AB7A8;
        color: white;
        font-size: 18px;
        font-weight: 700;
        border-radius: 14px;
        padding: 12px;
        border: none;
        transition: 0.3s;
    }

    div.stButton > button:hover {
        background-color: #4D9C90;
        color: white;
        border: none;
    }

    .stSlider [data-baseweb="slider"] > div {
        color: #6AB7A8;
    }

    h1, h2, h3 {
        color: #203647;
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
<div class="main-container">
    <div class="hero-title">🌿 Student Mental Health Risk Screening</div>
    <div class="hero-subtitle">
        Aplikasi pendukung berbasis machine learning untuk membantu mengestimasi risiko kesehatan mental mahasiswa.       
    </div>
</div>
""", unsafe_allow_html=True)

st.write(
    """
    Aplikasi ini digunakan untuk memprediksi risiko depresi pada mahasiswa
    berdasarkan faktor akademik, gaya hidup, tekanan finansial, dan riwayat keluarga.
    """
)

st.markdown("""
<div class="info-card">
    <b>Catatan:</b> Aplikasi ini memberikan estimasi risiko berdasarkan model machine learning dan bukan pengganti diagnosis medis.
    Jika mengalami kondisi serius, disarankan untuk berkonsultasi dengan tenaga profesional.
</div>
""", unsafe_allow_html=True)


st.subheader("Input Data Mahasiswa")


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

cgpa = ipk_indonesia * 2.5

study_satisfaction = st.slider(
    "Study Satisfaction",
    min_value=0,
    max_value=5,
    value=3
)

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


if st.button("Predict"):
    raw_input, final_input = preprocess_input()

    prediction = model.predict(final_input)[0]
    probability = model.predict_proba(final_input)[0][1]

    st.subheader("Input Data Setelah Diproses")
    st.dataframe(raw_input)

    st.subheader("Prediction Result")

    if prediction == 1:
        st.error("Hasil Prediksi: Mahasiswa berisiko mengalami depresi.")
    else:
        st.success("Hasil Prediksi: Mahasiswa tidak terprediksi berisiko mengalami depresi.")

    st.metric(
        label="Depression Risk Probability",
        value=f"{probability * 100:.2f}%"
    )

st.markdown("""
<div class="support-card">
    <div class="support-title">💬 Butuh teman cerita?</div>
    Kamu tidak harus menghadapi semuanya sendirian. Jika membutuhkan dukungan, hubungi layanan bantuan resmi yang tersedia.
    <br><br>
    <b>Placeholder teks:</b> Butuh teman cerita? Hubungi SEJIWA di 119 ext. 8 (Gratis & Rahasia)
</div>
""", unsafe_allow_html=True)
