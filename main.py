from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Google GenAI
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0
)

# Connect to database
db = SQLDatabase.from_uri(os.getenv("DATABASE_URL"))

# Create SQL toolkit and agent
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type="openai-tools"
)

def ask_question(question: str):
    """Ask a question about the Pagila database"""
    try:
        result = agent_executor.invoke({"input": question})
        return result["output"]
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    print("🎬 Pagila Database Q&A Terminal")
    print("Ask questions about movies, actors, rentals, etc.")
    print("Type 'quit' to exit\n")
    
    while True:
        question = input("Your question: ")
        if question.lower() in ['quit', 'exit', 'q']:
            break
        
        print("\nProcessing...")
        answer = ask_question(question)
        print(f"\nAnswer: {answer}\n")
        print("-" * 50)