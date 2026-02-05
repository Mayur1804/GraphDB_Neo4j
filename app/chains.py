from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (
    RunnableLambda, RunnableBranch, RunnablePassthrough, RunnableParallel
)
from langchain_core.messages import AIMessage, HumanMessage
from app.schemas import Entities
from app.database import get_vector_index
from app.tools import structured_retriever, normalize_text

# Models
llmgemma = ChatOllama(model="gemma3:4b", temperature=0.1)
vector_index = get_vector_index()

# Entity Extraction
entity_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are extracting organization and person entities from the text."),
    ("human", "Use the given format to extract information from the following input: {question}"),
])
entity_chain = entity_prompt | llmgemma.with_structured_output(Entities)

# Retriever Tool
def retriever_logic(question: str):
    structured_data = structured_retriever(question, entity_chain)
    unstructured_data = [el.page_content for el in vector_index.similarity_search(question)]
    return f"Structured data:\n{structured_data}\nUnstructured data:\n{'#Document '.join(unstructured_data)}"

# History Formatting
def _format_chat_history(chat_history):
    buffer = []
    for human, ai in chat_history:
        buffer.append(HumanMessage(content=human))
        buffer.append(AIMessage(content=ai))
    return buffer

# Search Query Branch
_template = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question.
Chat History: {chat_history}
Follow Up Input: {question}
Standalone question:"""
CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_template)

search_query = RunnableBranch(
    (
        RunnableLambda(lambda x: bool(x.get("chat_history"))),
        RunnablePassthrough.assign(chat_history=lambda x: _format_chat_history(x["chat_history"]))
        | CONDENSE_QUESTION_PROMPT | ChatOllama(model="gemma3:4b", temperature=0) | StrOutputParser(),
    ),
    RunnableLambda(lambda x: x["question"]),
)

# Main Chain
template = """Answer the question based only on the following context:
{context}
Question: {question}
Use natural language and be concise.
Answer:"""
prompt = ChatPromptTemplate.from_template(template)

rag_chain = (
    RunnableParallel({
        "context": search_query | retriever_logic,
        "question": RunnablePassthrough(),
    })
    | prompt | llmgemma | StrOutputParser() | RunnableLambda(normalize_text)
)