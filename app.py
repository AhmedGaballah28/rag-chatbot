import streamlit as st
import html
from RAG import process_documents
from LLM import get_database, memory, get_response_from_LLM
from langchain.schema import HumanMessage, AIMessage


def sanitize_html(content: str) -> str:
    """Sanitize content to prevent XSS attacks"""
    if not content:
        return ""
    return html.escape(str(content))


st.set_page_config(page_title="Chat-Bot with RAG", page_icon="🤖")

st.title("Chat-Bot with RAG")
st.markdown("#### A simple chat-bot application with Retrieval-Augmented Generation (RAG) capabilities.")
st.markdown("------------------------------------------------")

if "engine" not in st.session_state:
    st.session_state["engine"] = None
if "agent" not in st.session_state:
    st.session_state["agent"] = None
if "initialized" not in st.session_state:
    memory.chat_memory.add_message(AIMessage(content="Hello! How can I assist you today?"))
    st.session_state["initialized"] = True
if "raw_docs" not in st.session_state:
    st.session_state["raw_docs"] = []
if "last_processed_input" not in st.session_state:
    st.session_state["last_processed_input"] = ""

user_input = st.chat_input("You: ")

if user_input and user_input != st.session_state["last_processed_input"]:
    st.session_state["last_processed_input"] = user_input
    
    if st.session_state["agent"] is None:
        if st.session_state["engine"]:
            retriever = st.session_state["engine"].as_retriever(
                search_type="mmr",
                search_kwargs={"k": 3, "fetch_k": 6, "lambda_mult": 0.5},
            )
        else:
            retriever = None

        st.session_state["agent"] = get_response_from_LLM(retriever)
    
    response = st.session_state["agent"].invoke({"input": user_input})

    output_text = response.get("output") or response.get("result") or str(response)

for msg in memory.chat_memory.messages:
    # Sanitize message content to prevent XSS
    safe_content = sanitize_html(msg.content)
    
    if msg.type == "human":
        st.markdown(
            f"""
            <div style="display: flex; justify-content: flex-end; align-items: center; margin: 24px 0;">
                <div style="background-color: #2E7EF7; color: white; padding: 10px; border-radius: 10px; max-width: 70%; margin-right: 10px;">
                    {safe_content}
                </div>
                <div style="width: 35px; height: 35px; border-radius: 50%; background-color: #2E7EF7; display: flex; justify-content: center; align-items: center;">
                    <span style="color: white;">👤</span>
                </div>
            </div>
            """, unsafe_allow_html=True
        )
    elif msg.type == "ai":
        st.markdown(
            f"""
            <div style="display: flex; justify-content: flex-start; align-items: center; margin: 24px 0;">
                <div style="width: 35px; height: 35px; border-radius: 50%; background-color: #383838; display: flex; justify-content: center; align-items: center; margin-right: 10px;">
                    <span style="color: white;">🤖</span>
                </div>
                <div style="background-color: #383838; color: white; padding: 10px; border-radius: 10px; max-width: 70%;">
                    {safe_content}
                </div>
            </div>
            """, unsafe_allow_html=True
        )

with st.sidebar:
    st.markdown("### Settings")
    uploaded_files = st.file_uploader("Upload your documents here", accept_multiple_files=True)
    if st.button("Process Documents"):
        if uploaded_files:
            db, docs = process_documents(uploaded_files)
            st.session_state["engine"] = db
            st.session_state["raw_docs"] = docs
            st.session_state["agent"] = None  
            st.success("Documents processed successfully!")
        else:
            st.warning("Please upload at least one document.")