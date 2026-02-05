"""
Final Project Template
Replace this with your own project code
"""

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    """Your project main function"""
    print("=" * 60)
    print("Your LangChain Project")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  ERROR: OPENAI_API_KEY not found!")
        print("   Please create a .env file and add your OpenAI API key.\n")
        return
    
    # Initialize LLM
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
    
    # Your project code here
    print("\n🚀 Start building your project!\n")
    
    # Example: Simple interaction
    response = llm.invoke("Hello! This is my LangChain project.")
    print(f"Response: {response.content}\n")

if __name__ == "__main__":
    main()


