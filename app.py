import streamlit as st
from langchain.schema import Document

from log_parser import parse_ptp_log
from qa_agent import ask_question, initialize_qa
from summarizer import generate_daily_summary
from charts import plot_offset_chart, plot_state_changes

st.set_page_config(page_title="ClockSense", layout="wide")
st.title("🕰️ ClockSense - PTP Log Analyzer")

# Initialize QA chain and vector store
if "qa_chain" not in st.session_state:
    qa_chain, vectordb = initialize_qa()
    st.session_state.qa_chain = qa_chain
    st.session_state.vectordb = vectordb

# File upload
log_file = st.file_uploader("Upload PTP log file", type=["log", "txt"])
if log_file:
    text = log_file.read().decode()
    parsed_data, chunks = parse_ptp_log(text)

    # Index uploaded log chunks into vector store
    docs = [Document(page_content=chunk) for chunk in chunks]
    st.session_state.vectordb.add_documents(docs)

    # Query section
    query = st.text_input("Ask about your logs:")
    if query:
        ans = ask_question(query, st.session_state.qa_chain)
        st.markdown(f"**Answer:** {ans}")

    st.markdown("---")
    # Summary
    if st.button("Generate Daily Summary"):
        summary = generate_daily_summary(chunks)
        st.text_area("Summary", summary, height=250)

    st.markdown("---")
    # Visualizations
    col1, col2 = st.columns(2)
    with col1:
        st.caption("Offset Over Time")
        fig1 = plot_offset_chart(parsed_data)
        st.pyplot(fig1)
    with col2:
        st.caption("State Changes")
        fig2 = plot_state_changes(parsed_data)
        st.pyplot(fig2)
else:
    st.info("Upload a log file to begin.")
