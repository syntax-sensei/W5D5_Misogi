from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import create_sql_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

# Load environment variables at module level
load_dotenv(override=True)

def create_sql_chat_agent():
    """Create and return a SQL chat agent"""
    try:
        # Get API key explicitly and validate
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key not found in environment variables")
        
        if not api_key.startswith("sk-"):
            raise ValueError("Invalid OpenAI API key format")
            
        print(f"Using API key: {api_key[:15]}...{api_key[-10:]}")
        
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(script_dir, "qc.db")
        
        # Connect to SQLite DB using absolute path
        db = SQLDatabase.from_uri(f"sqlite:///{db_path}")
        
        # Verify database connection
        print(f"Connected to database at: {db_path}")
        print(f"Connected to database with {len(db.get_usable_table_names())} tables")
        print(f"Available tables: {db.get_usable_table_names()}")
        
        # Set environment variable explicitly for OpenAI
        os.environ["OPENAI_API_KEY"] = api_key
        
        # Initialize LLM - let it use environment variable
        llm = ChatOpenAI(
            model="gpt-4o", 
            temperature=0
        )
        
        # Create SQL agent using the modern approach
        agent = create_sql_agent(
            llm=llm,
            db=db,
            verbose=True,
            agent_type="openai-tools",
            handle_parsing_errors=True
        )
        
        return agent
        
    except Exception as e:
        print(f"Error creating agent: {e}")
        return None

def query_database(question: str):
    """Query the database with a natural language question"""
    agent = create_sql_chat_agent()
    if agent is None:
        return "Failed to create database agent"
    
    try:
        response = agent.invoke({"input": question})
        return response["output"]
    except Exception as e:
        print(f"Error querying database: {e}")
        return f"Error: {e}"

if __name__ == "__main__":
    # Simple test mode - you can change this or remove it
    test_question = input("Enter your question: ")
    if test_question.strip():
        print(f"Question: {test_question}")
        print("=" * 50)
        result = query_database(test_question)
        print(f"Answer: {result}")
    else:
        print("No question provided. Use the frontend to ask questions.")
