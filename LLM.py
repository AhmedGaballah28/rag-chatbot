from dotenv import load_dotenv
from typing import Any

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain.agents import create_react_agent ,AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain_community.vectorstores import Chroma
from langchain_core.tools import tool

load_dotenv()

prompt = ChatPromptTemplate.from_template(
    """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Always start with the tool which called search_docs_from_RAG check if the question can be answered from the context provided by the documents. 
If the context is not sufficient, you can use your own knowledge to answer the question or other tools to get the answer.

Begin!

Question: {input}

{agent_scratchpad}

{chat_history}
"""
)

llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

def get_database(database_instance):
    global database
    database = database_instance
    return 0

def get_response_from_LLM(retriever=None) -> AgentExecutor:
    @tool("search_docs_from_RAG")
    def search_docs_from_RAG(query: str) -> Any:
        """Searches the vector database for relevant documents based on the query."""
        if retriever is None:
            return "No documents have been processed yet. Please upload and process documents first."
        result = retriever.invoke(query)
        return result
    
    react_agent = create_react_agent(
        llm=llm,
        tools=[search_docs_from_RAG],
        prompt=prompt
    )
    
    return AgentExecutor(
        agent=react_agent,
        tools=[search_docs_from_RAG],
        verbose=True,
        memory=memory,
        handle_parsing_errors=True,
        max_iterations=6,
    )