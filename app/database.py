import os
from dotenv import load_dotenv
from langchain_neo4j import Neo4jGraph
from langchain_community.vectorstores import Neo4jVector
from langchain_ollama import OllamaEmbeddings

load_dotenv()

# [cite_start]Initialize the Graph [cite: 6]
graph = Neo4jGraph()

# [cite_start]Initialize the Vector Index for Hybrid Search [cite: 8, 9]
vector_index = Neo4jVector.from_existing_graph(
    embedding=OllamaEmbeddings(model="embeddinggemma"),
    embedding_node_property="embedding",
    search_type="hybrid",
    node_label="Document",
    text_node_properties=["text"]
)

def get_graph():
    return graph

def get_vector_index():
    return vector_index

