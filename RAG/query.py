import os
import argparse
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA

# Directories
BASE_DIR = r"c:\Users\user\Documents\DMDG_UT"
DB_DIR = os.path.join(BASE_DIR, "RAG", "chroma_db")

def query_rag(question):
    print("Initializing RAG pipeline...\n")
    
    if not os.path.exists(DB_DIR):
        print(f"Error: Vector database not found at {DB_DIR}. Please run ingest.py first.")
        return

    # Load Embeddings & Chroma DB
    embeddings = HuggingFaceEmbeddings(model_name="jhgan/ko-sroberta-multitask")
    vectorstore = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)
    
    # Initialize Local LLM via Ollama
    try:
        llm = Ollama(model="sgamma4:latest")
    except Exception as e:
        print("Error connecting to Ollama. Make sure Ollama app is running locally.")
        return

    # Define custom prompt
    prompt_template = """당신은 당목담글(DMDG) 프로젝트의 수석 지식 관리자입니다.
아래에 제공된 회의록 및 문서의 문맥(Context)을 바탕으로 사장님의 질문(Question)에 가장 정확하고 도움이 되는 답변을 작성하세요.
문맥에 없는 내용이라면 지어내지 말고, "제공된 회의록에서는 해당 내용을 찾을 수 없습니다."라고 정직하게 답변하세요.

Context: {context}

Question: {question}

Answer (in Korean):"""
    
    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    # Set up RetrievalQA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": 4}),
        return_source_documents=True,
        chain_type_kwargs={"prompt": PROMPT}
    )

    # Run the query
    print(f"🤔 Question: {question}")
    print("⏳ Searching through meeting notes and generating answer...\n")
    
    response = qa_chain.invoke({"query": question})
    
    # Print the answer
    print("💡 Answer:")
    print("-" * 50)
    print(response['result'])
    print("-" * 50)
    
    # Print sources
    print("\n📚 Sources referenced:")
    sources = set([doc.metadata.get("source", "Unknown") for doc in response['source_documents']])
    for src in sources:
        print(f" - {src}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query the DMDG Meeting Notes RAG system.")
    parser.add_argument("question", nargs="?", default="이전 회의록에 따르면 명성황후 롱폼 영상의 기획 의도와 어그로 전략은 무엇이었지?", help="The question to ask the AI.")
    args = parser.parse_args()
    
    query_rag(args.question)
