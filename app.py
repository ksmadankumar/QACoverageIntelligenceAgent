import streamlit as st
import pandas as pd
from pathlib import Path

from modules.requirement_parser import extract_requirements
from modules.csv_loader import load_test_cases
from modules.rag_engine import index_requirements
from modules.analyzer import analyze_all_test_cases
from modules.dashboard import render_dashboard
from modules.traceability_engine import build_traceability_matrix
from modules.report_generator import export_excel

st.set_page_config(
    page_title="QA Coverage Intelligence Agent",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 QA Coverage Intelligence Agent")

st.markdown("""
### Upload Files

**Requirements Document**
- PDF
- DOCX
- TXT

**Test Cases**
- CSV
- XLSX
""")

req_file = st.file_uploader(
    "📄 Upload Requirements",
    type=["pdf", "docx", "txt"]
)

tc_file = st.file_uploader(
    "🧪 Upload Test Cases",
    type=["csv", "xlsx"]
)

if req_file and tc_file:

    req_folder = Path("uploads/requirements")
    tc_folder = Path("uploads/testcases")

    req_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    tc_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    req_path = req_folder / req_file.name
    tc_path = tc_folder / tc_file.name

    with open(req_path, "wb") as f:
        f.write(req_file.getbuffer())

    with open(tc_path, "wb") as f:
        f.write(tc_file.getbuffer())

    st.success("Files uploaded successfully")

    if st.button("🚀 Start Analysis"):

        requirements_text = extract_requirements(
            req_path
        )

        with st.spinner(
            "Building requirement knowledge base..."
        ):
            index_requirements(
                requirements_text
            )

        df = load_test_cases(
            tc_path
        )

        progress_bar = st.progress(0)

        status_text = st.empty()

        def update_progress(
            processed,
            total,
            eta
        ):
            progress_bar.progress(
                processed / total
            )

            status_text.write(
                f"Processed {processed}/{total} | ETA {eta}s"
            )

        results = analyze_all_test_cases(
            df,
            update_progress
        )

        results_df = pd.DataFrame(
            results
        )

        traceability_df = (
            build_traceability_matrix(
                requirements_text,
                results_df
            )
        )

        st.session_state[
            "results_df"
        ] = results_df

        st.session_state[
            "traceability_df"
        ] = traceability_df

        st.success(
            "Analysis completed successfully"
        )

if (
    "results_df" in st.session_state
    and
    "traceability_df" in st.session_state
):

    results_df = (
        st.session_state[
            "results_df"
        ]
    )

    traceability_df = (
        st.session_state[
            "traceability_df"
        ]
    )

    render_dashboard(
        results_df,
        traceability_df
    )

    st.subheader(
        "📋 Analysis Results"
    )

    st.dataframe(
        results_df,
        use_container_width=True
    )

    st.subheader(
        "🔗 Requirement Traceability Matrix"
    )

    st.dataframe(
        traceability_df,
        use_container_width=True
    )

    excel_file = export_excel(
        results_df,
        traceability_df
    )

    with open(
        excel_file,
        "rb"
    ) as f:

        st.download_button(
            label="📥 Download Excel Report",
            data=f,
            file_name="QA_Analysis_Report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )