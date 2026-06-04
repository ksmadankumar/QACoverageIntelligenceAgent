import streamlit as st

st.title("QA Agent Debug")

st.success("App Started")

try:
    from modules.requirement_parser import extract_requirements
    st.success("requirement_parser loaded")
except Exception as e:
    st.error(f"requirement_parser failed: {e}")

try:
    from modules.csv_loader import load_test_cases
    st.success("csv_loader loaded")
except Exception as e:
    st.error(f"csv_loader failed: {e}")

try:
    from modules.rag_engine import index_requirements
    st.success("rag_engine loaded")
except Exception as e:
    st.error(f"rag_engine failed: {e}")

try:
    from modules.analyzer import analyze_all_test_cases
    st.success("analyzer loaded")
except Exception as e:
    st.error(f"analyzer failed: {e}")

try:
    from modules.dashboard import render_dashboard
    st.success("dashboard loaded")
except Exception as e:
    st.error(f"dashboard failed: {e}")

try:
    from modules.traceability_engine import build_traceability_matrix
    st.success("traceability_engine loaded")
except Exception as e:
    st.error(f"traceability_engine failed: {e}")

try:
    from modules.report_generator import export_excel
    st.success("report_generator loaded")
except Exception as e:
    st.error(f"report_generator failed: {e}")