from langchain_ollama import ChatOllama
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import WikipediaLoader
from langchain_text_splitters import TokenTextSplitter
from langchain_experimental.graph_transformers.llm import LLMGraphTransformer
from app.database import get_graph
from langchain_ollama import ChatOllama

load_dotenv()

def ingest_wikipedia_topic(topic: str):
    graph = get_graph()
    
    # 1. Load data from Wikipedia
    print(f"Loading data for: {topic}...")
    raw_docs = WikipediaLoader(query=topic, load_max_docs=5).load()
    
    # 2. Split into chunks
    text_splitter = TokenTextSplitter(chunk_size=1000, chunk_overlap=200)
    documents = text_splitter.split_documents(raw_docs)
    
    # 3. Transform to Graph
    # Note: Using Groq here for faster extraction
    llm = ChatOllama(model="gemma3:4b", temperature=0)
    llm_transformer = LLMGraphTransformer(llm=llm)
    
    print("Transforming text to graph documents...")
    graph_documents = llm_transformer.convert_to_graph_documents(documents)
    
    # 4. Add to Neo4j
    print("Writing to Neo4j...")
    graph.add_graph_documents(
        graph_documents,
        baseEntityLabel=True,
        include_source=True
    )
    print("Ingestion complete!")

if __name__ == "__main__":
    ingest_wikipedia_topic("Nikola Tesla")