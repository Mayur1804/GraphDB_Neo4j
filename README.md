# GraphDB_Neo4j

This README is designed for a professional GitHub repository. It includes project badges, a clear directory structure, and instructions for both the **Ingestion** and **Chat** phases.

---

# 👑 GraphRAG Explorer: Hybrid Knowledge Search

A powerful **Graph Retrieval-Augmented Generation (RAG)** system that combines the structured precision of **Neo4j Knowledge Graphs** with the semantic depth of **Vector Search**. This project uses **Groq** for high-speed inference and **Ollama** for local embeddings, allowing you to turn any Wikipedia topic into a searchable intelligence hub.

---

## 📂 Project Structure

```text
graph_rag_project/
├── app/
│   ├── database.py      # Neo4j connection & Hybrid Vector Index setup
│   ├── tools.py         # Custom Cypher logic & text normalization
│   ├── schemas.py       # Pydantic models for entity extraction
│   └── chains.py        # LCEL Chat & Retrieval pipelines
├── .env                 # API keys & DB credentials (HIDDEN)
├── ingest_data.py       # SCRIPT: Populates Neo4j from Wikipedia
├── main.py              # SCRIPT: Interactive Chat CLI
└── requirements.txt     # List of dependencies

```

---

## 🚀 Getting Started

### 1. Prerequisites

* **Neo4j**: An active instance (AuraDB or Desktop).
* **Ollama**: Installed with `embeddinggemma` and `gemma3:4b` models.
* **Groq API Key**: Obtain from the [Groq Console](https://console.groq.com/).

### 2. Installation

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
pip install -r requirements.txt

```

### 3. Environment Setup

Create a `.env` file in the root:

```env
NEO4J_URI=neo4j+s://your-id.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your-secure-password
GROQ_API_KEY=gsk_your_key_here

```

---

## 🛠️ Usage

### Step 1: Ingest Data

Before chatting, populate your graph with a topic (e.g., "Elizabeth I" or "SpaceX").

```bash
python ingest_data.py

```

*This script fetches Wikipedia pages, splits them into chunks, uses an LLM to extract nodes/relationships, and saves them to Neo4j.*

### Step 2: Start Chatting

Run the main application to interact with your data.

```bash
python main.py

```

---

## 🧠 How It Works: Hybrid Retrieval

This system doesn't just "read" text; it understands connections.

1. **Entity Linking**: Extracts key names from your question using Groq.
2. **Graph Search**: Traverses 1-hop relationships in Neo4j to find direct facts (e.g., *X belongs to House Y*).
3. **Vector Search**: Uses Ollama embeddings to find descriptive text chunks related to the query.
4. **Synthesis**: Combines both "Fact" (Graph) and "Context" (Vector) into a final answer.

---

## 🤝 Contributing

Feel free to fork this project and submit PRs. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

[MIT](https://choosealicense.com/licenses/mit/)

---

### Verify your Data

To see your graph in action, log into your Neo4j Browser and run:

```cypher
MATCH (n)-[r]->(m) RETURN n, r, m LIMIT 50

```


Clear the Old Data
```cypher
MATCH (n) DETACH DELETE n;
```
