import os
import streamlit as st
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Directories
BASE_DIR = r"c:\Users\user\Documents\DMDG_UT"
DB_DIR = os.path.join(BASE_DIR, "RAG", "chroma_db")

st.set_page_config(page_title="DMDG 회의록 AI 비서", page_icon="🤖", layout="centered")
st.title("🤖 DMDG 지식 관리 AI 비서")
st.markdown("회의록 데이터베이스를 기반으로 무엇이든 물어보세요!")

@st.cache_resource
def load_rag_pipeline():
    if not os.path.exists(DB_DIR):
        return None, "Vector DB가 없습니다. 먼저 ingest.py를 실행해주세요."
    
    try:
        embeddings = HuggingFaceEmbeddings(model_name="jhgan/ko-sroberta-multitask")
        vectorstore = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
        
        llm = Ollama(model="sgamma4:latest")
        
        template = """당신은 당목담글(DMDG) 프로젝트의 수석 지식 관리자입니다.
아래에 제공된 회의록 문맥(Context)을 바탕으로 사장님의 질문(Question)에 가장 정확하고 도움이 되는 답변을 한국어로 작성하세요.
문맥에 없는 내용이라면 지어내지 말고, "제공된 회의록에서는 해당 내용을 찾을 수 없습니다."라고 정직하게 답변하세요.

Context: {context}

Question: {question}

Answer:"""
        prompt = PromptTemplate.from_template(template)
        
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)
            
        rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
        
        return rag_chain, retriever
    except Exception as e:
        return None, f"파이프라인 로드 오류: {e}"

rag_chain, retriever_or_error = load_rag_pipeline()

if rag_chain is None:
    st.error(retriever_or_error)
else:
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("회의록에 대해 질문을 입력하세요 (예: 썸네일 전략이 뭐야?)"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            with st.spinner("회의록을 뒤져보고 있습니다..."):
                try:
                    response = rag_chain.invoke(prompt)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
                    # 출처 표시
                    docs = retriever_or_error.invoke(prompt)
                    sources = set([doc.metadata.get("source", "Unknown") for doc in docs])
                    st.caption("📚 **참고한 회의록 출처:**")
                    for src in sources:
                        st.caption(f"- {src}")
                except Exception as e:
                    st.error(f"답변 생성 중 오류가 발생했습니다. Ollama가 실행 중인지 확인해주세요.\n\n에러: {e}")
