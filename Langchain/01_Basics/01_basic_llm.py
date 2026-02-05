"""
Module 1: Basics - Introduction to LLMs with LangChain

This module introduces you to the fundamental concept of using Language Models
with LangChain. You'll learn how to:
1. Initialize an LLM
2. Make simple calls
3. Understand the basic structure
"""

from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def example_openai():
    """Example using OpenAI's GPT model"""
    print("=" * 60)
    print("Example 1: Using OpenAI Chat Model")
    print("=" * 60)
    
    # Initialize the ChatOpenAI model
    # model_name can be: "gpt-4", "gpt-3.5-turbo", etc.
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0.7,  # Controls randomness (0.0 = deterministic, 1.0 = creative)
    )
    
    # Simple call to the LLM
    response = llm.invoke("What is LangChain in one sentence?")
    print(f"\nResponse: {response.content}\n")
    
    return llm

def example_google_gemini():
    """Example using Google's Gemini model (optional)"""
    print("=" * 60)
    print("Example 2: Using Google Gemini Model")
    print("=" * 60)
    
    # Check if Google API key is available
    if not os.getenv("GOOGLE_API_KEY"):
        print("\n⚠️  GOOGLE_API_KEY not found. Skipping Gemini example.")
        print("   Add GOOGLE_API_KEY to your .env file to use Gemini.\n")
        return None
    
    # Initialize the Gemini model
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.7,
    )
    
    # Simple call to the LLM
    response = llm.invoke("Explain what LangChain is in one sentence.")
    print(f"\nResponse: {response.content}\n")
    
    return llm

def example_ollama_local():
    """Example using local Ollama model (moondream)"""
    print("=" * 60)
    print("Example 3: Using Local Ollama Model (moondream)")
    print("=" * 60)
    
    try:
        # Initialize the local Ollama model
        # Make sure Ollama is running: ollama serve
        # And the model is pulled: ollama pull moondream:latest
        llm = ChatOllama(
            model="moondream:latest",
            temperature=0.7,
            base_url="http://localhost:11434",  # Default Ollama URL
        )
        
        # Simple call to the local LLM
        response = llm.invoke("What is LangChain in one sentence?")
        print(f"\nResponse: {response.content}\n")
        
        return llm
        
    except Exception as e:
        print(f"\n⚠️  Could not connect to Ollama: {e}")
        print("   Make sure Ollama is running: ollama serve")
        print("   And model is available: ollama pull moondream:latest\n")
        return None

def example_multiple_calls():
    """Example showing multiple calls to the LLM"""
    print("=" * 60)
    print("Example 4: Multiple LLM Calls")
    print("=" * 60)
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
    
    questions = [
        "What is Python?",
        "What is machine learning?",
        "What is artificial intelligence?"
    ]
    
    print("\nAsking multiple questions:\n")
    for i, question in enumerate(questions, 1):
        response = llm.invoke(question)
        print(f"Q{i}: {question}")
        print(f"A{i}: {response.content[:100]}...")  # First 100 chars
        print()

def main():
    """Main function to run all examples"""
    print("\n" + "=" * 60)
    print("LANGCHAIN BASICS: Introduction to LLMs")
    print("=" * 60 + "\n")
    
    # Run examples
    try:
        # OpenAI example (requires API key)
        if os.getenv("OPENAI_API_KEY"):
            example_openai()
        else:
            print("⚠️  OPENAI_API_KEY not found. Skipping OpenAI example.")
            print("   Add OPENAI_API_KEY to your .env file to use OpenAI.\n")
        
        # Google Gemini example (requires API key)
        example_google_gemini()
        
        # Local Ollama example (no API key needed!)
        example_ollama_local()
        
        # Multiple calls example (uses OpenAI)
        if os.getenv("OPENAI_API_KEY"):
            example_multiple_calls()
        
        print("=" * 60)
        print("✅ All examples completed!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure you have:")
        print("1. Installed all dependencies: pip install -r requirements.txt")
        print("2. For cloud LLMs: Set API keys in .env file")
        print("3. For local LLMs: Ollama running (ollama serve)\n")

if __name__ == "__main__":
    main()

