import streamlit as st
import joblib
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Student Performance Predictor",
    page_icon="🎓",
    layout="wide"
)

# ---------------- LOAD MODEL ----------------
model = joblib.load("student_performance.pkl")

# ---------------- HEADER ----------------
st.title("🎓 Student Performance Prediction System")
st.markdown("Predict final marks using Machine Learning based on student data.")

st.divider()

# ---------------- INPUT SECTION ----------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📥 Input Features")

    study_hours = st.number_input("Study Hours", 0.0, 15.0, 5.0)
    attendance = st.number_input("Attendance (%)", 0.0, 100.0, 75.0)
    assignments = st.number_input("Assignments Completed", 0.0, 20.0, 10.0)
    previous_marks = st.number_input("Previous Marks", 0.0, 100.0, 60.0)

    predict = st.button("🚀 Predict Final Marks", use_container_width=True)

# ---------------- OUTPUT SECTION ----------------
with col2:
    st.subheader("📊 Prediction Result")

    if predict:
        prediction = model.predict([[study_hours, attendance, assignments, previous_marks]])
        result = float(prediction[0])

        st.metric("Predicted Final Marks", f"{result:.2f}")

        # Progress bar (0–100 clamp)
        st.progress(min(int(result), 100))

        # Performance category
        if result >= 85:
            st.success("🌟 Excellent Performance")
            st.balloons()
        elif result >= 70:
            st.info("👍 Good Performance")
        elif result >= 50:
            st.warning("📚 Average Performance")
        else:
            st.error("⚠️ Needs Improvement")

st.divider()

# ---------------- SUMMARY ----------------
st.subheader("📌 Input Summary")

df = pd.DataFrame({
    "Feature": [
        "Study Hours",
        "Attendance",
        "Assignments Completed",
        "Previous Marks"
    ],
    "Value": [
        study_hours,
        attendance,
        assignments,
        previous_marks
    ]
})

st.table(df)

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown(
    "Built with ❤️ using Streamlit and Scikit-Learn"
)