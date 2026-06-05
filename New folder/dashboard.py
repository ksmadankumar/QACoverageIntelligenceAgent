import streamlit as st
import pandas as pd
import plotly.express as px


def render_dashboard(results_df, traceability_df):

    st.sidebar.title(
        "QA Coverage Intelligence Agent"
    )

    page = st.sidebar.radio(
        "Navigation",
        [
            "Executive Summary",
            "Coverage Analysis",
            "Traceability Matrix",
            "Gap Analysis",
            "Raw Results"
        ]
    )

    if page == "Executive Summary":
        render_executive_summary(
            results_df,
            traceability_df
        )

    elif page == "Coverage Analysis":
        render_coverage_analysis(
            results_df
        )

    elif page == "Traceability Matrix":
        render_traceability(
            traceability_df
        )

    elif page == "Gap Analysis":
        render_gap_analysis(
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

    avg_score = round(
        results_df["quality_score"].mean(),
        2
    )

    covered = len(
        traceability_df[
            traceability_df["coverage_status"] == "Covered"
        ]
    )

    total_requirements = len(
        traceability_df
    )

    coverage_pct = round(
        (covered / max(total_requirements, 1)) * 100,
        2
    )

    high_risk = len(
        results_df[
            results_df["priority"]
            .astype(str)
            .str.lower()
            .isin(
                ["high", "critical"]
            )
        ]
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Tests",
        total_tests
    )

    col2.metric(
        "Avg Quality",
        avg_score
    )

    col3.metric(
        "Coverage %",
        coverage_pct
    )

    col4.metric(
        "High Risk",
        high_risk
    )

    st.divider()

    st.subheader(
        "Quality Score Distribution"
    )

    fig = px.histogram(
        results_df,
        x="quality_score"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


def render_coverage_analysis(
    results_df
):

    st.header(
        "Coverage Analysis"
    )

    categories = [
        "functional_score",
        "ui_score",
        "ux_score"
    ]

    available = [
        c
        for c in categories
        if c in results_df.columns
    ]

    if available:

        chart_df = pd.DataFrame(
            {
                "Category": available,
                "Score": [
                    results_df[c].mean()
                    for c in available
                ]
            }
        )

        fig = px.bar(
            chart_df,
            x="Category",
            y="Score"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.dataframe(
        results_df,
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


def render_gap_analysis(
    traceability_df
):

    st.header(
        "Gap Analysis"
    )

    gaps = traceability_df[
        traceability_df["coverage_status"]
        !=
        "Covered"
    ]

    st.metric(
        "Missing Requirements",
        len(gaps)
    )

    st.dataframe(
        gaps,
        use_container_width=True
    )


def render_raw_results(
    results_df
):

    st.header(
        "Raw Analysis Results"
    )

    st.dataframe(
        results_df,
        use_container_width=True
    )