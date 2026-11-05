import streamlit as st
import pandas as pd
import csv
import os

st.set_page_config(page_title="Survey", page_icon="📝")

st.title("Healthcare Survey 🏥")
st.write(
    "Enter the department you visit most and how many times "
    "you visited that department in the past year."
)

departments = [
    "General Medicine",
    "Pediatrics",
    "Dermatology",
    "Cardiology",
    "Other"
]

with st.form("healthcareSurvey"):
    departmentInput = st.text_input(
        "Which department do you visit most?",
        help="General Medicine, Pediatrics, Dermatology, Cardiology, or Other"
    )

    visitsInput = st.text_input(
        "How many times did you visit that department in the past year?"
    )

    submitted = st.form_submit_button("Submit")

if submitted:
    departmentName = ""

    for department in departments:
        if departmentInput.strip().lower() == department.lower():
            departmentName = department

    try:
        visits = int(visitsInput.strip())
    except ValueError:
        visits = -1

    if departmentName == "":
        st.error("Please enter one of the departments listed above.")

    elif visits < 0:
        st.error("Please enter a whole number that is zero or greater.")

    else:
        needsHeader = (
            not os.path.exists("data.csv")
            or os.path.getsize("data.csv") == 0
        )

        with open("data.csv", "a", newline="") as file:
            writer = csv.writer(file)

            if needsHeader:
                writer.writerow(["Category", "Value"])

            writer.writerow([departmentName, visits])

        st.success("Your response has been saved!")

        st.write("Department:", departmentName)
        st.write("Annual visits:", visits)

st.divider()
st.subheader("Collected Responses")

if os.path.exists("data.csv") and os.path.getsize("data.csv") > 0:
    surveyData = pd.read_csv("data.csv")

    if surveyData.empty:
        st.info("Submit a response to start collecting data.")
    else:
        st.dataframe(
            surveyData.rename(
                columns={
                    "Category": "Department",
                    "Value": "Annual Visits"
                }
            ),
            hide_index=True
        )
else:
    st.info("No responses have been collected yet.")
