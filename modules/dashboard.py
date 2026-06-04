import streamlit as st
import plotly.express as px


def render_dashboard(
    results_df,
    traceability_df
):

    st.header(
        "📊 QA Intelligence Dashboard"
    )

    total_cases = len(
        results_df
    )

    avg_score = round(
        results_df[
            "final_score"
        ].mean(),
        2
    )

    coverage = round(

        (
            len(
                traceability_df[
                    traceability_df[
                        "Coverage Status"
                    ]
                    ==
                    "Covered"
                ]
            )
            /
            len(traceability_df)
        )
        * 100,

        2

    )

    c1, c2, c3 = (
        st.columns(3)
    )

    c1.metric(
        "Test Cases",
        total_cases
    )

    c2.metric(
        "Average Score",
        avg_score
    )

    c3.metric(
        "Requirement Coverage %",
        coverage
    )

    st.divider()

    st.subheader(
        "Requirement Coverage"
    )

    coverage_fig = (
        px.histogram(
            traceability_df,
            x="Coverage Status"
        )
    )

    st.plotly_chart(
        coverage_fig,
        use_container_width=True
    )

    st.subheader(
        "Severity Distribution"
    )

    sev_fig = (
        px.histogram(
            results_df,
            x="severity"
        )
    )

    st.plotly_chart(
        sev_fig,
        use_container_width=True
    )

    st.subheader(
        "Risk Distribution"
    )

    risk_fig = (
        px.histogram(
            results_df,
            x="risk_level"
        )
    )

    st.plotly_chart(
        risk_fig,
        use_container_width=True
    )