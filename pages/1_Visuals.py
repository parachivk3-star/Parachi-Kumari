# This creates the page for displaying data visualizations.

import streamlit as st

import json
import matplotlib.pyplot as plt

import pandas as pd
import os
from matplotlib.ticker import MaxNLocator

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

st.title("Healthcare Insights 🏥")

st.write("Explore patient trends across different healthcare departments.")


patientTab, surveyTab = st.tabs([
    "🏥 Patient Trends",
    "📊 Survey Results"
])

with patientTab:
    # PART 1: GRAPHS FROM data.json

    with open("data.json", "r") as file:
        data = json.load(file)

    departments = data["data_points"]

    st.header(data["chart_title"])

    st.subheader("Patient Distribution by Department")

    departmentNames = []
    patientTotals = []

    for department, months in departments.items():
        departmentNames.append(department)
        patientTotals.append(sum(months.values()))

    colors = ["#F4A7B9", "#B8A9E8", "#A8D5BA", "#9CCBE8"]

    fig, ax = plt.subplots()

    ax.pie(
        patientTotals,
        labels=departmentNames,
        autopct="%1.1f%%",
        colors=colors
    )

    ax.set_title("Patient Distribution by Department")

    st.pyplot(fig)
    plt.close(fig)

    st.subheader("Monthly Patient Visits")

    if "department" not in st.session_state:
        st.session_state.department = "General Medicine"

    if "minimum" not in st.session_state:
        st.session_state.minimum = 0

    selectedDepartment = st.radio(
        "Choose a department",
        list(departments.keys()),
        key="department"
    )

    minimumPatients = st.slider(
        "Minimum number of patients",
        min_value=0,
        max_value=110,
        step=5,
        key="minimum"
    )

    monthlyData = departments[selectedDepartment]

    filteredData = {}

    for month, patients in monthlyData.items():
        if patients >= minimumPatients:
            filteredData[month] = patients

    if len(filteredData) > 0:
        st.bar_chart(
            filteredData,
            color="#B8A9E8",
            x_label="Month",
            y_label="Number of Patients"
        )
    else:
        st.warning("No months match your selection.")

    if len(filteredData) > 0:
        patientCounts = list(filteredData.values())

   
        meanPatients = sum(patientCounts) / len(patientCounts)

        
        sortedCounts = sorted(patientCounts)
        n = len(sortedCounts)

        if n % 2 == 1:
            medianPatients = sortedCounts[n // 2]
        else:
            medianPatients = (
                sortedCounts[n // 2 - 1] + sortedCounts[n // 2]
            ) / 2

       
        previousMean = st.session_state.get("previousMean", meanPatients)
        previousMedian = st.session_state.get("previousMedian", medianPatients)

        
        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Mean Patients",
                round(meanPatients, 1),
                delta=round(meanPatients - previousMean, 1)
            )

        with col2:
            st.metric(
                "Median Patients",
                round(medianPatients, 1),
                delta=round(medianPatients - previousMedian, 1)
            )

    
        st.session_state.previousMean = meanPatients
        st.session_state.previousMedian = medianPatients

    else:
        st.info("No patient data available to calculate statistics.")
    
with surveyTab:
# PART 2: GRAPHS FROM data.csv
    st.divider()
    st.header("Healthcare Survey Results")

    if not os.path.exists("data.csv") or os.path.getsize("data.csv") == 0:
        st.info("Go to the Survey page and submit responses first.")

    else:
        surveyData = pd.read_csv("data.csv")

        if surveyData.empty:
            st.info("Go to the Survey page and submit responses first.")

        else:
            # STATIC VISUALIZATION: BAR CHART
            # Uses all responses and does not depend on the filters below.

            st.subheader("Survey Responses by Department")

            departmentCounts = (
                surveyData["Category"]
                .value_counts()
                .sort_index()
            )

            fig, ax = plt.subplots(figsize=(8, 5))

            ax.bar(
                departmentCounts.index,
                departmentCounts.values,
                color="#B8A9E8"
            )

            ax.set_title("Survey Responses by Department")
            ax.set_xlabel("Department")
            ax.set_ylabel("Number of Responses")

            ax.yaxis.set_major_locator(MaxNLocator(integer=True))
            ax.tick_params(axis="x", rotation=20)

            fig.tight_layout()

            st.pyplot(fig)
            plt.close(fig)

            # DYNAMIC VISUALIZATION: HISTOGRAM

            st.subheader("Distribution of Annual Visits")

            departmentOptions = ["All departments"] + sorted(
                surveyData["Category"].unique().tolist()
            )

            # Session state keeps track of the selected controls.
            if "surveyDepartment" not in st.session_state:
                st.session_state.surveyDepartment = "All departments"

            if st.session_state.surveyDepartment not in departmentOptions:
                st.session_state.surveyDepartment = "All departments"

            if "surveyBins" not in st.session_state:
                st.session_state.surveyBins = 5

            selectedDepartment = st.radio(
                "Choose a department to view",
                departmentOptions,
                key="surveyDepartment"
            )

            numberOfBins = st.slider(
                "Number of histogram bins",
                min_value=2,
                max_value=15,
                key="surveyBins"
            )

            if selectedDepartment == "All departments":
                filteredSurvey = surveyData
            else:
                filteredSurvey = surveyData[
                    surveyData["Category"] == selectedDepartment
                ]

            visitCounts = filteredSurvey["Value"].tolist()

            fig, ax = plt.subplots(figsize=(8, 5))

            ax.hist(
                visitCounts,
                bins=numberOfBins,
                color="#9CCBE8",
                edgecolor="white"
            )

            ax.set_title("Annual Visits: " + selectedDepartment)
            ax.set_xlabel("Visits in the Past Year")
            ax.set_ylabel("Number of Responses")

            ax.yaxis.set_major_locator(MaxNLocator(integer=True))

            fig.tight_layout()

            st.pyplot(fig)
            plt.close(fig)

            st.write("Number of responses shown:", len(visitCounts))

            if visitCounts:
                # EXTRA CREDIT: MEAN AND MEDIAN WITH DELTAS

                meanVisits = sum(visitCounts) / len(visitCounts)

                sortedVisits = sorted(visitCounts)
                n = len(sortedVisits)

                if n % 2 == 1:
                    medianVisits = sortedVisits[n // 2]
                else:
                    medianVisits = (
                        sortedVisits[n // 2 - 1]
                        + sortedVisits[n // 2]
                    ) / 2

                previousMean = st.session_state.get(
                    "surveyPreviousMean",
                    meanVisits
                )

                previousMedian = st.session_state.get(
                    "surveyPreviousMedian",
                    medianVisits
                )

                col1, col2 = st.columns(2)

                with col1:
                    st.metric(
                        "Mean Annual Visits",
                        round(meanVisits, 2),
                        delta=round(meanVisits - previousMean, 2),
                        delta_color="off"
                    )

                with col2:
                    st.metric(
                        "Median Annual Visits",
                        round(medianVisits, 2),
                        delta=round(medianVisits - previousMedian, 2),
                        delta_color="off"
                    )

                st.session_state.surveyPreviousMean = meanVisits
                st.session_state.surveyPreviousMedian = medianVisits

                st.caption(
                    "The metrics compare the current selection with the "
                    "previous selection. Changing the number of bins changes "
                    "the histogram grouping, but not the mean or median."
                )
            else:
                st.info("No survey data available to calculate statistics.")
