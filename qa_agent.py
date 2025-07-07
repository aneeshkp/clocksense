from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_community.llms import OpenAI
from langchain_ollama import OllamaLLM
from langchain.chains import RetrievalQA


def initialize_qa(embed_model: str = "all-MiniLM-L6-v2", llm_model: str = "llama3"):
    """
    Initialize the RAG QA chain using specified embedding and LLM models.
    """
    # Embedding setup using langchain-huggingface
    embeddings = HuggingFaceEmbeddings(model_name=embed_model)
    # Vector store setup using langchain-chroma
    vectordb = Chroma(embedding_function=embeddings, persist_directory="./chroma_db")

    # LLM selection: hosted OpenAI or local Ollama
    if llm_model.startswith("gpt-"):
        llm = OpenAI(model_name=llm_model)
    else:
        llm = OllamaLLM(model=llm_model)

    # Build retrieval-based QA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectordb.as_retriever(),
        chain_type="stuff"
    )
    return qa_chain, vectordb


def ask_question(question: str, qa_chain):
    """
    Ask a natural language question to the QA chain.
    """
    # Use invoke() to avoid deprecation
    return qa_chain.invoke(question)
