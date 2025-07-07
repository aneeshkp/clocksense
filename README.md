
# ClockSense

**ClockSense** is a local Streamlit application that lets you upload PTP log files, query them with a Llama-based RAG engine, generate daily summaries, and visualize key metrics (offset spikes and state changes).

## Features
- **Upload** PTP log files via browser UI
- **Query** logs naturally (e.g., "Why did we enter HOLDOVER at 10:30?")
- **Summarize** daily log activity
- **Visualize** offset vs. time and clock state transitions

## Tech Stack
- **Frontend:** Streamlit
- **RAG:** LangChain + Ollama (LLaMA3)
- **Embeddings:** all-MiniLM-L6-v2
- **Vector Store:** Chroma
- **Charts:** Matplotlib

## Installation
1. Clone this repo:
   ```bash
   git clone https://github.com/your-org/clocksense.git
   cd clocksense

    Install dependencies:
    pip install -r requirements.txt

    Ensure Ollama is installed and Llama3 model is available:
    ollama pull llama3

    Run the app:
    streamlit run app.py

Usage

    Upload a .log or .txt file in the sidebar.

    Ask questions in the text box (e.g., "What caused the offset spike at 09:45?").

    Click Generate Summary for a quick daily overview.

    View charts for offset and state changes.

File Descriptions

    app.py: Main Streamlit application

    log_parser.py: Extracts timestamp, offset, and state from logs

    qa_agent.py: Initializes and runs the RAG QA chain

    summarizer.py: Builds simple daily summaries from log chunks

    charts.py: Generates Matplotlib figures for offsets and states

    requirements.txt: Python dependencies


## 📋 Alternative Libraries

| Component       | Current             | Alternatives                        | Why Chosen                                      |
|-----------------|---------------------|-------------------------------------|-------------------------------------------------|
| Frontend UI     | Streamlit           | Dash, Gradio, Panel                 | Rapid prototyping with minimal code             |
| RAG Framework   | LangChain           | LlamaIndex, Haystack, Vertex AI     | Modular chains, broad community support         |
| Embeddings      | all-MiniLM-L6-v2    | OpenAI Ada, Sentence-BERT           | Compact models offering fast local inference    |
| Vector Store    | Chroma              | FAISS, Pinecone, Weaviate           | Simple local persistence, easy Python API       |
| LLM Interface   | Ollama (local Llama)| OpenAI, Cohere, GPT4All             | Local execution avoids latency and API costs    |
| Charts & Viz    | Matplotlib          | Plotly, Altair, Bokeh               | Familiar API with extensive customization       |


