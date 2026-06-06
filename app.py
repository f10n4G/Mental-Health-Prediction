import streamlit as st
import pandas as pd
import joblib


st.set_page_config(
    page_title="Student Depression Prediction",
    page_icon="🧠",
    layout="centered"
)


@st.cache_resource
def load_model():
    return joblib.load("depression_model.pkl")


model_package = load_model()

model = model_package["model"]
scaler = model_package["scaler"]
feature_columns = model_package["feature_columns"]


st.title("🧠 Student Depression Prediction App")

st.write(
    """
    Aplikasi ini digunakan untuk memprediksi risiko depresi pada mahasiswa
    berdasarkan faktor akademik, gaya hidup, tekanan finansial, dan riwayat keluarga.
    """
)

st.warning(
    """
    Disclaimer: Hasil prediksi ini hanya berbasis model machine learning dan bukan diagnosis medis.
    Jika mengalami kondisi serius, tetap perlu berkonsultasi dengan tenaga profesional.
    """
)


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