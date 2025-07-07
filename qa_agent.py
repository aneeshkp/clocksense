from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM
from langchain.chains import RetrievalQA


def initialize_qa():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectordb = Chroma(embedding_function=embeddings, persist_directory="./chroma_db")
    llm = OllamaLLM(model="llama3")
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectordb.as_retriever(),
        chain_type="stuff"
    )
    return qa_chain, vectordb


def ask_question(question, qa_chain):
    # Use invoke() to avoid deprecated run()
    return qa_chain.invoke(question)
