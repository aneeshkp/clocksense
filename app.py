import streamlit as st
from langchain.schema import Document

from log_parser import parse_ptp_log
from qa_agent import ask_question, initialize_qa
from summarizer import generate_daily_summary
from charts import plot_offset_chart, plot_state_changes

st.set_page_config(page_title="ClockSense", layout="wide")
st.title("🕰️ ClockSense - PTP Log Analyzer")

# Model selection UI
embed_options = ["all-MiniLM-L6-v2", "all-MiniLM-L12-v2", "sentence-transformers/msmarco-distilbert-base-tas-b"]
ellm_options = ["llama3", "gpt-3.5-turbo"]
selected_embed = st.sidebar.selectbox("Select embedding model", embed_options, index=0)
selected_llm = st.sidebar.selectbox("Select LLM model", ellm_options, index=0)

# Initialize or reload QA chain and vector store
if ("qa_chain" not in st.session_state) or (st.session_state.get("model_config") != (selected_embed, selected_llm)):
    with st.spinner("🔄 Loading selected AI models..."):
        qa_chain, vectordb = initialize_qa(embed_model=selected_embed, llm_model=selected_llm)
        st.session_state.qa_chain = qa_chain
        st.session_state.vectordb = vectordb
        st.session_state.model_config = (selected_embed, selected_llm)
    st.success("✅ AI models loaded!")

# File upload
log_file = st.file_uploader("Upload PTP log file", type=["log", "txt"])
if log_file:
    with st.spinner("🔄 Parsing log file..."):
        text = log_file.read().decode()
        parsed_data, chunks = parse_ptp_log(text)
    st.success("✅ Log parsed!")

    # Index uploaded log chunks with progress bar
    docs = [Document(page_content=chunk) for chunk in chunks]
    progress_bar = st.progress(0)
    for i, doc in enumerate(docs):
        st.session_state.vectordb.add_documents([doc])
        progress_bar.progress((i + 1) / len(docs))
    progress_bar.empty()
    st.success("✅ Log indexed!")

    # Query section
    query = st.text_input("Ask about your logs:")
    if query:
        with st.spinner("🔄 Generating answer..."):
            ans = ask_question(query, st.session_state.qa_chain)
        st.markdown(f"**Answer:** {ans}")

    st.markdown("---")
    # Daily Summary
    if st.button("Generate Daily Summary"):
        with st.spinner("🔄 Generating summary..."):
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
