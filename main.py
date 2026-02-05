from app.chains import rag_chain

def start_chat():
    print("Graph RAG System Ready. Type 'exit' to quit.")
    history = []
    
    while True:
        query = input("\nYou: ")
        if query.lower() in ["exit", "quit"]:      
            break
            
        result = rag_chain.invoke({
            "question": query,
            "chat_history": history
        })
        
        print(f"\nAI: {result}")
        history.append((query, result))

if __name__ == "__main__":
    start_chat()