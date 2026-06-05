import streamlit as st
import pandas as pd
import plotly.express as px


def render_dashboard(
    results_df,
    traceability_df
):

    st.sidebar.title(
        "QA Coverage Intelligence Agent"
    )

    page = st.sidebar.radio(
        "Navigation",
        [
            "Executive Summary",
            "Traceability Matrix",
            "Raw Results"
        ]
    )

    if page == "Executive Summary":

        render_executive_summary(
            results_df,
            traceability_df
        )

    elif page == "Traceability Matrix":

        render_traceability(
            traceability_df
        )

    elif page == "Raw Results":

        render_raw_results(
            results_df
        )


def render_executive_summary(
    results_df,
    traceability_df
):

    st.header(
        "Executive Summary"
    )

    total_tests = len(
        results_df
    )

    avg_score = 0

    if "quality_score" in results_df.columns:

        avg_score = round(
            pd.to_numeric(
                results_df["quality_score"],
                errors="coerce"
            ).fillna(0).mean(),
            2
        )

    covered = 0

    if (
        "coverage_status"
        in traceability_df.columns
    ):

        covered = len(
            traceability_df[
                traceability_df[
                    "coverage_status"
                ]
                ==
                "Covered"
            ]
        )

    total_requirements = len(
        traceability_df
    )

    coverage_pct = round(
        (
            covered
            /
            max(
                total_requirements,
                1
            )
        )
        * 100,
        2
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Tests",
        total_tests
    )

    col2.metric(
        "Average Quality",
        avg_score
    )

    col3.metric(
        "Coverage %",
        coverage_pct
    )

    st.divider()

    if (
        "quality_score"
        in results_df.columns
    ):

        fig = px.histogram(
            results_df,
            x="quality_score",
            title="Quality Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


def render_traceability(
    traceability_df
):

    st.header(
        "Requirement Traceability Matrix"
    )

    st.dataframe(
        traceability_df,
        use_container_width=True
    )


def render_raw_results(
    results_df
):

    st.header(
        "Analysis Results"
    )

    st.dataframe(
        results_df,
        use_container_width=True
    )