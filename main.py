import streamlit as st
import pandas as pd
import tempfile
from pathlib import Path

from agent.pipeline import ResumeScreeningAgent
from agent.output import ResultsExporter


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="AI Resume Screening Agent",
    page_icon="🤖",
    layout="wide"
)


# ==================================================
# HEADER
# ==================================================

st.title("🤖 AI Resume Screening Agent")

st.markdown(
    """
    ### Intelligent Resume Screening & Ranking

    Analyze a job description, screen multiple candidates,
    calculate AI-powered matching scores, rank candidates,
    and identify their strengths and skill gaps.
    """
)

st.divider()


# ==================================================
# INPUT SECTION
# ==================================================

st.header("📥 Input")

col1, col2 = st.columns(2)


# --------------------------------------------------
# Job Description
# --------------------------------------------------

with col1:

    st.subheader("📄 Job Description")

    job_description = st.text_area(
        "Paste the complete job description",
        height=300,
        placeholder=(
            "Example:\n\n"
            "We are looking for a Junior AI Research "
            "Associate with knowledge of Python..."
        ),
        label_visibility="collapsed"
    )


# --------------------------------------------------
# Resume Upload
# --------------------------------------------------

with col2:

    st.subheader("📑 Candidate Resumes")

    uploaded_resumes = st.file_uploader(
        "Upload candidate resumes",
        type=[
            "pdf",
            "docx",
            "txt"
        ],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )

    if uploaded_resumes:

        st.success(
            f"{len(uploaded_resumes)} resume(s) uploaded."
        )

        for resume in uploaded_resumes:

            st.write(
                f"📄 {resume.name}"
            )


st.divider()


# ==================================================
# SCREEN BUTTON
# ==================================================

screen_button = st.button(
    "🚀 Screen Candidates",
    type="primary",
    use_container_width=True
)


# ==================================================
# SCREENING
# ==================================================

if screen_button:

    # ----------------------------------------------
    # Validate input
    # ----------------------------------------------

    if not job_description.strip():

        st.error(
            "⚠️ Please enter a job description."
        )

        st.stop()

    if not uploaded_resumes:

        st.error(
            "⚠️ Please upload at least one resume."
        )

        st.stop()

    # ----------------------------------------------
    # Run screening
    # ----------------------------------------------

    with st.spinner(
        "🤖 AI agent is analyzing candidates..."
    ):

        try:

            with tempfile.TemporaryDirectory() as temp_dir:

                resume_folder = Path(temp_dir)

                # Save uploaded resumes
                for uploaded_file in uploaded_resumes:

                    file_path = (
                        resume_folder
                        / uploaded_file.name
                    )

                    with open(
                        file_path,
                        "wb"
                    ) as file:

                        file.write(
                            uploaded_file.getbuffer()
                        )

                # Create agent
                agent = ResumeScreeningAgent()

                # Run screening
                results = agent.screen_candidates(
                    resume_folder=resume_folder,
                    job_description=job_description
                )

        except Exception as error:

            st.error(
                "❌ An error occurred while screening the resumes."
            )

            st.exception(error)

            st.stop()


    # ==================================================
    # JOB REQUIREMENTS
    # ==================================================

    st.divider()

    st.header("🧠 Job Requirements Identified by AI")

    requirements = results[
        "requirements"
    ]

    req_col1, req_col2, req_col3 = st.columns(3)


    # --------------------------------------------------
    # Required Skills
    # --------------------------------------------------

    with req_col1:

        st.subheader("Required Skills")

        skills = requirements[
            "required_skills"
        ]

        if skills:

            for skill in skills:

                st.write(
                    f"• {skill}"
                )

        else:

            st.write(
                "No technical skills detected."
            )


    # --------------------------------------------------
    # Experience
    # --------------------------------------------------

    with req_col2:

        st.subheader("Experience")

        experience = requirements[
            "minimum_experience_months"
        ]

        if experience > 0:

            if experience >= 12:

                years = experience / 12

                st.metric(
                    "Minimum Experience",
                    f"{years:.1f} years"
                )

            else:

                st.metric(
                    "Minimum Experience",
                    f"{experience:.0f} months"
                )

        else:

            st.metric(
                "Minimum Experience",
                "Not specified"
            )


    # --------------------------------------------------
    # Education
    # --------------------------------------------------

    with req_col3:

        st.subheader("Education")

        education = requirements[
            "education_keywords"
        ]

        if education:

            for item in education:

                st.write(
                    f"• {item}"
                )

        else:

            st.write(
                "No education requirements detected."
            )


    # ==================================================
    # SCREENING RESULTS
    # ==================================================

    st.divider()

    st.header("🏆 Candidate Ranking")

    candidates = results[
        "candidates"
    ]


    # ==================================================
    # SUMMARY METRICS
    # ==================================================

    if candidates:

        best_candidate = candidates[0]

        metric1, metric2, metric3, metric4 = (
            st.columns(4)
        )

        with metric1:

            st.metric(
                "Candidates Screened",
                len(candidates)
            )

        with metric2:

            st.metric(
                "Top Candidate",
                best_candidate["name"]
            )

        with metric3:

            st.metric(
                "Top Score",
                f"{best_candidate['overall_score']:.2f}/100"
            )

        with metric4:

            # Use the recommendation labels
            # actually generated by the project.
            strong_matches = sum(
                1
                for candidate in candidates
                if candidate["recommendation"]
                == "Good Match"
            )

            st.metric(
                "Good Matches",
                strong_matches
            )


    # ==================================================
    # RANKING TABLE
    # ==================================================

    st.subheader("📊 Ranking Overview")

    table_data = []

    for candidate in candidates:

        table_data.append(
            {
                "Rank":
                    candidate["rank"],

                "Candidate":
                    candidate["name"],

                "Overall Score":
                    candidate["overall_score"],

                "Semantic":
                    candidate["semantic_score"],

                "Skills":
                    candidate["skill_score"],

                "Experience":
                    candidate["experience_score"],

                "Education":
                    candidate["education_score"],

                "Recommendation":
                    candidate["recommendation"]
            }
        )


    ranking_df = pd.DataFrame(
        table_data
    )


    st.dataframe(
        ranking_df,
        use_container_width=True,
        hide_index=True
    )


    # ==================================================
    # SCORE CHART
    # ==================================================

    st.subheader("📈 Candidate Scores")

    chart_df = ranking_df[
        [
            "Candidate",
            "Overall Score"
        ]
    ].set_index(
        "Candidate"
    )

    st.bar_chart(
        chart_df
    )


    # ==================================================
    # DETAILED CANDIDATE RESULTS
    # ==================================================

    st.subheader(
        "🔍 Candidate Details"
    )


    for candidate in candidates:

        recommendation = (
            candidate["recommendation"]
        )


        # Recommendation icons
        if recommendation == "Good Match":

            icon = "🟢"

        elif recommendation == "Moderate Match":

            icon = "🟡"

        elif recommendation == "Low Match":

            icon = "🔴"

        else:

            icon = "🔵"


        with st.expander(
            f"{icon} Rank {candidate['rank']} — "
            f"{candidate['name']} — "
            f"{candidate['overall_score']:.2f}/100"
        ):

            detail_col1, detail_col2 = (
                st.columns(2)
            )


            # ------------------------------------------
            # Scores
            # ------------------------------------------

            with detail_col1:

                st.markdown(
                    "### 📊 Scores"
                )

                st.write(
                    f"**Overall:** "
                    f"{candidate['overall_score']:.2f}/100"
                )

                st.write(
                    f"**Semantic Match:** "
                    f"{candidate['semantic_score']:.2f}"
                )

                st.write(
                    f"**Skills:** "
                    f"{candidate['skill_score']:.2f}"
                )

                st.write(
                    f"**Experience:** "
                    f"{candidate['experience_score']:.2f}"
                )

                st.write(
                    f"**Education:** "
                    f"{candidate['education_score']:.2f}"
                )

                st.write(
                    f"**Recommendation:** "
                    f"{recommendation}"
                )


            # ------------------------------------------
            # Strengths
            # ------------------------------------------

            with detail_col2:

                st.markdown(
                    "### ✅ Strengths"
                )

                if candidate["strengths"]:

                    for skill in candidate[
                        "strengths"
                    ]:

                        st.write(
                            f"✅ {skill}"
                        )

                else:

                    st.write(
                        "No major strengths identified."
                    )


                st.markdown(
                    "### ⚠️ Skill Gaps"
                )

                if candidate["skill_gaps"]:

                    for skill in candidate[
                        "skill_gaps"
                    ]:

                        st.write(
                            f"⚠️ {skill}"
                        )

                else:

                    st.write(
                        "No major skill gaps identified."
                    )


    # ==================================================
    # EXPORT
    # ==================================================

    st.divider()

    st.header("📥 Export Results")

    try:

        exporter = ResultsExporter()

        output_path = exporter.export_csv(
            candidates
        )

        output_path = Path(output_path)

        if output_path.exists():

            with open(
                output_path,
                "rb"
            ) as file:

                st.download_button(
                    label="⬇️ Download Screening Results (CSV)",
                    data=file,
                    file_name="screening_results.csv",
                    mime="text/csv",
                    use_container_width=True
                )

        else:

            st.warning(
                "CSV export file was not created."
            )

    except Exception as error:

        st.error(
            "❌ Unable to generate CSV export."
        )

        st.exception(error)