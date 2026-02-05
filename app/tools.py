import unicodedata
import re
from langchain_community.vectorstores.neo4j_vector import remove_lucene_chars
from app.database import get_graph

graph = get_graph()

def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def generate_full_text_query(input: str) -> str:
    full_text_query = ""
    words = [el for el in remove_lucene_chars(input).split() if el]
    for word in words[:-1]:
        full_text_query += f" {word}~2 AND"
    full_text_query += f" {words[-1]}~2"
    return full_text_query.strip()

def structured_retriever(question: str, entity_chain) -> str:
    result = []
    entities = entity_chain.invoke({"question": question})
    for entity in entities.names:
        # Using your specific Cypher query from the upload
        response = graph.query(
            """
            CALL db.index.fulltext.queryNodes('keyword', $query, {limit: 5})
            YIELD node AS doc, score
            MATCH (doc)-[:MENTIONS]->(entity)
            CALL (entity) {
              MATCH (entity)-[r]->(neighbor)
              RETURN entity.id + ' - ' + type(r) + ' -> ' + neighbor.id AS output
              UNION ALL
              MATCH (entity)<-[r]-(neighbor)
              RETURN neighbor.id + ' - ' + type(r) + ' -> ' + entity.id AS output
            }
            RETURN DISTINCT output
            LIMIT 50
            """,
            {"query": entity},
        )
        result.extend(row["output"] for row in response)
    return "\n".join(result)