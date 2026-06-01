import os
import re
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# Directories
BASE_DIR = r"c:\Users\user\Documents\DMDG_UT"
NOTES_DIR = os.path.join(BASE_DIR, "회의록")
DB_DIR = os.path.join(BASE_DIR, "RAG", "chroma_db")

def ingest_documents():
    print("1. Loading Markdown documents from 회의록 folder...")
    if not os.path.exists(NOTES_DIR):
        print(f"Error: Directory {NOTES_DIR} does not exist.")
        return

    # 1. Load markdown files
    documents = []
    for filename in os.listdir(NOTES_DIR):
        if filename.endswith(".md"):
            filepath = os.path.join(NOTES_DIR, filename)
            loader = TextLoader(filepath, encoding="utf-8")
            documents.extend(loader.load())
            print(f" - Loaded: {filename}")

    # 2. Split documents by headers
    print("\n2. Splitting documents by Markdown headers...")
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]
    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    
    docs_chunks = []
    for doc in documents:
        # Markdown splitter drops original metadata, so we keep track of the source file
        chunks = markdown_splitter.split_text(doc.page_content)
        for chunk in chunks:
            chunk.metadata["source"] = os.path.basename(doc.metadata["source"])
            docs_chunks.append(chunk)

    print(f" - Total chunks created: {len(docs_chunks)}")

    # 3. Create Embeddings & Store in ChromaDB
    print("\n3. Generating embeddings and storing in local ChromaDB...")
    # Use a fast local model for Korean & English
    embeddings = HuggingFaceEmbeddings(model_name="jhgan/ko-sroberta-multitask")
    
    # Store in Chroma
    vectorstore = Chroma.from_documents(
        documents=docs_chunks, 
        embedding=embeddings, 
        persist_directory=DB_DIR
    )
    
    print("\n✅ Ingestion Complete! Meeting notes are now stored as vectors in RAG/chroma_db.")

if __name__ == "__main__":
    ingest_documents()
