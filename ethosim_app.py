
import streamlit as st

def age_weight(age):
    if age <= 40:
        return 0.6
    elif 41 <= age <= 65:
        return 0.3
    else:
        return 0.1

def duration_weight(months):
    if months <= 6:
        return 0.1
    elif 7 <= months <= 18:
        return 0.3
    else:
        return 0.5

def ethical_decision_advanced_v2(
    patient_request,
    doctor_view,
    family_view,
    law,
    weight_autonomy,
    weight_sanctity,
    pain_level,
    mental_status,
    quality_of_life,
    age,
    disease_duration,
    weight_doctor=0.3,
    weight_family=0.3,
    weight_law=0.3,
    weight_pain=0.5,
    weight_mental=0.3,
    weight_qol=0.4,
):
    conflict = abs(weight_autonomy - weight_sanctity)
    w_age = age_weight(age)
    w_duration = duration_weight(disease_duration)

    decision_score = (
        weight_autonomy * patient_request +
        weight_doctor * doctor_view +
        weight_family * family_view +
        weight_law * law -
        conflict +
        weight_pain * pain_level -
        weight_mental * abs(mental_status) -
        weight_qol * (10 - quality_of_life) +
        w_age +
        w_duration
    )

    if decision_score > 5:
        return "توصیه: توقف درمان / پایان زندگی"
    elif decision_score < -5:
        return "توصیه: ادامه درمان"
    else:
        return "منطقه خاکستری: نیاز به بررسی بیشتر"

# --- Streamlit UI ---
st.title("شبیه‌ساز تصمیم‌گیری اخلاقی پزشکی (Ethosim)")

st.header("ورود داده‌های بیمار و تیم درمان")

patient_request = st.slider("درخواست بیمار برای توقف درمان (0 تا 10)", 0, 10, 5)
doctor_view = st.slider("دیدگاه پزشک (-10 مخالف تا 10 موافق)", -10, 10, 0)
family_view = st.slider("دیدگاه خانواده (-10 مخالف تا 10 موافق)", -10, 10, 0)
law = st.selectbox("آیا قانون کشور اجازه توقف درمان را می‌دهد؟", options=[0, 1], format_func=lambda x: "خیر" if x == 0 else "بله")
weight_autonomy = st.slider("وزن اهمیت آزادی فردی (0 تا 1)", 0.0, 1.0, 0.7)
weight_sanctity = st.slider("وزن اهمیت تقدس جان (0 تا 1)", 0.0, 1.0, 0.8)
pain_level = st.slider("شدت درد بیمار (0 تا 10)", 0, 10, 5)
mental_status = st.slider("وضعیت روانی بیمار (-10 ناپایدار تا 10 پایدار)", -10, 10, 0)
quality_of_life = st.slider("کیفیت زندگی بیمار (0 ضعیف تا 10 عالی)", 0, 10, 5)
age = st.number_input("سن بیمار (سال)", min_value=0, max_value=120, value=50)
disease_duration = st.number_input("مدت بیماری (ماه)", min_value=0, max_value=120, value=12)

if st.button("محاسبه تصمیم"):
    result = ethical_decision_advanced_v2(
        patient_request,
        doctor_view,
        family_view,
        law,
        weight_autonomy,
        weight_sanctity,
        pain_level,
        mental_status,
        quality_of_life,
        age,
        disease_duration,
    )
    st.subheader("نتیجه تصمیم‌گیری:")
    st.write(result)
